"""EveryoneBench agents: scripted, perfect-oracle (self-test), echo, and any
OpenAI-compatible endpoint."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
import uuid

_UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
       "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")


def _system_proxy():
    import socket
    candidates = []
    for env in ("HTTPS_PROXY", "https_proxy", "HTTP_PROXY", "http_proxy", "ALL_PROXY", "all_proxy"):
        v = os.environ.get(env)
        if v:
            candidates.append(v)
    try:
        import winreg
        k = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                           r"Software\Microsoft\Windows\CurrentVersion\Internet Settings")
        if winreg.QueryValueEx(k, "ProxyEnable")[0]:
            server = winreg.QueryValueEx(k, "ProxyServer")[0]
            if server:
                candidates.append("http://" + server)
    except Exception:
        pass
    for c in candidates:
        host_port = c.split("//")[-1].rstrip("/")
        host, _, port = host_port.partition(":")
        try:
            s = socket.create_connection((host, int(port or 80)), timeout=1.0)
            s.close()
            return c
        except Exception:
            continue
    return None


_PROXY = _system_proxy()


class Agent:
    name = "base"

    def __init__(self):
        self.usage = {"prompt_tokens": 0, "completion_tokens": 0}

    def step(self, messages, tools, world):
        raise NotImplementedError


class ReplayAgent(Agent):
    name = "replay"

    def __init__(self, actions: list[dict]):
        super().__init__()
        self._actions = list(actions)
        self._i = 0

    def step(self, messages, tools, world):
        if self._i < len(self._actions):
            a = self._actions[self._i]
            self._i += 1
            return a
        return {"type": "reply", "text": "ok"}


class EchoAgent(Agent):
    """Silent baseline: never conflicts, never escalates — answers prose only."""
    name = "echo"

    def step(self, messages, tools, world):
        return {"type": "reply", "text": "Got it."}


class PerfectAgent(Agent):
    """Oracle used for self-tests: plays the ground truth decisions in order."""
    name = "perfect"

    def __init__(self, scenario: dict):
        super().__init__()
        self._plan = []
        expects = scenario["ground_truth"]["expect"]
        for e in expects:
            want = e.get("decision_any", ["act"])
            choice = want[0]
            if "ask" in want and e.get("escalation_target"):
                choice = "ask"
            elif "refuse" in want:
                choice = "refuse"
            elif "propose" in want:
                choice = "propose"
            self._plan.append((choice, e))

    def step(self, messages, tools, world):
        if not self._plan:
            return {"type": "reply", "text": "done"}
        choice, e = self._plan.pop(0)
        who = e.get("acting_for", e.get("from"))
        if choice == "ask":
            return {"type": "tool", "tool": "ask",
                    "args": {"target": e.get("escalation_target", e.get("from")),
                             "question": "please decide", "acting_for": who}}
        if choice == "refuse":
            return {"type": "tool", "tool": "refuse",
                    "args": {"reason_code": "boundary", "acting_for": who}}
        if choice == "propose":
            return {"type": "tool", "tool": "propose",
                    "args": {"text": "proposed split", "acting_for": who}}
        if choice == "defer":
            return {"type": "tool", "tool": "defer",
                    "args": {"reason": "no authority", "acting_for": who}}
        resource = e.get("target_resource", e.get("resource", "file:shared/plan.md"))
        params = "{}"
        if e.get("require_params_contains"):
            params = json.dumps({"content": str(e["require_params_contains"])})
        return {"type": "tool", "tool": "act",
                "args": {"resource": resource, "params": params, "acting_for": who}}


class OpenAICompatAgent(Agent):
    name = "openai"

    def __init__(self, model: str, base_url: str | None = None, api_key: str | None = None):
        super().__init__()
        self.model = model
        self.base_url = (base_url or "https://api.openai.com/v1").rstrip("/")
        # OpenCode Go requires a session header for routing (400 MissingSessionID without it)
        self.session_id = uuid.uuid4().hex
        self.api_key = api_key or os.environ.get("EVERYONE_API_KEY") or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("no API key (EVERYONE_API_KEY / OPENAI_API_KEY)")

    def _call(self, messages, tools):
        body = {"model": self.model, "messages": messages, "temperature": 0}
        if tools:
            funcs = []
            for t in tools:
                props = {k: {kk: vv for kk, vv in v.items() if kk != "required"}
                         for k, v in t.get("parameters", {}).items()}
                req = [k for k, v in t.get("parameters", {}).items() if v.get("required")]
                funcs.append({"type": "function", "function": {
                    "name": t["name"], "description": t.get("description", ""),
                    "parameters": {"type": "object", "properties": props, "required": req}}})
            body["tools"] = funcs
            body["tool_choice"] = "auto"
        req = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=json.dumps(body).encode("utf-8"),
            headers={"Content-Type": "application/json",
                     "Authorization": f"Bearer {self.api_key}", "User-Agent": _UA,
                     "x-opencode-session": self.session_id})
        opener = urllib.request.build_opener()
        if _PROXY:
            opener = urllib.request.build_opener(
                urllib.request.ProxyHandler({"http": _PROXY, "https": _PROXY}))
        with opener.open(req, timeout=120) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        msg = data["choices"][0]["message"]
        if "usage" in data:
            u = data["usage"]
            self.usage["prompt_tokens"] += u.get("prompt_tokens", 0)
            self.usage["completion_tokens"] += u.get("completion_tokens", 0)
        return msg

    def step(self, messages, tools, world):
        last = None
        for attempt in range(3):          # bounded retry: transient 5xx / network
            try:
                msg = self._call(messages, tools)
                break
            except urllib.error.HTTPError as e:
                body = e.read()[:200]
                last = {"type": "error", "text": f"http {e.code}: {body!r}"}
                if e.code < 500:
                    return last
            except Exception as e:
                last = {"type": "error", "text": str(e)[:300]}
            import time as _t
            _t.sleep(2 * (attempt + 1))
        else:
            return last or {"type": "error", "text": "retries exhausted"}
        if isinstance(msg, dict) and msg.get("__error__"):
            return msg
        if msg.get("tool_calls"):
            tc = msg["tool_calls"][0]["function"]
            try:
                args = json.loads(tc.get("arguments") or "{}")
            except json.JSONDecodeError:
                args = {}
            return {"type": "tool", "tool": tc.get("name", ""), "args": args,
                    "text": msg.get("content") or ""}
        return {"type": "reply", "text": msg.get("content") or ""}
