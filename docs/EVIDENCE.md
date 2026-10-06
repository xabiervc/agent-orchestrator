# Evidence

Evidence is stored under `.agent/runs/<run-id>/evidence/`.

A manifest records:

- run ID;
- timestamp;
- screenshots, logs, reports, and test outputs;
- optional hashes and descriptions.

A non-empty, matching manifest is required by the default evidence quality gate.
