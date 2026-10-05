# Provider Adapters

Adapters produce explicit command plans for installed CLIs. They do not execute commands and do not store credentials.

Supported command families:

- Claude Code: `claude --model <alias> --permission-mode plan --prompt-file <path>`
- Codex: `codex --prompt-file <path>`
- Copilot: `copilot --prompt-file <path>`

Provider availability is external to the core. A missing provider must be recorded as unavailable and must not become an approval.
