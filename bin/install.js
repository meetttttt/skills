#!/usr/bin/env node

const fs = require('fs');
const os = require('os');
const path = require('path');
const readline = require('readline');

const SOURCE_DIR = path.join(__dirname, '..', '.agents', 'skills');
const TARGET_DIR = path.join(os.homedir(), '.claude', 'skills');

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

async function resolveOverwrite(rl, skillName, mode) {
  if (mode.value === 'all') return { proceed: true, mode };
  if (mode.value === 'none') return { proceed: false, mode };

  const answer = (
    await ask(rl, `  "${skillName}" already exists in ~/.claude/skills — overwrite? (y/n/all/none) `)
  )
    .trim()
    .toLowerCase();

  if (answer === 'all') return { proceed: true, mode: { value: 'all' } };
  if (answer === 'none') return { proceed: false, mode: { value: 'none' } };
  return { proceed: answer === 'y' || answer === 'yes', mode };
}

async function main() {
  if (!fs.existsSync(SOURCE_DIR)) {
    console.error(`Could not find bundled skills at ${SOURCE_DIR}`);
    process.exitCode = 1;
    return;
  }

  fs.mkdirSync(TARGET_DIR, { recursive: true });

  const skills = listSkillDirs(SOURCE_DIR);
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });

  console.log(`Installing ${skills.length} skill(s) to ${TARGET_DIR}\n`);

  let overwriteMode = { value: 'ask' };
  const installed = [];
  const skipped = [];

  for (const skill of skills) {
    const source = path.join(SOURCE_DIR, skill);
    const target = path.join(TARGET_DIR, skill);
    const exists = fs.existsSync(target);

    let proceed = true;
    if (exists) {
      const result = await resolveOverwrite(rl, skill, overwriteMode);
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

  rl.close();

  console.log('');
  if (installed.length) console.log(`Installed: ${installed.join(', ')}`);
  if (skipped.length) console.log(`Skipped: ${skipped.join(', ')}`);
  console.log(`\nDone. Skills are available in Claude Code from ${TARGET_DIR}`);
}

main();
