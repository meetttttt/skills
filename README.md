# MN-Skills — AI Coding Agent Skills Library

A collection of project-agnostic, vendor-neutral skills for AI coding agents — `grill-me`, `prd-frd`, `clickup`, `implement`, `smoke-test`, `ship`, `code-review`, `hipaa-compliance`, `software-effort-estimation`, and `document-generation`. Works across Claude Code, Gemini CLI, Codex, Cursor, Windsurf, and any agent that reads markdown instructions.

See [`.agents/skills/README.md`](.agents/skills/README.md) for the full skill index, workflow chain, and detailed docs per skill.

## Install

```bash
npx mn-skills
```

(or `npx github:meetttttt/skills`, which works the same way without depending on the npm registry)

No cloning required — `npx` fetches the package into a temp cache and runs it. The installer auto-detects which of these are present on your machine and installs into each:

| Agent | Install location |
|---|---|
| Claude Code | `~/.claude/skills/` |
| Codex CLI | `$CODEX_HOME/skills/` (defaults to `~/.codex/skills/`) |
| Gemini CLI | `~/.gemini/config/skills/` |

If none are detected, it defaults to Claude Code. If a skill with the same name already exists at a target, you'll be prompted before it's overwritten (or choose "all"/"none" to apply to the rest of the run).

No install script, no dependencies — the installer is a small zero-dependency Node script bundled in this package.

## Updating

Re-run the same command any time to pick up newer versions of the skills. You'll be prompted per-skill (or choose "all"/"none") before anything already installed is overwritten.

## License

MIT
