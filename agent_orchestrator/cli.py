from __future__ import annotations

import argparse
from pathlib import Path
import json

from .config import load_project_config, write_project_config
from .consensus import calculate_consensus
from .models import DEFAULT_ROUTES
from .policy import RoutingPolicy
from .providers import detect_provider
from .runs import create_run, latest_run
from .validation import validate_run


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="agent", description="Provider-agnostic coding-agent orchestrator")
    sub = parser.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init")
    init.add_argument("--profile", default="generic")
    start = sub.add_parser("start")
    start.add_argument("--task", required=True)
    route = sub.add_parser("route")
    route.add_argument("--risk", choices=["mechanical", "low", "normal", "high", "critical"], default="normal")
    route.add_argument("--role", choices=["exploration", "planning", "review", "implementation"], default="planning")
    provider = sub.add_parser("provider")
    provider.add_argument("name", choices=["claude-code", "codex", "copilot"])
    for name in ("status", "consensus", "validate"):
        sub.add_parser(name)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = Path.cwd()
    if args.command == "init":
        config = {"schema_version": 1, "project": {"name": root.name, "kind": "software"}, "profiles": [args.profile], "commands": {}, "context": {"required": []}, "risks": {}}
        print(write_project_config(root, config))
        return 0
    if args.command == "route":
        policy = RoutingPolicy()
        model = policy.model_for(args.risk)
        role = args.role
        route = DEFAULT_ROUTES["complex_implementation"] if role == "implementation" and args.risk in {"high", "critical"} else DEFAULT_ROUTES.get(role, DEFAULT_ROUTES["planning"])
        print(json.dumps({"role": role, "risk": args.risk, "provider": route.provider, "model": model, "effort": route.effort}, indent=2))
        return 0
    if args.command == "provider":
        print(json.dumps(detect_provider(args.name).__dict__, indent=2))
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
        print((run / "task.json").read_text(encoding="utf-8"))
    elif args.command == "consensus":
        print(json.dumps(calculate_consensus(run), indent=2))
    elif args.command == "validate":
        errors = validate_run(run)
        print(json.dumps({"valid": not errors, "errors": errors}, indent=2))
        return 1 if errors else 0
    return 0
