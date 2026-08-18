# MN-Skills — AI Coding Agent Skills Library

A collection of project-agnostic, vendor-neutral skills for AI coding agents — `grill-me`, `prd-frd`, `clickup`, `implement`, `smoke-test`, `ship`, and `repository-audit`. Works across Claude Code, Gemini CLI, Codex, Cursor, Windsurf, and any agent that reads markdown instructions.

See [`.agents/skills/README.md`](.agents/skills/README.md) for the full skill index, workflow chain, and detailed docs per skill.

## Install for Claude Code

```bash
npx mn-skills
```

This copies every skill into `~/.claude/skills/`, where Claude Code discovers them automatically. If a skill with the same name already exists there, you'll be prompted before it's overwritten.

No install script, no dependencies — the installer is a small zero-dependency Node script bundled in this package.

## Updating

Re-run `npx mn-skills` any time to pick up newer versions of the skills. You'll be prompted per-skill (or choose "all"/"none") before anything already installed is overwritten.

## License

MIT
