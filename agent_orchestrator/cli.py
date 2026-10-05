from __future__ import annotations

import argparse
from pathlib import Path
import json

from .config import load_project_config, write_project_config
from .consensus import calculate_consensus
from .runs import create_run, latest_run
from .validation import validate_run


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="agent", description="Provider-agnostic coding-agent orchestrator")
    sub = parser.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init")
    init.add_argument("--profile", default="generic")
    start = sub.add_parser("start")
    start.add_argument("--task", required=True)
    for name in ("status", "consensus", "validate"):
        sub.add_parser(name)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = Path.cwd()
    if args.command == "init":
        config = {"schema_version": 1, "project": {"name": root.name, "kind": "software"}, "profiles": [args.profile], "commands": {}, "context": {"required": []}, "risks": {}}
        path = write_project_config(root, config)
        print(path)
        return 0
    config = load_project_config(root)
    if args.command == "start":
        print(create_run(root, config, args.task))
        return 0
    run = latest_run(root)
    if run is None:
        print("No runs found.")
        return 1
    if args.command == "status":
        print(json.dumps(json.loads((run / "task.json").read_text()), indent=2))
    elif args.command == "consensus":
        print(json.dumps(calculate_consensus(run), indent=2))
    elif args.command == "validate":
        errors = validate_run(run)
        print(json.dumps({"valid": not errors, "errors": errors}, indent=2))
        return 1 if errors else 0
    return 0
