# Research provenance

The design adapts concepts; it does not copy Matt Pocock's full prompts or require his runtime.

- [Matt's skills snapshot](https://github.com/mattpocock/skills/tree/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d): routing, grilling, domain modeling, vertical tasks, TDD, review, context boundaries and retrospective.
- [Course Video Manager snapshot](https://github.com/mattpocock/course-video-manager/tree/b47b1ec54cc7742326ca2682e49f09803cdac303): backlog Docker runner, Sandcastle orchestration and GitHub AFK platform. See matt-pocock-audit.md for source findings and conflicts.
- [Cucumber example mapping](https://cucumber.io/docs/bdd/example-mapping/): rules, concrete examples and unanswered questions.
- [HumanLayer context engineering](https://www.humanlayer.dev/blog/advanced-context-engineering): focused research/planning and useful review points.
- [Anthropic long-running harnesses](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents): incremental progress and durable session artifacts.
- [Codex non-interactive mode](https://developers.openai.com/codex/noninteractive/): stdin prompt transport and workspace-write permissions; checked 2026-11-01.
- [Claude Code headless mode](https://code.claude.com/docs/en/headless): print mode and stdin transport; checked 2026-11-01.

Provider CLIs evolve. Profile definitions need compatibility checks against installed versions before unattended use. The core contract remains independent of those commands.
