#!/usr/bin/env python3
"""Install the canonical make-ppt Agent Skill into supported AI clients."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


CLIENTS = ("codex", "claude", "kiro", "copilot")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install make-ppt into Agent Skills compatible AI clients."
    )
    parser.add_argument(
        "--client",
        choices=(*CLIENTS, "all"),
        default="all",
        help="Client to install for (default: all).",
    )
    parser.add_argument(
        "--scope",
        choices=("user", "project"),
        default="user",
        help="Install globally for the user or into one project (default: user).",
    )
    parser.add_argument(
        "--project-dir",
        type=Path,
        default=Path.cwd(),
        help="Project root for --scope project (default: current directory).",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace an existing make-ppt installation.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print target paths without writing files.",
    )
    return parser.parse_args()


def user_target(client: str) -> Path:
    roots = {
        "codex": Path.home() / ".agents" / "skills",
        "claude": Path.home() / ".claude" / "skills",
        "kiro": Path.home() / ".kiro" / "skills",
        "copilot": Path.home() / ".copilot" / "skills",
    }
    return roots[client] / "make-ppt"


def project_target(client: str, project_dir: Path) -> Path:
    roots = {
        "codex": project_dir / ".agents" / "skills",
        "claude": project_dir / ".claude" / "skills",
        "kiro": project_dir / ".kiro" / "skills",
        "copilot": project_dir / ".github" / "skills",
    }
    return roots[client] / "make-ppt"


def safe_to_replace(target: Path) -> bool:
    return target.name == "make-ppt" and target.parent.name == "skills"


def install_one(
    client: str,
    source: Path,
    codex_metadata: Path,
    target: Path,
    *,
    force: bool,
    dry_run: bool,
) -> None:
    print(f"{client:7} -> {target}")
    if dry_run:
        return

    if target.exists() or target.is_symlink():
        if not force:
            raise FileExistsError(
                f"{target} already exists; rerun with --force to replace it."
            )
        if not safe_to_replace(target):
            raise RuntimeError(f"Refusing to replace unexpected target: {target}")
        if target.is_dir() and not target.is_symlink():
            shutil.rmtree(target)
        else:
            target.unlink()

    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(
        source,
        target,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"),
    )

    if client == "codex" and codex_metadata.exists():
        metadata_target = target / "agents" / "openai.yaml"
        metadata_target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(codex_metadata, metadata_target)


def main() -> int:
    args = parse_args()
    repo_dir = Path(__file__).resolve().parent
    source = repo_dir / "skill" / "make-ppt"
    codex_metadata = repo_dir / "integrations" / "codex" / "openai.yaml"

    if not (source / "SKILL.md").is_file():
        raise FileNotFoundError(f"Canonical skill not found: {source}")

    clients = CLIENTS if args.client == "all" else (args.client,)
    project_dir = args.project_dir.resolve()

    jobs = []
    for client in clients:
        target = (
            user_target(client)
            if args.scope == "user"
            else project_target(client, project_dir)
        )
        jobs.append((client, target))

    existing = [
        target for _, target in jobs if target.exists() or target.is_symlink()
    ]
    if existing and not args.force and not args.dry_run:
        formatted = "\n".join(f"  - {target}" for target in existing)
        raise FileExistsError(
            "Installation stopped before making changes because these targets exist:\n"
            f"{formatted}\nRerun with --force to replace them."
        )

    for client, target in jobs:
        install_one(
            client,
            source,
            codex_metadata,
            target,
            force=args.force,
            dry_run=args.dry_run,
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
