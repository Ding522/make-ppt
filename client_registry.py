#!/usr/bin/env python3
"""Load and resolve the make-ppt client integration registry."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REPO_DIR = Path(__file__).resolve().parent
DEFAULT_REGISTRY = REPO_DIR / "integrations" / "clients.json"
SCOPES = ("user", "project")
AGENT_FORMATS = ("codex-toml", "markdown")


@dataclass(frozen=True)
class ClientSpec:
    client_id: str
    display_name: str
    skill_roots: dict[str, str]
    agent_roots: dict[str, str]
    agent_path: str
    agent_format: str
    integration_dir: str
    skill_metadata: dict[str, str] | None
    legacy_skill_roots: dict[str, tuple[str, ...]]


def _relative_path(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty relative path")
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"{field} must stay relative to its scope root: {value}")
    return value


def _scoped_paths(raw: Any, field: str) -> dict[str, str]:
    if not isinstance(raw, dict):
        raise ValueError(f"{field} must be an object")
    return {
        scope: _relative_path(raw.get(scope), f"{field}.{scope}")
        for scope in SCOPES
    }


def _legacy_paths(raw: Any, field: str) -> dict[str, tuple[str, ...]]:
    if not isinstance(raw, dict):
        raise ValueError(f"{field} must be an object")
    result: dict[str, tuple[str, ...]] = {}
    for scope in SCOPES:
        values = raw.get(scope, [])
        if not isinstance(values, list):
            raise ValueError(f"{field}.{scope} must be a list")
        result[scope] = tuple(
            _relative_path(value, f"{field}.{scope}") for value in values
        )
    return result


def load_registry(path: Path = DEFAULT_REGISTRY) -> dict[str, ClientSpec]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if raw.get("schema_version") != 1:
        raise ValueError(f"unsupported client registry schema: {raw.get('schema_version')}")
    clients = raw.get("clients")
    if not isinstance(clients, dict) or not clients:
        raise ValueError("client registry must define at least one client")

    registry: dict[str, ClientSpec] = {}
    for client_id, data in clients.items():
        if not isinstance(data, dict):
            raise ValueError(f"client {client_id} must be an object")
        if not client_id.replace("-", "").isalnum() or client_id.lower() != client_id:
            raise ValueError(f"invalid client id: {client_id}")
        agent_format = data.get("agent_format")
        if agent_format not in AGENT_FORMATS:
            raise ValueError(f"unsupported agent format for {client_id}: {agent_format}")
        agent_path = _relative_path(data.get("agent_path"), f"{client_id}.agent_path")
        if "{agent_name}" not in agent_path:
            raise ValueError(f"{client_id}.agent_path must contain {{agent_name}}")
        integration_dir = _relative_path(
            data.get("integration_dir"), f"{client_id}.integration_dir"
        )
        metadata = data.get("skill_metadata")
        if metadata is not None:
            if not isinstance(metadata, dict):
                raise ValueError(f"{client_id}.skill_metadata must be an object")
            metadata = {
                "source": _relative_path(metadata.get("source"), f"{client_id}.skill_metadata.source"),
                "target": _relative_path(metadata.get("target"), f"{client_id}.skill_metadata.target"),
            }
        display_name = data.get("display_name")
        if not isinstance(display_name, str) or not display_name.strip():
            raise ValueError(f"{client_id}.display_name must be a non-empty string")

        registry[client_id] = ClientSpec(
            client_id=client_id,
            display_name=display_name,
            skill_roots=_scoped_paths(data.get("skill_roots"), f"{client_id}.skill_roots"),
            agent_roots=_scoped_paths(data.get("agent_roots"), f"{client_id}.agent_roots"),
            agent_path=agent_path,
            agent_format=agent_format,
            integration_dir=integration_dir,
            skill_metadata=metadata,
            legacy_skill_roots=_legacy_paths(data.get("legacy_skill_roots", {}), f"{client_id}.legacy_skill_roots"),
        )
    return registry


def scope_base(scope: str, project_dir: Path, home_dir: Path | None = None) -> Path:
    if scope == "project":
        return project_dir.resolve()
    if scope == "user":
        return (home_dir or Path.home()).resolve()
    raise ValueError(f"unsupported scope: {scope}")


def skill_target(spec: ClientSpec, scope: str, project_dir: Path, home_dir: Path | None = None) -> Path:
    return scope_base(scope, project_dir, home_dir) / spec.skill_roots[scope] / "make-ppt"


def agent_target(spec: ClientSpec, agent_name: str, scope: str, project_dir: Path, home_dir: Path | None = None) -> Path:
    relative = spec.agent_path.format(agent_name=agent_name)
    return scope_base(scope, project_dir, home_dir) / spec.agent_roots[scope] / relative


def legacy_skill_targets(spec: ClientSpec, scope: str, project_dir: Path, home_dir: Path | None = None) -> tuple[Path, ...]:
    base = scope_base(scope, project_dir, home_dir)
    current = skill_target(spec, scope, project_dir, home_dir).resolve()
    return tuple(
        base / root / "make-ppt"
        for root in spec.legacy_skill_roots[scope]
        if (base / root / "make-ppt").resolve() != current
    )
