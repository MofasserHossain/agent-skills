# Screenshot/workshop comparison

The screenshots identify a third source beyond the original two-repository audit:

[ai-engineer-workshop-2026-project at 8f1ea9b0a210caddd5f8d1749be636f7b22a9e62](https://github.com/mattpocock/ai-engineer-workshop-2026-project/tree/8f1ea9b0a210caddd5f8d1749be636f7b22a9e62).

Checked 2026-11-01 against its source files.

| Workshop source | Behavior | This kit |
|---|---|---|
| .claude/skills/grill-me/SKILL.md | Explore facts; ask one decision question at a time with a recommendation | grill uses small rounds of independent questions |
| .claude/skills/write-a-prd/SKILL.md | Resolve design/testing choices; write local issues/prd.md | write-spec writes a feature PRD at the configured location |
| .claude/skills/prd-to-issues/SKILL.md | Review vertical slices, HITL/AFK, blockers and story coverage; create numbered local Markdown issues | plan-tasks plus stable requirement labels and task metadata |
| .claude/skills/tdd/SKILL.md | Plan public behavior/tests; work one red-green slice at a time; refactor when green | implement carries proportionate test-first guidance |
| ralph/prompt.md | AFK issues only, one task per run, checks, commit, move completed issue to done/ | Current helper validates eligibility but leaves status/acceptance to supervision |
| ralph/afk.sh | Bounded Docker Sandbox loop with issue and commit context | Automated scheduling and Docker adapter remain planned |

The workshop explicitly uses local issue files; it is a different setup from the GitHub-native platform in Course Video Manager. The workshop is a useful model for a first pilot. Its CLI syntax and fixed commands should be checked against the chosen runtime and project.

The [prompt map](../prompt-map.md) checks the separate stage/runner prompt files and installation mechanisms. The workshop tracks its skills locally and aliases .agents to .claude; other inspected runners also reference globally installed skills. Neither pattern establishes a single private workspace arrangement.

Slash commands and @file references are host interaction syntax. The reusable idea is procedure plus source/context, then a reviewed artifact passed into the next stage.

The screenshots' context and token numbers are observations from that demonstration, not general model limits or proof of lower total cost. Isolated exploration can reduce parent-session context while still consuming tokens.

## Final recap supplied by the user

The user supplied a transcript of the final video segment, without a video URL or usable timestamps. This is evidence of the demonstrated intent, not a separate runtime verification. It describes a batch planner choosing parallel issues, per-issue sandbox implementation, review of produced commits, and a merger agent resolving integration/check failures. It also describes deliberate module design, explicitly supplied review standards, implementation-time documentation lookup, different implementation/review models, and QA continuously creating follow-up issues.

The [execution plan](../execution-plan.md) now includes a batch-planner proposal stage followed by deterministic eligibility checks, continuous QA feedback and distinct role context. The [QA procedure](../../skills/engineering/qa/SKILL.md) handles deduplication, reproduction, acceptance failures and rechecks. Model names from the demonstration remain examples; [model policy](../../skills/productivity/agent-workflow/references/model-policy.md) leaves provider/model choices replaceable. The transcript does not imply that this kit already has an automated runner or authority for final main-branch merges.

Our stable requirement labels replace a mandatory long user-story list. AFK execution and human review remain independent. Project rules continue to govern merge and publication.
