#!/usr/bin/env node

const fs = require('fs');
const os = require('os');
const path = require('path');
const readline = require('readline');

const SOURCE_DIR = path.join(__dirname, '..', '.agents', 'skills');

const AGENTS = [
  {
    name: 'Claude Code',
    baseDir: path.join(os.homedir(), '.claude'),
    skillsDir: path.join(os.homedir(), '.claude', 'skills'),
  },
  {
    name: 'Codex CLI',
    baseDir: process.env.CODEX_HOME || path.join(os.homedir(), '.codex'),
    skillsDir: path.join(process.env.CODEX_HOME || path.join(os.homedir(), '.codex'), 'skills'),
  },
  {
    name: 'Gemini CLI',
    baseDir: path.join(os.homedir(), '.gemini'),
    skillsDir: path.join(os.homedir(), '.gemini', 'config', 'skills'),
  },
];

function listSkillDirs(dir) {
  return fs
    .readdirSync(dir, { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .map((entry) => entry.name)
    .sort();
}

function ask(rl, question) {
  return new Promise((resolve) => rl.question(question, resolve));
}

const NON_INTERACTIVE = !(process.stdin.isTTY && process.stdout.isTTY);

async function resolveOverwrite(rl, label, mode) {
  if (mode.value === 'all') return { proceed: true, mode };
  if (mode.value === 'none') return { proceed: false, mode };

  if (NON_INTERACTIVE) {
    console.log(`  "${label}" already exists — skipping (non-interactive shell; re-run in a terminal to overwrite)`);
    return { proceed: false, mode };
  }

  const answer = (await ask(rl, `  "${label}" already exists — overwrite? (y/n/all/none) `))
    .trim()
    .toLowerCase();

  if (answer === 'all') return { proceed: true, mode: { value: 'all' } };
  if (answer === 'none') return { proceed: false, mode: { value: 'none' } };
  return { proceed: answer === 'y' || answer === 'yes', mode };
}

async function installTo(agent, skills, rl, overwriteMode) {
  fs.mkdirSync(agent.skillsDir, { recursive: true });

  const installed = [];
  const skipped = [];

  for (const skill of skills) {
    const source = path.join(SOURCE_DIR, skill);
    const target = path.join(agent.skillsDir, skill);
    const exists = fs.existsSync(target);

    let proceed = true;
    if (exists) {
      const result = await resolveOverwrite(rl, `${skill} (${agent.name})`, overwriteMode);
      proceed = result.proceed;
      overwriteMode = result.mode;
    }

    if (!proceed) {
      skipped.push(skill);
      continue;
    }

    fs.rmSync(target, { recursive: true, force: true });
    fs.cpSync(source, target, { recursive: true });
    installed.push(skill);
  }

  return { installed, skipped, overwriteMode };
}

async function main() {
  if (!fs.existsSync(SOURCE_DIR)) {
    console.error(`Could not find bundled skills at ${SOURCE_DIR}`);
    process.exitCode = 1;
    return;
  }

  const skills = listSkillDirs(SOURCE_DIR);
  let detected = AGENTS.filter((agent) => fs.existsSync(agent.baseDir));

  if (!detected.length) {
    console.log('No known agent config directories detected — defaulting to Claude Code.\n');
    detected = [AGENTS[0]];
  }

  const rl = NON_INTERACTIVE ? null : readline.createInterface({ input: process.stdin, output: process.stdout });
  if (NON_INTERACTIVE) {
    console.log('Non-interactive shell detected — existing skills will be left untouched (re-run in a terminal to be prompted).\n');
  }
  let overwriteMode = { value: 'ask' };

  for (const agent of detected) {
    console.log(`Installing ${skills.length} skill(s) for ${agent.name} → ${agent.skillsDir}`);
    const result = await installTo(agent, skills, rl, overwriteMode);
    overwriteMode = result.overwriteMode;

    if (result.installed.length) console.log(`  Installed: ${result.installed.join(', ')}`);
    if (result.skipped.length) console.log(`  Skipped: ${result.skipped.join(', ')}`);
    console.log('');
  }

  if (rl) rl.close();

  console.log(`Done. Detected agents: ${detected.map((a) => a.name).join(', ')}`);
}

main();
