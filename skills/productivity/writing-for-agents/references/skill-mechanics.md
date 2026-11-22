# Skill mechanics

The skill-specific branch of writing for agents: naming, frontmatter, body shape, collaborators and metadata.

## Name

A skill's name is its first leading word: what the user types and what the agent reads. Choose the word people already say, and let the shape of the name tell its role:

- **Converters** turn one artifact into the next and start with `to-`: `to-brief`, `to-spec`, `to-tasks`.
- **Actions** are verbs: `implement`, `research`, `prototype`, `handoff`.
- **Disciplines** that other skills reuse are nouns or gerunds: `ui-design`, `writing-for-agents`.
- **Commands the user speaks** can use the first person: `grill-me`.
- **Kit entry points** name what they give you: `next-step`, `setup-<kit>`.
- Established short forms stay short: `qa`, `pr`.

Use one term per concept across names, bodies and templates; when the project has a glossary, use its words. The folder name, the `name` field and every reference must match. A rename is a migration: record the old name wherever installers and docs map old names to new ones.

## Frontmatter

- `name`: lowercase letters, digits and hyphens, equal to the folder name.
- `description`: the always-loaded pointer. Leading word first, then "Use when …" with one phrase per distinct trigger, in one or two sentences.
- Explicit-only invocation (for example Claude Code's `disable-model-invocation`) removes the description from automatic context, and also stops automatic and skill-to-skill use. Treat it as a deliberate host-local choice, not a portable default.

## Body shape

A purpose line with the skill's leading words → an optional one-line **Why** where misuse is likely → `## Process` with numbered steps, each ending "Done when:" → reference sections → branch files in `references/` or `templates/`. A skill that only sequences other skills can be a few lines; put depth in the discipline that many skills reuse.

## Collaborators

Name another skill by its installed name in backticks and say when to use it: "Invoke the `research` skill for a factual gap." Say what happens when it is absent: continue where this procedure suffices, or report the missing guidance; never claim it ran. Never link into another skill's folder, because installed skills move independently.

## Resources

Keep every file the skill needs inside its own folder, linked relatively. A template describes output shape; it doesn't repeat the process.

## Codex metadata

`agents/openai.yaml` holds `interface.display_name`, `short_description` (this kit validates 25–64 characters) and `default_prompt`, which must invoke the skill as `$<name>`. The metadata labels the skill in a picker; `SKILL.md` owns behavior.

## Router skills

When there are too many skills to remember, one router names the others and when to reach for each. It hints at the route; each named skill still owns its own procedure.
