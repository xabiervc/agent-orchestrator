from __future__ import annotations

from pathlib import Path
import json


def calculate_consensus(run: Path) -> dict:
    proposals = list((run / "proposals").glob("*.json"))
    reviews = list((run / "reviews").glob("*.json"))
    result = {
        "run_id": run.name,
        "decision": "pending",
        "proposal_count": len(proposals),
        "review_count": len(reviews),
        "blocking_reasons": [],
    }
    if not proposals:
        result["blocking_reasons"].append("No proposal artifacts found.")
    elif not reviews:
        result["blocking_reasons"].append("No review artifacts found.")
    else:
        result["decision"] = "approve"
    (run / "consensus.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result
