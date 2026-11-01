# Model and effort policy

The workflow chooses task needs; the executor maps those needs to its own models and settings.

Initial advisory policy:
- Routine extraction and transformations: low or medium.
- Ordinary implementation and synthesis: medium.
- Complex planning, debugging and review: high.
- Exceptionally difficult unresolved reasoning: compare extra effort selectively.

Choose implementation and review settings independently. A capable implementation model plus a stronger reasoning/review model is one pilot candidate when review involves difficult correctness or architecture judgments. Routine reviews may use the same model; extra capacity is not proof of independent verification. Compare accepted results and missed defects before making this a default. Model names mentioned in a demonstration are examples, not pinned requirements.

Labels are not assumed equivalent across providers. The v0.1 helper inherits native settings and does not translate them automatically.

Missing facts require research; missing decisions require clarification; large scope requires slicing; unsupported conclusions require verification. Escalating effort alone does not solve these.

Track accepted outcomes, retries, latency, human review burden and usage where available. Optimize total cost per accepted result. Do not promise savings before pilot measurements.
