#!/usr/bin/env bash
# Standard project-scoped Skills CLI installation; canonical skill folders are installed directly.
set -euo pipefail

if [[ $# -lt 1 || "$1" == "--help" || "$1" == "-h" ]]; then
  echo 'Usage: bash scripts/install-skills.sh PROJECT [--list | --skill NAME ...] [--agent NAME ...] [--copy] [--yes]'
  echo 'Without --skill, choose skills interactively. Defaults to Claude Code and Codex; --agent selects Skills CLI agent targets.'
  exit 0
fi

project="$1"
shift
kit_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
skill_dir="$kit_root/skills"
if [[ ! -d "$project" ]]; then
  echo "Project directory does not exist: $project" >&2
  exit 2
fi
if [[ ! -f "$skill_dir/agent-workflow/SKILL.md" ]]; then
  echo 'Canonical skills are missing from this checkout.' >&2
  exit 2
fi

selected=false
listing=false
noninteractive=false
agents=()
cli_arguments=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    --agent|-a)
      shift
      if [[ $# -eq 0 || "$1" == -* ]]; then
        echo '--agent requires a Skills CLI agent name.' >&2
        exit 2
      fi
      while [[ $# -gt 0 && "$1" != -* ]]; do
        agents+=("$1")
        shift
      done
      continue ;;
    --agent=*)
      if [[ -z "${1#--agent=}" || "${1#--agent=}" == -* ]]; then
        echo '--agent requires a Skills CLI agent name.' >&2
        exit 2
      fi
      agents+=("${1#--agent=}") ;;
    --skill|-s|--skill=*) selected=true; cli_arguments+=("$1") ;;
    --list|-l) listing=true; cli_arguments+=("$1") ;;
    --yes|-y) noninteractive=true; cli_arguments+=("$1") ;;
    --global|-g|--all)
      echo 'This wrapper installs project-local skills; use --agent to select targets.' >&2
      exit 2 ;;
    *) cli_arguments+=("$1") ;;
  esac
  shift
done
if [[ ${#agents[@]} -eq 0 ]]; then
  agents=(claude-code codex)
fi
agent_environment="${CODEX_SANDBOX:-}${CODEX_CI:-}${CODEX_THREAD_ID:-}${CLAUDECODE:-}${CLAUDE_CODE:-}${AI_AGENT:-}"
if [[ "$selected" == false && "$listing" == false ]] && { [[ "$noninteractive" == true ]] || [[ ! -t 0 ]] || [[ -n "$agent_environment" ]]; }; then
  echo 'Choose skills in a normal terminal outside an agent, or pass --skill NAME ... explicitly; no skills installed.' >&2
  exit 2
fi

export DISABLE_TELEMETRY=1
export DO_NOT_TRACK=1
cd -- "$project"
exec npx --yes skills@1.7.4 add "$skill_dir" --agent "${agents[@]}" "${cli_arguments[@]}"
