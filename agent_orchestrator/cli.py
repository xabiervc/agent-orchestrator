from __future__ import annotations

import argparse
import json
from pathlib import Path

from .commands import build_project_command
from .config import load_project_config, write_project_config
from .consensus import calculate_consensus
from .evidence import append_evidence_entries, create_evidence_manifest, validate_evidence_manifest
from .handoff import create_handoff
from .lifecycle import RunState
from .providers import detect_provider
from .quality import evaluate_quality, execute_quality_command
from .routing import route_for, route_dict
from .runs import create_run, latest_run
from .validation import validate_run


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="agent", description="Provider-agnostic coding-agent orchestrator")
    sub = parser.add_subparsers(dest="command", required=True)
    init_parser = sub.add_parser("init")
    init_parser.add_argument("--profile", default="generic")
    start_parser = sub.add_parser("start")
    start_parser.add_argument("--task", required=True)
    route_parser = sub.add_parser("route")
    route_parser.add_argument("--risk", choices=["mechanical", "low", "normal", "high", "critical"], default="normal")
    route_parser.add_argument("--role", choices=["exploration", "planning", "review", "implementation"], default="planning")
    provider_parser = sub.add_parser("provider")
    provider_parser.add_argument("name", choices=["claude-code", "codex", "copilot"])
    transition_parser = sub.add_parser("transition")
    transition_parser.add_argument("--to", dest="target", required=True)
    handoff_parser = sub.add_parser("handoff")
    handoff_parser.add_argument("--provider", required=True)
    handoff_parser.add_argument("--model", required=True)
    handoff_parser.add_argument("--allowed-file", action="append", default=[])
    handoff_parser.add_argument("--verify-command", action="append", default=[])
    quality_parser = sub.add_parser("quality")
    quality_parser.add_argument("--result", action="append", default=[])
    quality_parser.add_argument("--command", dest="command_specs", action="append", default=[])
    quality_parser.add_argument("--timeout", type=int, default=300)
    evidence_parser = sub.add_parser("evidence")
    evidence_parser.add_argument("--entry", action="append", default=[])
    for name in ("status", "consensus", "validate"):
        sub.add_parser(name)
    return parser


def _parse_bool(value: str) -> bool:
    if value.lower() in {"true", "1", "yes", "pass", "passed"}:
        return True
    if value.lower() in {"false", "0", "no", "fail", "failed"}:
        return False
    raise argparse.ArgumentTypeError("Expected true or false.")


def _latest_or_error(root: Path) -> Path:
    run = latest_run(root)
    if run is None:
        raise SystemExit("No runs found.")
    return run


def _parse_entries(values: list[str]) -> list[dict[str, str]]:
    entries = []
    for value in values:
        entry = {}
        for pair in value.split(","):
            key, separator, item = pair.partition("=")
            if not separator or not key.strip() or not item.strip():
                raise ValueError("Evidence entries must use key=value pairs.")
            entry[key.strip()] = item.strip()
        entries.append(entry)
    return entries


def _quality_commands(values: list[str], timeout: int, project_root: Path) -> list[dict[str, object]]:
    results = []
    for item in values:
        name, separator, command = item.partition("=")
        if not separator or not name.strip() or not command.strip():
            raise SystemExit("Quality commands must use gate=command.")
        plan = build_project_command(name.strip(), command.strip(), timeout_seconds=timeout)
        result = execute_quality_command(plan, project_root=project_root)
        if not isinstance(result, dict):
            raise TypeError("Command execution must return evidence mapping.")
        results.append(result)
    return results


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = Path.cwd()
    if args.command == "init":
        write_project_config(root, {"project": {"name": root.name}, "profiles": [args.profile]})
        return 0
    if args.command == "route":
        route = route_for(args.role, risk=args.risk)
        payload = {"role": args.role, "risk": args.risk, **route_dict(route)}
        print(json.dumps(payload, indent=2))
        return 0
    if args.command == "provider":
        print(json.dumps(detect_provider(args.name).__dict__, indent=2))
        return 0
    if args.command == "start":
        config = load_project_config(root)
        print(create_run(root, config, args.task))
        return 0
    if args.command == "quality":
        results: dict[str, bool] = {}
        for item in args.result:
            key, separator, value = item.partition("=")
            if not separator or not key.strip():
                raise SystemExit("Quality results must use gate=true or gate=false.")
            results[key.strip()] = _parse_bool(value)
        command_results: list[dict[str, object]] = []
        if args.command_specs:
            run = _latest_or_error(root)
            command_results = _quality_commands(args.command_specs, args.timeout, root)
            for item in command_results:
                results[str(item["gate"])] = bool(item["passed"])
            append_evidence_entries(run, command_results)
        result = evaluate_quality(results, required_gates=tuple(results.keys()))
        print(json.dumps(result.as_dict(), indent=2))
        return 0 if result.passed else 1
    run = _latest_or_error(root)
    if args.command == "transition":
        payload = json.loads((run / "run.json").read_text(encoding="utf-8"))
        state = RunState(payload.get("state", "created")).transition(args.target)
        payload["state"] = state.state
        (run / "run.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        state_path = run / "state.json"
        state_data = json.loads(state_path.read_text(encoding="utf-8")) if state_path.exists() else {"history": ["created"]}
        state_data["history"].append(state.state)
        state_data["state"] = state.state
        state_path.write_text(json.dumps(state_data, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(payload, indent=2))
        return 0
    if args.command == "handoff":
        print(json.dumps(create_handoff(run, args.provider, args.model, args.allowed_file, args.verify_command), indent=2))
        return 0
    if args.command == "evidence":
        manifest = create_evidence_manifest(run, _parse_entries(args.entry))
        errors = validate_evidence_manifest(manifest, run.name)
        print(json.dumps({"manifest": manifest, "valid": not errors, "errors": errors}, indent=2))
        return 0 if not errors else 1
    if args.command == "status":
        print((run / "run.json").read_text(encoding="utf-8"))
    elif args.command == "consensus":
        print(json.dumps(calculate_consensus(run), indent=2))
    elif args.command == "validate":
        print(json.dumps(validate_run(run), indent=2))
    return 0
