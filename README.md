# ASD-SDE-80-Karpathy

**Clear AI answers in one step.** ASD-SDE-80-Karpathy Explain is an agent skill that makes your AI assistant write like an aircraft maintenance manual: short sentences, plain words, one idea in each sentence. It can also research a topic on the web first, and then give the explanation as a diagram, an interactive page with animated diagrams and source links, or a silent video.

It works in Claude, Claude Code, Codex, ChatGPT, Cursor and other tools that read the open [Agent Skills](https://agentskills.io) format.

https://github.com/user-attachments/assets/cb9c9235-d517-42bd-8e5e-bd37977bb426

## Why

People now spend more time reading AI output than writing prompts. In October 2026, Andrej Karpathy shared a tip: ask the model to explain things in **ASD-STE100**, the controlled English that the aerospace industry made for maintenance manuals. He also suggested "80% of the way", because the full standard is very strict.

This skill packs that tip so that you do not type it each time. It also adds what the tip needs to be safe:

- **It keeps the facts.** Strict STE prompts can remove technical terms and the facts that go with them. The skill tells the model what it must never lose, and a checker script finds lost facts.
- **It knows when to stop.** The skill does not use STE for stories, marketing or personal writing.
- **It goes further than text.** The same skill makes a diagram, an interactive HTML page or a silent Manim video.

## Install

The repository is `pasha1442/ASD-SDE-80-Karpathy`.

### Any agent, one command

```bash
npx skills add pasha1442/ASD-SDE-80-Karpathy
```

The [skills CLI](https://github.com/vercel-labs/skills) asks which agent you use and installs the skill there. Add `-g` to install it for all your projects.

### Claude Code (plugin)

```
/plugin marketplace add pasha1442/ASD-SDE-80-Karpathy
/plugin install ste-explain@ste-explain-skill
```

### Claude app (web, desktop, mobile)

1. Download [`dist/ste-explain.zip`](dist/ste-explain.zip).
2. In Claude, open **Customize > Skills**.
3. Select **+**, then **Create skill**, then **Upload a skill**.
4. Upload the ZIP file.

Code execution must be on in your settings, because the skill includes a script.

### Codex

```bash
npx skills add pasha1442/ASD-SDE-80-Karpathy -a codex
```

Or copy the folder `skills/ste-explain` to `~/.agents/skills/` (all projects) or to `.agents/skills/` in a repository. Type `$ste-explain` to call the skill.

### ChatGPT

- **With Skills** (desktop app): add the folder `skills/ste-explain` in the Skills panel. Type `@` and select **STE Explain**.
- **Without Skills** (all plans): paste [`chatgpt/custom-instructions.txt`](chatgpt/custom-instructions.txt) into your custom instructions. It fits the 1,500-character limit. For the full version, paste [`chatgpt/project-instructions.md`](chatgpt/project-instructions.md) into the instructions of a Project or a custom GPT.

The menus in ChatGPT change often. If a menu name is different, see the OpenAI help pages.

### Cursor, Windsurf, Gemini CLI and others

Use the `npx skills add` command above. For a tool with no skill support, paste [`snippets/agents-rule.md`](snippets/agents-rule.md) into its rules file (`AGENTS.md`, `CLAUDE.md`, `.cursorrules`).

## Use

Ask in your own words. The skill starts when you ask for a clear answer or name STE.

| You type | You get |
|---|---|
| `Explain how DNS works. Use STE.` | A short, clear explanation |
| `This is too wordy. Make it easier to read.` | The same content in short sentences |
| `Rewrite this error message so that nobody can misread it: ...` | Only the rewritten text |
| `Rewrite this tool description in strict STE: ...` | Text for an AI agent, with all rules applied |
| `Explain the OAuth code flow as a diagram.` | A Mermaid diagram and one sentence for each arrow |
| `Make an interactive page that explains compound interest.` | One HTML file with a control that you can change |
| `Make a 90-second silent video that explains binary search.` | A Manim script and an MP4 |
| `How do vaccines train the immune system?` (a topic only) | The skill searches the web first, then answers with source links |
| `Check this text against STE: ...` | A list of findings |

In Claude Code you can also call it by name: `/ste-explain how does a JWT work`. If you installed it as a plugin, the name is `/ste-explain:ste-explain`.

### The eight modes

| Mode | For |
|---|---|
| `research` | Web research on a topic. It runs first when you give only a topic, and it feeds all other modes |
| `explain` | Answers, summaries, explanations (default) |
| `rewrite` | Your own text, made clearer |
| `strict` | Text that a program or an AI agent reads |
| `diagram` | A diagram that you can check |
| `page` | An interactive HTML explainer with animated diagrams and a list of source links |
| `video` | A silent animated explainer |
| `check` | Findings from the checker script |

## The checker

`ste_check.py` is a small Python script with no dependencies. The skill runs it when the agent can run code. You can also run it yourself.

```bash
python skills/ste-explain/scripts/ste_check.py README.md          # style findings
python skills/ste-explain/scripts/ste_check.py --compare old.md new.md   # lost facts
python skills/ste-explain/scripts/ste_check.py --selftest
```

- **Style findings:** long sentences, long paragraphs, semicolons, filler phrases, formal words, phrasal verbs, nouns used for verbs. Passive voice and compound tenses are advisory.
- **Lost facts:** numbers, identifiers, code and file names that are in the source and not in the rewrite. It also counts words such as "may", "unless" and "not".

The exit code is 1 when there are hard findings, so you can use the script in CI.

## What "80%" means

| The skill applies | The skill relaxes |
|---|---|
| One idea in each sentence | Technical terms stay, even if the STE dictionary does not have them |
| 20 words for an instruction, 25 for a description | Connecting words stay: because, so, but, then |
| Active voice, simple tenses | A compound tense stays when it carries meaning ("may have failed") |
| One name for one thing | One sentence can be longer if a split would separate a condition from its result |
| Plain words, no filler, no semicolons | |

Why not 100%? In one public test of code explanations, a strict "ASD-STE100" prompt lost 46.8% of the scored facts. A looser "Simple Technical English" prompt lost 8.5%. The test was small and informal, but the cause is clear: the dictionary has no words for most software ideas.

## Limits

- **This is not a certified STE tool.** The skill does not contain the official ASD-STE100 dictionary, which is copyrighted. For real aircraft, defence or safety documents, use the [official standard](https://www.asd-ste100.org/).
- **A prompt is a request, not a guarantee.** A model can write text that looks like STE and still breaks a rule. The checker finds patterns. It does not prove that a rewrite kept the meaning.
- **A clear answer can be incorrect.** Before you use an answer, check one important fact against the source.
- **The answer does not always get shorter.** STE makes sentences shorter. If you want a shorter answer, ask for one.

## What is in this repository

```
skills/ste-explain/
  SKILL.md                      the skill: modes, rules, process
  references/ste-rules.md       fuller rules, verb forms, strict mode
  references/diagram.md         diagram mode
  references/html-page.md       page mode
  references/video.md           video mode
  references/research.md        research mode: search, check and cite sources
  scripts/ste_check.py          the checker
  assets/explainer-template.html
  assets/manim_template.py
  agents/openai.yaml            display name for Codex and ChatGPT
.claude-plugin/                 plugin and marketplace files for Claude Code
chatgpt/                        instructions to paste into ChatGPT
snippets/agents-rule.md         a short rule for AGENTS.md or CLAUDE.md
examples/before-after.md        five worked examples
evals/evals.json                test prompts for people who change the skill
docs/                           an interactive guide, the explainer video
dist/ste-explain.zip            the skill as a ZIP for the Claude app
```

## Learn the technique

[`docs/index.html`](docs/index.html) is an interactive guide: a step-by-step rewrite, a rule explorer, a text checker in the browser and a decision flow. [`docs/ste100-explainer.mp4`](docs/ste100-explainer.mp4) is a silent animation of the same technique. It is the video at the top of this page.

## Contribute

1. Change the skill.
2. Run `python skills/ste-explain/scripts/ste_check.py --selftest`.
3. Try the prompts in `evals/evals.json` with and without the skill, and compare the answers.
4. Run `tools/package.sh` to build the ZIP again.
5. Open a pull request.

If you find a rule here that does not agree with the official standard, open an issue and quote the rule number.

## Credits

- [Andrej Karpathy](https://x.com/karpathy/status/2105819303471976479) for the tip.
- ASD and the Simplified Technical English Maintenance Group for the [standard](https://www.asd-ste100.org/).
- [Max Nardit](https://max.nardit.com/articles/karpathy-understanding-llm-outputs) for the review that found the errors in a popular cheat sheet.
- [Lucian Ghinda](https://allaboutcoding.ghinda.com/explain-to-me-in-simple-technical-english/) for the test of lost facts.
- Related skills with a different focus: [danyuchn/asd-ste100-skill](https://github.com/danyuchn/asd-ste100-skill) and [AminBlg/SimpleEnglish](https://github.com/AminBlg/SimpleEnglish).

This project is not affiliated with ASD, Anthropic or OpenAI.

## License

[MIT](LICENSE)
