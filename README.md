# ELI100

Explain it like STE100.

You know [ELI5](https://www.reddit.com/r/explainlikeimfive/): explain it like the reader is five. ELI100 is that same favor for a grown-up who has a spec open and no patience for fog. The 100 is [ASD-STE100](https://www.asd-ste100.org/), Simplified Technical English. Five gets a story. One hundred gets a sentence you can check.

ELI100 is a writing skill for coding agents. Hand it a plan, a spec, a procedure, or a decision note. You get short sentences, one idea each, and words that say what actually happens.

Everyday ELI100 is about 80 percent of those limits, so the page stays human. Ask for full ELI100 when a procedure must not be ambiguous.

This is not the official STE dictionary, and it is not an ASD certification. ASD owns the standard. If a document has to comply, use the official issue.

## Install

Uses the [skills CLI](https://github.com/vercel-labs/skills) from Vercel.

```bash
npx skills add daniellinuk/ELI100
```

Put it on every project for this machine, and skip the prompts:

```bash
npx skills add daniellinuk/ELI100 --skill eli100 -g -y
```

See the skill before you install it:

```bash
npx skills add daniellinuk/ELI100 --list
```

The skill lives in `skills/eli100/`. That folder name is the skill id.

## What you get

Your agent picks the kind of text (steps, explanation, or a safety note), rewrites it in ELI100, then runs a small checker. The checker catches long sentences, contractions, semicolons, and commands written in the passive. It will not pretend to be the official dictionary.

| | Everyday ELI100 | Full ELI100 |
| --- | --- | --- |
| A procedure | 25 words | 20 words |
| An explanation | 31 words | 25 words |

## License

[MIT](LICENSE) for this skill. That license does not cover ASD-STE100.
