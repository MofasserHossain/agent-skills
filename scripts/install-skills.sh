#!/usr/bin/env bash
# Standard project-scoped Skills CLI installation; packages are prepared in the root kit.
set -euo pipefail

if [[ $# -lt 1 || "$1" == "--help" || "$1" == "-h" ]]; then
  echo 'Usage: bash scripts/install-skills.sh PROJECT [--list | --skill NAME ...] [--copy] [--yes]'
  echo 'Without --skill, choose skills interactively. Targets Claude Code and Codex in PROJECT.'
  exit 0
fi

project="$1"
shift
kit_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
package_dir="$kit_root/dist/skills"
if [[ ! -d "$project" ]]; then
  echo "Project directory does not exist: $project" >&2
  exit 2
fi
if [[ ! -f "$package_dir/.workflow-install.json" ]]; then
  echo 'Prepare the source kit first: python3 tools/package_skills.py' >&2
  exit 2
fi

selected=false
listing=false
noninteractive=false
for argument in "$@"; do
  case "$argument" in
    --skill|-s|--skill=*) selected=true ;;
    --list|-l) listing=true ;;
    --yes|-y) noninteractive=true ;;
    --global|-g|--all|--agent|-a|--agent=*)
      echo 'This wrapper targets project-local Claude Code and Codex only.' >&2
      exit 2 ;;
  esac
done
agent_environment="${CODEX_SANDBOX:-}${CODEX_CI:-}${CODEX_THREAD_ID:-}${CLAUDECODE:-}${CLAUDE_CODE:-}${AI_AGENT:-}"
if [[ "$selected" == false && "$listing" == false ]] && { [[ "$noninteractive" == true ]] || [[ ! -t 0 ]] || [[ -n "$agent_environment" ]]; }; then
  echo 'Choose skills in a normal terminal outside an agent, or pass --skill NAME ... explicitly; no skills installed.' >&2
  exit 2
fi

export DISABLE_TELEMETRY=1
export DO_NOT_TRACK=1
cd -- "$project"
exec npx --yes skills@1.7.4 add "$package_dir" --agent claude-code codex "$@"
