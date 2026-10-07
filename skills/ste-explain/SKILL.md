---
name: ste-explain
description: Writes explanations, summaries, instructions and rewrites in clear "80% ASD-STE100" Simplified Technical English (short sentences, plain words, active voice, one idea per sentence), and explains a topic as a labelled diagram, an interactive HTML page or a silent Manim explainer video. Use when the user mentions STE, ASD-STE100, Simplified Technical English or the Karpathy STE tip; asks for a clearer, plainer, simpler or easier-to-read answer; says an answer is too wordy, dense or hard to follow; asks to rewrite instructions, error messages, tool descriptions, prompts or docs so that nobody can misread them; or asks to explain or visualize something as a diagram, as an interactive page or as an explainer video, or gives only a topic to learn about and needs researched facts with source links. Not for creative, marketing or personal-voice writing.
license: MIT
metadata:
  version: "1.1.0"
---

# STE Explain

People now spend more time reading AI output than writing prompts. This skill makes that output cheap to read and safe to trust. It borrows the discipline of ASD-STE100 (Simplified Technical English), the controlled English that aircraft maintenance manuals use so that a mechanic reads each instruction correctly the first time.

The target is **80% of the way to ASD-STE100**, not the full standard. The full standard removes words that software and science need, and a model that follows it too strictly drops facts. Section 3 says what must never be lost.

## 1. Pick the mode

| The user wants | Mode | What to do |
|---|---|---|
| Only a topic or a question about the world, with no source text | `research` | Read `references/research.md`. Search the web first, then continue in the mode below. |
| An explanation, answer or summary (default) | `explain` | Write with the rules in section 2. |
| Their own text made clearer | `rewrite` | Sections 2 and 3. Return the rewritten text only. |
| Text that a program or another AI agent reads: tool description, error message, system prompt, runbook step | `strict` | Section 2 with no relaxations. Read `references/ste-rules.md`. |
| "as a diagram", "draw it", "visualize" | `diagram` | Read `references/diagram.md`. |
| "as a page", "in HTML", "interactive" | `page` | Read `references/html-page.md`. |
| "as a video", "animate it", "3b1b style" | `video` | Read `references/video.md`. |
| "check this", "is this STE?" | `check` | Run `scripts/ste_check.py` and report the findings. |

If the user gives only a topic, run `research` first and then use `explain`. Skip `research` when the user gives the source text, says "no research", or when the surface has no web tools. In that case say in one sentence that the facts are not checked, and do not add source links. Do not ask which mode they want unless the request is truly unclear. The modes combine: "explain X, then draw it" is `explain` followed by `diagram`. For `diagram`, `page` and `video` about a factual topic, run `research` first and use its fact list.

**The short rules for the three formats.** The reference files give the details. If you cannot open a reference file, use these rules. Do not tell the user that a file was not available. The user asked for the answer, not for a report about this skill.

- `research`: Make a list of 3 to 6 questions. Search for each one. Open each page that you cite. Cite only pages that you opened, and copy each URL exactly. Never invent a source. Say when sources disagree or when you found only one.
- `diagram`: Use Mermaid in a code block. If the surface cannot show Mermaid, draw the diagram with text characters. Maximum 12 nodes. Put a verb on every arrow. Below the diagram, write one numbered STE sentence for each arrow, so that the reader can check each connection.
- `page`: Give one self-contained HTML file with all CSS and JavaScript inline. Include an animated diagram, at least one control that changes an assumption and shows the result, a visible list of assumptions, and a "Sources" section with real links from the research. All text on the page follows section 2.
- `video`: Write a storyboard of 6 to 9 scenes first, one sentence for each scene. Then write a Manim script that uses `Text` only (no LaTeX), 60 to 120 seconds, silent. Give the script with the video.

## 2. The writing rules

Each rule removes one cause of wrong reading. Apply them in this order when you edit a sentence.

1. **Delete words that say nothing.** No "It is important to note that", no "basically", no praise for the question, no summary of what you are about to say. Start with the content.
2. **One idea in each sentence.** An instruction sentence gives one action. If a sentence has "and" between two actions, make two sentences. Exception: two actions that occur at the same time.
3. **Keep sentences short.** Maximum 20 words for an instruction. Maximum 25 words for a description. Maximum 6 sentences in a paragraph, and one topic in a paragraph.
4. **Use the active voice and name the actor.** Write "The script deletes the file", not "The file is deleted". Start an instruction with the verb: "Open the file."
5. **Use simple tenses.** Write "The server receives the request", not "is receiving" or "has received". Keep a compound tense only when the simple tense changes the meaning, for example "may have failed".
6. **Use one word for one thing.** Give each thing one name and use that name every time. If you call it "the worker", do not call it "the agent" or "the process" later. The reader cannot know that three names mean one thing.
7. **Use the plain word.** Prefer the short, common word. Some pairs from the standard: commence → start, prior to → before, ensure → make sure, utilize → use, replenish → fill. Two common mistakes: "approximately" is an approved word (do not change it to "about"), and "test" is a noun only ("Do a test of the circuit").
8. **Use the verb, not the noun made from it.** Write "Analyze the log", not "Perform an analysis of the log".
9. **Stack a maximum of three nouns.** Write "the email template for a password reset", not "the user account password reset email template".
10. **Keep the small words.** Do not remove "the", "a" or "this" to save space. "Check log, restart service" is harder to read than "Check the log. Restart the service."
11. **Do not use semicolons.** Write two sentences.
12. **Write procedures as numbered steps.** One action in each step. Put the condition first: "If the light is red, stop the pump." Put a warning before the step it applies to, and give the command first, then the risk.

