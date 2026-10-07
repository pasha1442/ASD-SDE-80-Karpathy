# How to publish this repository

This file is for the owner of the repository. Delete it after the first release if you want.

## 1. Put your name in the files

Replace two placeholders in the whole repository:

| Placeholder | Replace with | Files |
|---|---|---|
| `OWNER` | pasha1442 | `README.md` (done) |
| `YOUR_NAME` | Akash Parashar | `LICENSE`, `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` (done) |

Both replacements are done. To check, run this command. It must print nothing:

```bash
grep -rnE "OWNER|YOUR_NAME" README.md LICENSE .claude-plugin
```

## 2. Push to GitHub

Use the repository `pasha1442/ASD-SDE-80-Karpathy`. Then:

```bash
git init
git add .
git commit -m "STE Explain 1.0.0"
git branch -M main
git remote add origin https://github.com/pasha1442/ASD-SDE-80-Karpathy.git
git push -u origin main
```

The Claude Code install command uses the marketplace name from `.claude-plugin/marketplace.json`, and the README uses the repository name.

## 3. Test each install path

Do these tests on a clean machine or a clean project.

| Path | Command | Expected result |
|---|---|---|
| skills CLI | `npx skills add pasha1442/ASD-SDE-80-Karpathy --list` | The list shows `ste-explain` |
| Claude Code | `/plugin marketplace add pasha1442/ASD-SDE-80-Karpathy` then `/plugin install ste-explain@ste-explain-skill` | `/ste-explain` is available |
| Claude app | Upload `dist/ste-explain.zip` in Customize > Skills | The skill is in your list |
| Codex | `npx skills add pasha1442/ASD-SDE-80-Karpathy -a codex` | `$ste-explain` is available |

Then send this prompt in each tool: `Explain how DNS works. Use STE.` The answer must have short sentences and must not mention the rules.

## 4. Optional

- **GitHub Pages:** in the repository settings, set Pages to the `main` branch and the `/docs` folder. The interactive guide is then online.
- **Release:** make a release with the tag `v1.0.0` and attach `dist/ste-explain.zip`. Claude app users can then download the ZIP from the release page.
- **Listing:** the skill appears on skills.sh after people install it with the skills CLI. There is no form to fill in.

## 5. When you change the skill

1. Edit files in `skills/ste-explain/`.
2. Change `version` in `SKILL.md`, `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`.
3. Run `tools/package.sh` to build `dist/ste-explain.zip` again.
4. Commit and push.
