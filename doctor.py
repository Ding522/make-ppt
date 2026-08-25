#!/usr/bin/env python3
"""Diagnose make-ppt dependencies and registered client installations."""

from __future__ import annotations

import argparse
import importlib.util
import json
import platform
import shutil
import sys
from importlib import metadata
from pathlib import Path
from typing import Any

from client_registry import (
    AGENT_FORMATS,
    ClientSpec,
    agent_target,
    legacy_skill_targets,
    load_registry,
    skill_target,
)


AGENT_NAMES = ("ppt-planner", "ppt-builder")
PYTHON_MODULES = {
    "pptx": "python-pptx",
    "PIL": "Pillow",
    "openpyxl": "openpyxl",
    "docx": "python-docx",
    "pypdf": "pypdf",
}


def parse_args(registry: dict[str, ClientSpec]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--client",
        choices=(*registry, "all"),
        default="all",
        help="Inspect one registered client or all clients (default: all).",
    )
    parser.add_argument(
        "--scope",
        choices=("user", "project"),
        default="user",
        help="Inspect user or project installations (default: user).",
    )
    parser.add_argument(
        "--project-dir",
        type=Path,
        default=Path.cwd(),
        help="Project root for --scope project (default: current directory).",
    )
    parser.add_argument(
        "--home-dir",
        type=Path,
        default=None,
        help=argparse.SUPPRESS,
    )
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    return parser.parse_args()


def check_python() -> dict[str, Any]:
    modules = {}
    for module, package in PYTHON_MODULES.items():
        available = importlib.util.find_spec(module) is not None
        try:
            version = metadata.version(package) if available else None
        except metadata.PackageNotFoundError:
            version = None
        modules[package] = {
            "module": module,
            "available": available,
            "version": version,
        }
    supported_version = sys.version_info >= (3, 9)
    return {
        "status": "pass" if supported_version and all(item["available"] for item in modules.values()) else "fail",
        "executable": sys.executable,
        "version": platform.python_version(),
        "supported_version": supported_version,
        "modules": modules,
    }


def powerpoint_available() -> bool:
    if sys.platform != "win32":
        return any(
            path.is_dir()
            for path in (
                Path("/Applications/Microsoft PowerPoint.app"),
                Path.home() / "Applications" / "Microsoft PowerPoint.app",
            )
        )
    try:
        import winreg

        with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, r"PowerPoint.Application\CLSID"):
            return True
    except (ImportError, FileNotFoundError, OSError):
        return False


def libreoffice_path() -> str | None:
    command = shutil.which("soffice") or shutil.which("libreoffice")
    if command:
        return command
    if sys.platform == "win32":
        candidates = (
            Path("C:/Program Files/LibreOffice/program/soffice.exe"),
            Path("C:/Program Files (x86)/LibreOffice/program/soffice.exe"),
            Path.home() / "AppData/Local/Programs/LibreOffice/program/soffice.exe",
        )
    elif sys.platform == "darwin":
        candidates = (Path("/Applications/LibreOffice.app/Contents/MacOS/soffice"),)
    else:
        candidates = ()
    return next((str(path) for path in candidates if path.is_file()), None)


def check_rendering() -> dict[str, Any]:
    powerpoint = powerpoint_available()
    libreoffice = libreoffice_path()
    pdftoppm = shutil.which("pdftoppm")
    if sys.platform == "win32":
        usable = powerpoint or bool(libreoffice and pdftoppm)
    else:
        usable = bool(pdftoppm and (powerpoint or libreoffice))
    return {
        "status": "pass" if usable else "warn",
        "platform": sys.platform,
        "powerpoint": powerpoint,
        "libreoffice": libreoffice,
        "pdftoppm": pdftoppm,
        "note": (
            "A renderer is available."
            if usable
            else "PPTX generation can work, but rendered preview QA is unavailable."
        ),
    }