**What "80%" relaxes.** Keep the connecting words that show how ideas relate: because, so, but, then, for example. Without them the text reads like a parts list. You may let one sentence go over the limit when a split would separate a condition from its result. You may use any technical term the subject needs. The first sentence of an answer may be a little more natural than the rest.

## 3. Never lose these

Short sentences are worth nothing if a fact disappears. In one public test, a strict "ASD-STE100" prompt lost almost half of the scored facts in code explanations, and a looser "Simple Technical English" prompt lost under a tenth. The losses came from technical terms that the model explained away. So:

- **Technical terms, identifiers, product names, code, file paths, commands:** keep them exactly as written. If the reader may not know a term, explain it once in a short sentence. Do not replace it.
- **Numbers, units, versions, limits and dates:** keep every one.
- **Conditions and exceptions:** keep each "if", "unless", "only when", "except" and "not".
- **Uncertainty:** keep "may", "might", "can", "probably" and "not verified" at the same strength. "The request may have failed" and "The request failed" are different claims.
- **In `rewrite` mode, add nothing.** Do not add a cause, a number or an example that the source did not give.

## 4. Process

1. Read the content for meaning first. Note the facts, terms, numbers and conditions that must survive.
2. Write or rewrite with the rules in section 2.
3. Check your draft against this list:
   - Is each sentence within its limit, with one idea?
   - Is each thing called by one name from start to end?
   - Are all terms, numbers, conditions and hedges from step 1 still there?
   - Did a passive sentence hide who does the action?
4. If you can run code and `scripts/ste_check.py` is present, and the text is long or the mode is `strict` or `rewrite`, run the checker:
   ```bash
   python scripts/ste_check.py draft.md                 # style findings
   python scripts/ste_check.py --compare source.md draft.md   # facts that went missing
   ```
   Fix every hard finding. Use your judgment on advisory findings. See `python scripts/ste_check.py --help` for options.
5. Deliver the result.

## 5. Output

- After research, end an `explain` answer with a numbered "Sources" list (title, site, full URL) and put the number in brackets after each key claim.
- Give the answer itself. Do not write a sentence about this skill, about STE or about the rules, unless the user asks.
- Use light Markdown: a numbered list for a procedure, a table for a comparison, a code block for code. Do not change text inside code blocks.
- In `rewrite` mode, return only the rewritten text. Two short notes are permitted after the text, each on one line, and only when they apply:
  - `Kept as written: <phrase> (<reason>)` for a phrase that you left long on purpose.
  - `Unclear in the source: <what>. I used this reading: <reading>.` when the source has two possible meanings. Do not guess silently, and do not write a paragraph about it.
- If the user asks what changed, give a three-column table: rule, original, rewrite.
- STE makes sentences shorter. It does not always make answers shorter. Do not pad the answer, and do not cut facts to make it short.

## 6. Say what this is, and what it is not

- Call the result "STE-style" or "80% STE". Do not say that a text complies with ASD-STE100. This skill does not contain the official dictionary, and only a check against the standard can show compliance.
- For real aircraft, defence or safety documentation, tell the user to use the official standard from asd-ste100.org and a qualified reviewer.
- A clear answer can be incorrect. Do not let short, confident sentences hide a doubt. If you are not sure, say so in a short sentence.
- A source link shows where a claim came from. It does not prove that the claim is true. Say so when the sources are weak or disagree.

## 7. When not to use this skill

Do not use STE for stories, poems, marketing copy, speeches, personal messages, or text that must sound like the user. Do not use it for a legal text where the exact words matter. If the user asks for a natural or warm voice, give them that. In a mixed document, use STE for the reference parts and a natural voice for the introduction.

## Files

These files are present when the skill is installed from the repository or from the ZIP file. If they are not present, sections 1 to 7 are sufficient.

- `references/ste-rules.md`: the fuller rule set, verb forms, safety instructions and `strict` mode.
- `references/research.md`: how to search, check and cite sources.
- `references/diagram.md`: how to explain with a diagram that the reader can check.
- `references/html-page.md`: how to build an interactive explainer page. Template: `assets/explainer-template.html`.
- `references/video.md`: how to make a silent Manim explainer video. Template: `assets/manim_template.py`.
- `scripts/ste_check.py`: a checker for the mechanical rules and for lost facts. Standard library only.
