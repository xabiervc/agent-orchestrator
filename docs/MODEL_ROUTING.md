# Model Routing

The default policy is task-based rather than vendor-dependent.

| Work | Default | Escalate when |
|---|---|---|
| Exploration | Haiku | context is ambiguous |
| Normal planning | Sonnet | architecture or persistence is involved |
| Normal implementation | Sonnet-equivalent | risk is high |
| Architecture review | Opus | only with high-risk scope |
| Extended reasoning | Fable/manual | explicitly justified |

Aliases are resolved by the provider. A project must not assume that every provider exposes the same model names. The run records the requested alias and the provider-reported model when available.
