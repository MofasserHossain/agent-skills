# Context cost: files, discovery and activation

An installed file consumes disk space. It becomes model context only when the host supplies or the agent reads it. Installation scope does not itself determine token cost.

The source screenshot supplied by the user reports 12.5k total context tokens, including 660 attributed to nine skills, and 100 to memory files. These are observations from that particular session, host/version/model and installed set. They do not establish the cost of using every skill or a universal context threshold.

[Claude's skill documentation](https://code.claude.com/docs/en/skills#skill-descriptions-are-cut-short) describes a discovery listing of names/descriptions and the Skills row in /context. [Codex documentation](https://learn.chatgpt.com/docs/build-skills) describes metadata/path discovery followed by the selected instruction body. Detailed supporting material is read as needed. Host/version differences mean the screenshot is not an exact benchmark for another installation.

## Standard installed shape

Each user-selected skill has its own native discovery entry and bundled references/templates. Only metadata participates in discovery; selected bodies and supporting files load when needed. The optional agent-workflow router does not preload other skills. Standard installation does not copy research, tests, examples or Python tooling. More selected entries can increase discovery metadata; no exact savings are claimed.

## Legacy snapshot shape

- One small agent-workflow entry per selected host, pointing within the project snapshot.
- The router chooses the needed stage; it does not request all stage bodies.
- Only selected skills and linked supporting resources are installed; the helper is optional. Kit research, tests and examples remain in the authoring checkout. Installed supporting files stay on disk until needed.
- Project instructions/configuration, selected issue/spec and relevant evidence still contribute when read.
- Existing global/system skills, tools, MCP descriptions and conversation history contribute independently.

The source-copy snapshot trades disk duplication for independent project versions. It does not require reading the author's main workspace. Linked development mode reads the source checkout but should still load only the needed stages; a filesystem link alone is not the reason for large context.

## Verify on a real session

Use a fresh session in the target project and a known installed version. In Claude, inspect /context before invoking the workflow, then again after selecting a stage and reading its inputs. Identify memory/instruction, tool, skill-list and message contributions separately. In Codex, inspect the context/usage information the installed client exposes; do not assume it has Claude's same slash commands or categories.

Record host/model/version, visible discovery entries, loaded files and the actual task. Compare accepted outcomes, retries and total usage, not only the initial percentage. A larger context-window denominator can make a percentage smaller without reducing token count. Caching and context usage are distinct from total billing/allowance consumption.

Filesystem byte/word counts are useful for finding large instructions, but are not exact model token counts. No fixed saving or parity with the screenshot is claimed without measured native-session evidence. Do not launch a paid agent solely to manufacture a context measurement.

## Keep useful context small

Keep discovery descriptions concise and avoid duplicate linked/global/project registrations. Keep root project rules focused; put long architecture/reference material behind clear task-specific pointers when that can preserve the project's obligations. Do not delete essential constraints for a smaller number.

Pass the selected task and relevant requirement references rather than every issue and all history. Keep useful reasoning during a planning session; hand off durable records when switching tasks or executors. Use [context policy](../skills/productivity/agent-workflow/references/context-policy.md) and [model policy](../skills/productivity/agent-workflow/references/model-policy.md).
