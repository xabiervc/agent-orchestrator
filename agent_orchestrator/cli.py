from __future__ import annotations

import argparse
import json
from pathlib import Path

from .artifacts import append_evidence_entries, latest_run, write_project_config
from .lifecycle import advance_task, start_task
from .providers import detect_provider
from .quality import evaluate_quality, execute_quality_command
from .routing import route_dict, route_for


def _quality_results(values: list[str]) -> dict[str, bool]:
    results: dict[str, bool] = {}
    for value in values:
        name, separator, status = value.partition("=")
        if not separator or not name.strip():
            raise ValueError("Quality results must use NAME=true|false syntax.")
        normalized = status.strip().lower()
        if normalized not in {"true", "false"}:
            raise ValueError("Quality result status must be true or false.")
        results[name.strip()] = normalized == "true"
    return results


def _quality_commands(values: list[str], timeout: int) -> list[dict[str, object]]:
    command_results: list[dict[str, object]] = []
    for value in values:
        name, separator, command = value.partition("=")
        if not separator or not name.strip() or not command.strip():
            raise ValueError("Quality commands must use NAME=COMMAND syntax.")
        report = execute_quality_command(name.strip(), command.strip(), timeout_seconds=timeout)
        gate = report.gates[0]
        command_results.append({"gate": gate.name, "passed": gate.passed, "details": gate.details})
    return command_results


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="agent")
    subparsers = parser.add_subparsers(dest="command", required=True)
    init_parser = subparsers.add_parser("init")
    init_parser.add_argument("--profile", default="software")
    start_parser = subparsers.add_parser("start")
    start_parser.add_argument("--task", required=True)
    advance_parser = subparsers.add_parser("advance")
    advance_parser.add_argument("--run", required=True)
    advance_parser.add_argument("--state", default="advanced")
    route_parser = subparsers.add_parser("route")
    route_parser.add_argument("--role", required=True)
    route_parser.add_argument("--risk", default="low")
    provider_parser = subparsers.add_parser("provider")
    provider_parser.add_argument("--name", required=True)
    quality_parser = subparsers.add_parser("quality")
    quality_parser.add_argument("--result", action="append", default=[])
    quality_parser.add_argument("--command", dest="command_specs", action="append", default=[])
    quality_parser.add_argument("--timeout", type=int, default=300)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = Path.cwd()
    if args.command == "init":
        config = {"schema_version": 1, "project": {"name": root.name, "kind": "software"}, "profiles": [args.profile], "commands": {}, "context": {"required": []}, "risks": {}}
        print(write_project_config(root, config))
        return 0
    if args.command == "start":
        run = start_task(root, args.task)
        print(run)
        return 0
    if args.command == "advance":
        run = Path(args.run)
        payload = advance_task(run, args.state)
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0
    if args.command == "route":
        selected = route_for(args.role, risk=args.risk)
        print(json.dumps({"role": args.role, "risk": args.risk, **route_dict(selected)}, indent=2))
        return 0
    if args.command == "provider":
        print(json.dumps(detect_provider(args.name).__dict__, indent=2))
        return 0
    if args.command == "quality":
        results = _quality_results(args.result)
        command_results = _quality_commands(args.command_specs, args.timeout) if args.command_specs else []
        for item in command_results:
            results[str(item["gate"])] = bool(item["passed"])
        if command_results:
            results["_evidence"] = all(bool(item["passed"]) for item in command_results)
            run = latest_run(root)
            if run is not None:
                append_evidence_entries(run, command_results)
        result = evaluate_quality(results)
        print(json.dumps(result.as_dict(), indent=2, sort_keys=True))
        return 0 if result.passed else 1
    return 2