def check_client(
    spec: ClientSpec,
    scope: str,
    project_dir: Path,
    home_dir: Path | None,
) -> dict[str, Any]:
    skill = skill_target(spec, scope, project_dir, home_dir)
    agents = {
        name: str(agent_target(spec, name, scope, project_dir, home_dir))
        for name in AGENT_NAMES
    }
    agent_exists = {name: Path(path).is_file() for name, path in agents.items()}
    legacy = [
        str(path)
        for path in legacy_skill_targets(spec, scope, project_dir, home_dir)
        if path.exists() or path.is_symlink()
    ]
    installed = (skill / "SKILL.md").is_file()
    complete = installed and all(agent_exists.values())
    return {
        "status": "pass" if complete and not legacy else "warn",
        "display_name": spec.display_name,
        "agent_format": spec.agent_format,
        "skill": {"path": str(skill), "installed": installed},
        "agents": {
            name: {"path": path, "installed": agent_exists[name]}
            for name, path in agents.items()
        },
        "legacy_skills": legacy,
    }


def build_report(
    registry: dict[str, ClientSpec],
    client_ids: tuple[str, ...],
    scope: str,
    project_dir: Path,
    home_dir: Path | None,
) -> dict[str, Any]:
    python = check_python()
    rendering = check_rendering()
    clients = {
        client_id: check_client(
            registry[client_id], scope, project_dir, home_dir
        )
        for client_id in client_ids
    }
    statuses = [python["status"], rendering["status"]]
    statuses.extend(client["status"] for client in clients.values())
    overall = "fail" if "fail" in statuses else "warn" if "warn" in statuses else "pass"
    return {
        "schema_version": 1,
        "overall": overall,
        "scope": scope,
        "python": python,
        "rendering": rendering,
        "clients": clients,
        "known_agent_formats": list(AGENT_FORMATS),
    }


def render_text(report: dict[str, Any]) -> str:
    lines = [f"make-ppt doctor: {report['overall'].upper()}"]
    python = report["python"]
    lines.append(f"[{python['status'].upper()}] Python {python['version']} - {python['executable']}")
    if not python["supported_version"]:
        lines.append("  MISSING Python 3.9 or newer")
    for package, item in python["modules"].items():
        mark = "OK" if item["available"] else "MISSING"
        version = f" {item['version']}" if item["version"] else ""
        lines.append(f"  {mark:7} {package}{version} ({item['module']})")
    rendering = report["rendering"]
    lines.append(f"[{rendering['status'].upper()}] Rendering - {rendering['note']}")
    lines.append(f"  PowerPoint: {rendering['powerpoint']}")
    lines.append(f"  LibreOffice: {rendering['libreoffice'] or 'not found'}")
    lines.append(f"  pdftoppm: {rendering['pdftoppm'] or 'not found'}")
    for client_id, client in report["clients"].items():
        lines.append(f"[{client['status'].upper()}] {client_id} - {client['display_name']}")
        skill = client["skill"]
        lines.append(f"  Skill: {'OK' if skill['installed'] else 'MISSING'} - {skill['path']}")
        for name, agent in client["agents"].items():
            lines.append(f"  {name}: {'OK' if agent['installed'] else 'MISSING'} - {agent['path']}")
        for legacy in client["legacy_skills"]:
            lines.append(f"  LEGACY: {legacy}")
    return "\n".join(lines)


def main() -> int:
    repo_dir = Path(__file__).resolve().parent
    registry = load_registry(repo_dir / "integrations" / "clients.json")
    args = parse_args(registry)
    client_ids = tuple(registry) if args.client == "all" else (args.client,)
    report = build_report(
        registry,
        client_ids,
        args.scope,
        args.project_dir.resolve(),
        args.home_dir.resolve() if args.home_dir else None,
    )
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(render_text(report))
    return 1 if report["python"]["status"] == "fail" else 0


if __name__ == "__main__":
    raise SystemExit(main())
