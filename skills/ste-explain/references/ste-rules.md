# STE rules: the fuller reference

Read this file for `strict` mode, or when you need more detail than `SKILL.md` gives.

## Contents

- What ASD-STE100 is
- The limits
- Words
- Verbs
- Sentences and paragraphs
- Procedures
- Descriptions
- Safety instructions
- Strict mode
- What this skill cannot check
- Sources

## What ASD-STE100 is

ASD-STE100, Simplified Technical English, is a controlled language. European airlines asked for it in 1979 because many mechanics read English as a second language. The first guide appeared in 1986. ASD, the European aerospace and defence association, maintains it. Issue 9 (January 2025) is the current issue.

The standard has two parts:

1. **Writing rules.** 53 rules in nine sections: words, multi-word nouns, verbs, sentences, procedural writing, descriptive writing, safety instructions, punctuation and word counts, writing practices.
2. **A dictionary.** About 900 approved words, each with one meaning and one part of speech. About 1,200 more words are listed as not approved, each with an approved alternative. A writer can add technical nouns and technical verbs for the subject.

The standard is free to request from asd-ste100.org. It is copyrighted, so this skill does not include the dictionary.

## The limits

| Limit | Applies to |
|---|---|
| 20 words | A sentence in a procedure |
| 25 words | A sentence in a description |
| 6 sentences | A paragraph |
| 3 words | A multi-word noun ("fuel pump valve") |
| 1 instruction | Each sentence, unless the actions occur at the same time |

## Words

- Use a word with one meaning only. In the standard, "close" is a verb ("Close the valve"). It is not an adjective that means "near".
- Use one name for one thing in the whole text.
- Prefer the common word. Pairs that the standard lists:

  | Not approved | Approved |
  |---|---|
  | commence | start |
  | prior to | before |
  | ensure | make sure |
  | utilize | use |
  | replenish | fill |

- Plain-English preferences that are good practice, but that this skill has not checked against the dictionary: in order to → to, subsequently → then, facilitate → help, leverage → use, numerous → many, sufficient → enough.
- Known traps. Popular summaries get these wrong:
  - "approximately" is approved. "about" is approved only with the meaning "concerned with". Write "Wait for approximately 10 minutes".
  - "test" is approved as a noun only. Write "Do a test of the circuit", not "Test the circuit".
- Keep each technical term that the subject needs. Define it once if the reader may not know it.

## Verbs

| Form | Example | Use it? |
|---|---|---|
| Command | Close the valve. | Yes |
| Simple present | The valve closes. | Yes |
| Simple past | The valve closed. | Yes |
| Simple future | The valve will close. | Yes |
| Infinitive | Turn the knob to close the valve. | Yes |
| Past participle as an adjective | the closed valve | Yes |
| Progressive (-ing) | The valve is closing. | No |
| Perfect | The valve has closed. | No |
| Passive in a procedure | The valve must be closed. | No |

- Use the -ing form only as part of a technical noun, for example "landing gear".
- Use the verb for an action, not a noun made from the verb: "Adjust the cable", not "Make an adjustment to the cable".
- Do not make a phrasal verb when one plain verb exists: "start", not "spin up"; "remove", not "take off".
- 80% relaxation: keep a perfect or modal form when the simple form changes the meaning. "The job has finished" (and its output is ready now) is not the same as "The job finished".

## Sentences and paragraphs

- One topic in each sentence.
- Do not leave out words to make a sentence shorter. Keep the subject, the verb and the articles.
- Use a vertical list for three or more items, conditions or steps.
- Do not use a semicolon. All other standard punctuation is permitted.
- One topic in each paragraph. Start the paragraph with the topic sentence.

## Procedures

- Write each step as a command: "Remove the panel."
- One instruction in each sentence, unless two actions occur at the same time: "Hold the lever and push the button."
- Put the condition before the action: "If the pressure is low, open the valve."
- Number the steps when the sequence is important.

## Descriptions

- Give information in small steps, from what the reader knows to what is new.
- Use the active voice. Use the passive only when you do not know who or what does the action.

## Safety instructions

- Use WARNING for a risk of injury to a person. Use CAUTION for a risk of damage to equipment or data.
- Put the safety instruction before the step that it applies to.
- Start with a clear command. Then give the risk: "WARNING: Do not touch the brake unit until it is cool. Hot parts can cause injury."

For software, the same pattern applies to data loss: "CAUTION: Make a backup before you run this command. The command deletes all rows in the table."

## Strict mode

Use strict mode for text that a program or an AI agent reads with no person to resolve a doubt: tool descriptions, error messages, system prompts, instructions between agents, runbook steps.

- Apply every limit with no exceptions for length.
- Say who does each action. In a tool description, the actor is "the tool" or "the caller", never an unclear "it".
- Use exactly one term for each parameter, state and component. Use the identifier from the code.
- State each condition and each default value.
- An error message has three parts in this sequence: what occurred, the probable cause (with "may" if it is not certain), and what to do next.
- Run `scripts/ste_check.py --limit 20` and fix every hard finding.

## What this skill cannot check

- It cannot check words against the official dictionary.
- The checker script finds patterns. It does not prove that a text obeys the standard, and it does not prove that a rewrite kept the meaning.
- Models tend to think that they obey a style rule more than they do. Treat the model's own claim of compliance as unverified.

## Sources

- ASD-STE100 official site: https://www.asd-ste100.org/
- Simplified Technical English, Wikipedia: https://en.wikipedia.org/wiki/Simplified_Technical_English
- Andrej Karpathy's post that suggested the technique (2 October 2026): https://x.com/karpathy/status/2105819303471976479
- Max Nardit, review of the technique and of a popular cheat sheet: https://max.nardit.com/articles/karpathy-understanding-llm-outputs
- Lucian Ghinda, test of lost facts in code explanations: https://allaboutcoding.ghinda.com/explain-to-me-in-simple-technical-english/
