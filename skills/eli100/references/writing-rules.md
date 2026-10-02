# Writing rules for ELI100

Working rules for this skill. They follow the public description of ASD-STE100 (nine rule groups: words, noun groups, verbs, sentences, procedures, description, safety, punctuation and word count, writing practice). They are not the text of the standard. If the official issue disagrees with this file, the official issue wins.

The checker in `scripts/check_ste.py` enforces the rows marked **check**. You enforce the rest.

## Words

- Use one part of speech and one meaning for each ordinary word.
- A **technical noun** is a name the project already uses: a part, a tool, an API, a file, a command. Keep it. Do not turn it into a verb.
- A **technical verb** is an industry action that no simple verb already covers (`drill`, `ream`). Keep it only in that case. Do not turn it into a noun.
- When the project has an official name, use that name. Do not invent a shorter synonym for the same part.
- Pick a short name (three words or fewer) when you must name something new.
- No slang, and no word that only one site would know.
- Full mode: American spelling, unless the source text is a quote or a label that the product shows.

## Noun groups

- A noun group is a row of nouns and adjectives with no word such as `of` or `for` between them. Keep it to three words.
- `primary hydraulic pump` is three words. `primary hydraulic system pump` is four. Write `primary pump for the hydraulic system`.
- If the official name is longer than three words, write it in full once. After that, use a short name. You may join closely related words with a hyphen so the group reads as three words or fewer. Do not change a hyphen that is already part of the official name.

## Verbs

Use only these forms:

- infinitive (`to remove`)
- imperative (`Remove the cover.`)
- simple present (`The pump sends fluid.`)
- simple past (`The test failed.`)
- simple future (`The valve will open.`)
- past participle as an adjective (`the removed cover`, `the cover is open` when `open` is the state)

Do not use:

- perfect (`has removed`)
- progressive (`is removing`) **check**
- a contraction (`don't`) **check**
- a noun where a verb can carry the action (`before the removal of` → `before you remove`)

**check** Active voice in a procedure and in a safety text. In a description, passive only when you cannot name who did the action. Prefer to name the agent.

## Sentences

- Short, and one topic.
- Do not drop the subject, the verb, or an article to save words.
- No semicolon. **check** Write two sentences.
- A colon before a list ends the lead-in. The lead-in and each list item obey the word limit.
- Tie the next sentence to the previous one when the link is not obvious: `and`, `but`, `then`, `thus`, `as a result`, `at the same time`.
- Put `a`, `an`, `the`, `this`, or `these` before a noun when the noun needs it. Do not put `the` before a name that already has an identifier (`pump P-101`).

## Procedures

- **check** Word limit: 20 full, 25 soften.
- One instruction in each sentence. Two instructions in one sentence only when the reader does them at the same time.
- Imperative, to the reader.
- A condition comes first, then a comma, then the command: `When the lamp is on, release the button.`
- A note gives information. A note does not give a command, a limit, or a result. Put the limit in the step.
- **check** Do not write `you must` in front of a command, except inside a safety condition.

## Description

- **check** Word limit: 25 full, 31 soften.
- One topic in each sentence. Add the next fact in the next sentence.
- The first sentence of a paragraph states the topic. The other sentences stay on that topic.
- **check** At most six sentences in a paragraph. Start a new paragraph for the next topic.

## Safety

- **check** Word limit: same as a procedure.
- `Warning`: injury or death. `Caution`: damage to equipment, tools, or material. If both risks are present, write `Warning`.
- First sentence: the command, or the condition the reader must know.
- Next sentence, when you can say it: the specific result if the reader does not obey.

## How the checker counts words

This matches the public counting method closely enough to enforce the limits. It is still an approximation.

- A hyphenated group counts as one word (`off-the-shelf`).
- A number plus its unit counts as one word (`12 mm`).
- A URL, a quoted block, or the whole text inside one pair of parentheses counts as one word.
- A colon, a period, a question mark, or an exclamation mark ends a sentence.
- Text in a fenced code block, inline code, and a Markdown heading is not counted.

## Practice

- If a one-word swap loses the meaning or breaks grammar, rewrite the sentence.
- Do not add a particle that creates a new meaning (`carry out` for `do`, `figure out` for `find`). A particle that keeps its own meaning is fine (`Put the cover on the box.`).
- Use the same sentence pattern for the same kind of step. Do not vary the wording for style.
