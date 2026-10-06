from __future__ import annotations

import argparse
from pathlib import Path
import json

from .commands import build_project_command
from .config import load_project_config, write_project_config
from .consensus import calculate_consensus
from .evidence import append_evidence_entries, create_evidence_manifest, validate_evidence_manifest
from .handoff import create_handoff
from .lifecycle import RunState
from .quality import evaluate_quality, execute_quality_command
from .providers import detect_provider
from .routing import route_for, route_dict
from .runs import create_run, latest_run
from .validation import validate_run


def _parse_bool(value: str) -> bool:
    if value.lower() in {"true", "1", "yes", "pass", "passed"}:
        return True
    if value.lower() in {"false", "0", "no", "fail", "failed"}:
        return False
    raise argparse.ArgumentTypeError("Expected true or false.")


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
    transition = sub.add_parser("transition")
    transition.add_argument("--to", dest="target", choices=["planning", "reviewing", "consensus", "approved", "implementing", "verifying", "completed", "blocked", "failed"], required=True)
    handoff = sub.add_parser("handoff")
    handoff.add_argument("--provider", required=True)
    handoff.add_argument("--model", required=True)
    handoff.add_argument("--allowed-file", action="append", default=[])
    handoff.add_argument("--verify-command", action="append", default=[])
    quality = sub.add_parser("quality")
    quality.add_argument("--result", action="append", default=[], help="gate=true or gate=false")
    quality.add_argument("--command", dest="command_specs", action="append", default=[], help="gate=command")
    quality.add_argument("--timeout", type=int, default=300)
    evidence = sub.add_parser("evidence")
    evidence.add_argument("--entry", action="append", default=[], help="key=value,key=value")
    for name in ("status", "consensus", "validate"):
        sub.add_parser(name)
    return parser


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


def _quality_results(values: list[str]) -> dict[str, bool]:
    results = {}
    for item in values:
        key, separator, value = item.partition("=")
        if not separator:
            raise SystemExit("Quality results must use gate=true or gate=false.")
        results[key] = _parse_bool(value)
    return results


def _quality_commands(values: list[str], timeout: int) -> list[dict[str, object]]:
    results = []
    for item in values:
        name, separator, command = item.partition("=")
        if not separator or not name.strip() or not command.strip():
            raise SystemExit("Quality commands must use gate=command.")
        results.append(execute_quality_command(build_project_command(name.strip(), command.strip(), timeout_seconds=timeout)))
    return results


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = Path.cwd()
    if args.command == "init":
        config = {"schema_version": 1, "project": {"name": root.name, "kind": "software"}, "profiles": [args.profile], "commands": {}, "context": {"required": []}, "risks": {}}
        print(write_project_config(root, config))
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
            results[item["gate"]] = bool(item["passed"])
        if command_results:
            results["_evidence"] = command_results
            run = latest_run(root)
            if run is not None:
                append_evidence_entries(run, command_results)
        result = evaluate_quality(results)
        print(json.dumps({"passed": result.passed, "gates": result.gates, "failures": result.failures, "evidence": result.evidence}, indent=2))
        return 0 if result.passed else 1
    if args.command == "start":
        config = load_project_config(root)
        print(create_run(root, config, args.task))
        return 0
    run = _latest_or_error(root)
    if args.command == "transition":
        current = json.loads((run / "run.json").read_text(encoding="utf-8"))["state"]
        state = RunState(current).transition(args.target)
        data = json.loads((run / "run.json").read_text(encoding="utf-8"))
        data["state"] = state.state
        (run / "run.json").write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(data, indent=2))
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
        print((run / "task.json").read_text(encoding="utf-8"))
    elif args.command == "consensus":
        print(json.dumps(calculate_consensus(run), indent=2))
    elif args.command == "validate":
        errors = validate_run(run)
        print(json.dumps({"valid": not errors, "errors": errors}, indent=2))
        return 1 if errors else 0
    return 0
