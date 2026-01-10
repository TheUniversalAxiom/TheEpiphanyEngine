"""MCP server for the Universal Axiom."""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from typing import Any, Dict, Optional

from axiom.core_equation import compute_intelligence

AXIOM_FORMULA = "Intelligence_n = E_n * (1 + F_n) * X * Y * Z * (A * B * C)"


@dataclass
class MCPResponse:
    id: Optional[str]
    result: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, Any]] = None

    def to_json(self) -> str:
        payload: Dict[str, Any] = {"jsonrpc": "2.0", "id": self.id}
        if self.error is not None:
            payload["error"] = self.error
        else:
            payload["result"] = self.result
        return json.dumps(payload)


def _tool_schema() -> Dict[str, Any]:
    return {
        "name": "compute_universal_axiom",
        "description": "Compute the Universal Axiom intelligence score.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "A": {"type": "number"},
                "B": {"type": "number"},
                "C": {"type": "number"},
                "X": {"type": "number"},
                "Y": {"type": "number"},
                "Z": {"type": "number"},
                "E_n": {"type": "number"},
                "F_n": {"type": "number"},
                "validate": {"type": "boolean", "default": True},
                "clamp_to_unit": {"type": "boolean", "default": True},
                "strict_bounds": {"type": "boolean", "default": False},
                "return_components": {"type": "boolean", "default": True},
            },
            "required": ["A", "B", "C", "X", "Y", "Z", "E_n", "F_n"],
        },
    }


def _list_resources() -> Dict[str, Any]:
    return {
        "resources": [
            {
                "uri": "axiom://universal/formula",
                "name": "Universal Axiom Formula",
                "mimeType": "text/plain",
                "description": "Core intelligence equation for The Universal Axiom.",
            }
        ]
    }


def _read_resource(uri: str) -> Dict[str, Any]:
    if uri == "axiom://universal/formula":
        return {
            "contents": [
                {"uri": uri, "mimeType": "text/plain", "text": AXIOM_FORMULA}
            ]
        }
    raise ValueError(f"Unknown resource uri: {uri}")


def _handle_initialize() -> Dict[str, Any]:
    return {
        "protocolVersion": "2024-11-05",
        "serverInfo": {"name": "universal-axiom-mcp", "version": "0.1.0"},
        "capabilities": {
            "tools": {"compute_universal_axiom": _tool_schema()},
            "resources": _list_resources(),
        },
    }


def _handle_tools_list() -> Dict[str, Any]:
    return {"tools": [_tool_schema()]}


def _handle_tools_call(params: Dict[str, Any]) -> Dict[str, Any]:
    name = params.get("name")
    arguments = params.get("arguments", {})
    if name != "compute_universal_axiom":
        raise ValueError(f"Unknown tool: {name}")

    missing = [
        key
        for key in _tool_schema()["inputSchema"]["required"]
        if key not in arguments
    ]
    if missing:
        missing_list = ", ".join(missing)
        raise ValueError(f"Missing required arguments: {missing_list}")

    result = compute_intelligence(
        A=arguments["A"],
        B=arguments["B"],
        C=arguments["C"],
        X=arguments["X"],
        Y=arguments["Y"],
        Z=arguments["Z"],
        E_n=arguments["E_n"],
        F_n=arguments["F_n"],
        validate=arguments.get("validate", True),
        clamp_to_unit=arguments.get("clamp_to_unit", True),
        strict_bounds=arguments.get("strict_bounds", False),
        return_components=arguments.get("return_components", True),
    )

    if isinstance(result, tuple):
        score, components = result
        content = {
            "score": score,
            "components": components,
            "formula": AXIOM_FORMULA,
        }
    else:
        content = {"score": result, "formula": AXIOM_FORMULA}

    return {"content": [{"type": "json", "json": content}]}


def _dispatch(method: str, params: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    if method == "initialize":
        return _handle_initialize()
    if method == "tools/list":
        return _handle_tools_list()
    if method == "tools/call":
        if params is None:
            raise ValueError("Missing params for tools/call")
        return _handle_tools_call(params)
    if method == "resources/list":
        return _list_resources()
    if method == "resources/read":
        if params is None or "uri" not in params:
            raise ValueError("Missing uri for resources/read")
        return _read_resource(params["uri"])
    raise ValueError(f"Unknown method: {method}")


def _error_response(request_id: Optional[str], error: Exception) -> MCPResponse:
    return MCPResponse(
        id=request_id,
        error={
            "code": -32000,
            "message": str(error),
        },
    )


def serve(stdin: Any = sys.stdin, stdout: Any = sys.stdout) -> None:
    for line in stdin:
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
            request_id = payload.get("id")
            method = payload.get("method")
            params = payload.get("params")
            result = _dispatch(method, params)
            response = MCPResponse(id=request_id, result=result)
        except Exception as error:  # keep server alive
            response = _error_response(payload.get("id") if "payload" in locals() else None, error)
        stdout.write(response.to_json() + "\n")
        stdout.flush()


def main() -> None:
    serve()


if __name__ == "__main__":
    main()
