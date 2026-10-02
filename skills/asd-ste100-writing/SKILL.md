---
name: asd-ste100-writing
description: >-
  Rewrites plans, specs, procedures, how-tos, and decision notes into
  constrained English in the spirit of ASD-STE100 Simplified Technical English
  (ELI100). Default mode is about 80 percent of those limits. Applies the full
  sentence, verb, and safety limits when the user asks for strict STE100,
  ASD-STE100, or full ELI100. Use when the user asks to simplify, rewrite, or
  check technical English, STE, STE100, ELI100, simplified technical English,
  or controlled language. Not the official ASD dictionary.
license: MIT
metadata:
  author: daniellinuk
  version: "1.0.0"
---

# ELI100

Rewrite technical text so a person can check it in one pass. The style follows the public writing rules of ASD-STE100 (Simplified Technical English). This skill is not the standard, not the STE dictionary, and not a certification. ASD owns ASD-STE100. When a text must comply, use the official issue from [asd-ste100.org](https://www.asd-ste100.org/).

## When to use

Use this skill for a plan, spec, procedure, how-to, decision note, or other technical prose.

Do not use it for casual chat, social posts, or a warm 1:1 reply unless the user asks. Do not rewrite code, quotes, UI labels, or product names.

## Mode

- **soften** (default): about 80 percent of the STE limits. Same structure. Longer sentences. Do not reject a word because it might be outside the dictionary.
- **full**: the user says strict STE100, ASD-STE100, or full ELI100, or the text is a procedure that must not be ambiguous. Use the short sentence limits. Replace the published non-approved examples in [word-choice.md](references/word-choice.md). If you do not know the approved meaning, use a simpler everyday word, or keep a real technical noun and do not call it approved.

## Steps

1. Classify the text.
   - **procedure** — steps the reader does
   - **description** — how something works, a plan, a spec, a decision
   - **safety** — injury or equipment damage
   - A plan that also has steps: treat the steps as a procedure and the rest as a description. Check each part with its own `--kind`.
2. Read [writing-rules.md](references/writing-rules.md). Read [word-choice.md](references/word-choice.md) before you change words. Read [examples.md](references/examples.md) if the shape is unclear.
3. Rewrite. Keep the meaning. Do not add filler. One idea in each sentence.
4. Run the checker from this skill folder. Fix every ERROR. In full mode, also fix each WARN that names a replacement. Run the checker again. Stop when it prints `OK`, or when only WARNs remain that would change the meaning.

```bash
python3 scripts/check_ste.py --mode soften --kind description -- path/to/draft.md
```

`--mode` is `soften` or `full`. `--kind` is `procedure`, `description`, or `safety`. Omit the file to read stdin.

The checker counts words, contractions, semicolons, progressive verbs, and passive voice. It does not know the STE dictionary. You still judge meaning.

5. Return the rewrite. In full mode, add one sentence: this draft was not checked against the official STE dictionary.

## Shape for a plan or a spec

First sentence: the decision or the outcome. Then, in this order:

- Context, only what the reader needs
- Decision or plan
- Steps, or checks that show the work is done
- Out of scope

## Rules that always apply

- Active voice. Name who does the action.
- One instruction in one sentence, unless the actions happen together.
- Keep the subject, the verb, and the articles (`a`, `an`, `the`).
- No contraction. No semicolon.
- A noun group has at most three words (`hydraulic pump cover`). Break a longer group with `of`, `for`, `on`, or `in`.
- Use a vertical list when a sentence would hold many items or many actions.
- Same name for the same thing each time.
- Commands in a procedure: `Open the valve.` Not `You must open the valve.`
- Safety: start with `Warning` (injury or death) or `Caution` (damage). If both, use `Warning`. Put the command or the condition first. Then say what happens if the reader does not obey.

## Word limits

| Kind | soften | full |
| --- | --- | --- |
| procedure, safety | 25 words | 20 words |
| description | 31 words | 25 words |

Soften is one quarter longer than the public STE limits (20 and 25), rounded to the nearest word. A description paragraph has at most six sentences.

## After the rewrite

If the reader still cannot use the text, offer one follow-on. Do not do it in the same reply unless the user asks: a diagram, a short HTML explainer, or a short video explainer.
