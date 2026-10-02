#!/usr/bin/env python3
"""Mechanical checks for ELI100 drafts.

This is an aid for the eli100 skill. It is not an official
ASD-STE100 checker and it does not contain the STE dictionary.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass

MODES = ("soften", "full")
KINDS = ("procedure", "description", "safety")

# Full limits are the public STE sentence limits.
# Soften is one quarter longer, rounded to the nearest word: 20→25, 25→31.
LIMITS = {
    "full": {"procedure": 20, "description": 25, "safety": 20},
    "soften": {"procedure": 25, "description": 31, "safety": 25},
}

UNITS = {
    "mm",
    "cm",
    "m",
    "km",
    "kg",
    "g",
    "lb",
    "lbs",
    "oz",
    "v",
    "a",
    "w",
    "hz",
    "khz",
    "mhz",
    "ghz",
    "psi",
    "bar",
    "rpm",
    "in",
    "ft",
    "°c",
    "°f",
    "%",
}

# Published STE choices (ASD public FAQ / encyclopedia summary). Not a dictionary.
FULL_WORD_SWAPS = {
    "begin": "start",
    "begins": "starts",
    "began": "started",
    "commence": "start",
    "commences": "starts",
    "commenced": "started",
    "initiate": "start",
    "initiates": "starts",
    "initiated": "started",
    "originate": "start",
    "originates": "starts",
    "originated": "started",
    "achieve": "do",
    "achieves": "does",
    "achieved": "did",
    "accomplish": "do",
    "accomplishes": "does",
    "accomplished": "did",
    "acceptance": "accept (verb)",
    "accessible": "get access to",
}

FOG_SWAPS = {
    "leverage": "use",
    "utilize": "use",
    "utilise": "use",
    "utilizes": "uses",
    "utilises": "uses",
    "optimize": "name the change",
    "optimise": "name the change",
    "optimizes": "name the change",
    "robust": "say what stays correct",
    "seamless": "say what the person does not have to do",
    "facilitate": "help, or name the action",
    "facilitates": "helps, or name the action",
    "empower": "allow",
    "holistic": "whole",
    "streamline": "remove a step, or name the shorter path",
}

PHRASE_SWAPS = (
    ("carry out", "do"),
    ("figure out", "find"),
    ("in order to", "to"),
    ("due to the fact that", "because"),
    ("a large number of", "many"),
    ("at this point in time", "now"),
)

CONTRACTION_RE = re.compile(
    r"\b(?:I'm|you're|we're|they're|he's|she's|it's|that's|there's|here's|"
    r"don't|doesn't|didn't|can't|couldn't|won't|wouldn't|shouldn't|isn't|"
    r"aren't|wasn't|weren't|haven't|hasn't|hadn't|let's|I've|you've|we've|"
    r"they've|I'd|you'd|he'd|she'd|we'd|they'd|I'll|you'll|he'll|she'll|"
    r"we'll|they'll)\b",
    re.IGNORECASE,
)

PASSIVE_RE = re.compile(
    r"\b(?:is|are|was|were|be|been|being)\s+"
    r"(?:being\s+)?(?:\w+ed|known|shown|done|written|given|taken|made|seen|"
    r"found|left|built|sent|kept|held|set|put|run|read)\b",
    re.IGNORECASE,
)

PROGRESSIVE_RE = re.compile(
    r"\b(?:is|are|was|were|be|been|being)\s+\w+ing\b",
    re.IGNORECASE,
)

ABBREVIATIONS = ("e.g.", "i.e.", "etc.", "Fig.", "No.", "vs.", "Mr.", "Dr.")


@dataclass
class Finding:
    severity: str  # ERROR or WARN
    code: str
    line: int
    message: str
    text: str


def strip_uncheckable(text: str) -> str:
    """Drop frontmatter and fenced code. Leave prose."""
    text = text.replace("\r\n", "\n")
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            text = text[end + 5 :]
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    text = re.sub(r"`[^`\n]+`", "", text)
    return text


def protect_abbreviations(text: str) -> str:
    for item in ABBREVIATIONS:
        text = text.replace(item, item.replace(".", "\0"))
        text = text.replace(item.lower(), item.lower().replace(".", "\0"))
        text = text.replace(item.upper(), item.upper().replace(".", "\0"))
    return text


def restore_dots(text: str) -> str:
    return text.replace("\0", ".")


def split_sentences(text: str) -> list[str]:
    protected = protect_abbreviations(text.strip())
    protected = re.sub(r"https?://\S+", " __URL__ ", protected)
    chunks = re.split(r"(?<=[.!?])\s+|\s*;\s*|\s*:\s+", protected)
    sentences = []
    for chunk in chunks:
        cleaned = restore_dots(chunk).strip(" \t-•")
        if cleaned:
            sentences.append(cleaned)
    return sentences


def word_count(sentence: str) -> int:
    text = sentence.strip()
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"https?://\S+", " __URL__ ", text)
    text = re.sub(r"\([^)]*\)", " __PAREN__ ", text)
    text = re.sub(r'"[^"]*"', " __QUOTE__ ", text)
    text = re.sub(r"“[^”]*”", " __QUOTE__ ", text)
    text = re.sub(r"(?<=\d),(?=\d)", "", text)
    text = text.replace("**", "").replace("*", "")
    tokens = re.findall(
        r"__PAREN__|__QUOTE__|__URL__|[A-Za-z0-9°%]+(?:-[A-Za-z0-9°%]+)*",
        text,
    )
    merged: list[str] = []
    index = 0
    while index < len(tokens):
        token = tokens[index]
        if (
            index + 1 < len(tokens)
            and re.fullmatch(r"\d+(?:\.\d+)?", token)
            and tokens[index + 1].lower() in UNITS
        ):
            merged.append(token + tokens[index + 1])
            index += 2
            continue
        merged.append(token)
        index += 1
    return len(merged)


def limit_for(mode: str, kind: str) -> int:
    return LIMITS[mode][kind]


def line_of(source: str, snippet: str) -> int:
    """Best-effort line number for a sentence in the stripped source."""
    needle = snippet.strip()[:40]
    if not needle:
        return 1
    for number, line in enumerate(source.splitlines(), start=1):
        if needle[:24] and needle[:24] in line:
            return number
    return 1


def check_text(text: str, mode: str, kind: str) -> list[Finding]:
    if mode not in MODES:
        raise ValueError(f"mode must be one of {MODES}")
    if kind not in KINDS:
        raise ValueError(f"kind must be one of {KINDS}")

    source = strip_uncheckable(text)
    findings: list[Finding] = []
    limit = limit_for(mode, kind)
    paragraphs = re.split(r"\n\s*\n", source)
    sentence_count = 0
    longest = 0

    if kind == "safety" and not re.search(r"\b(?:warning|caution)\b", source, re.I):
        findings.append(
            Finding(
                "WARN",
                "safety-label",
                1,
                'Safety text needs a signal word: "Warning" for injury, "Caution" for damage.',
                "",
            )
        )

    for paragraph in paragraphs:
        paragraph_sentences: list[str] = []
        for raw_line in paragraph.splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or re.fullmatch(r"[-| :]+", line):
                continue
            line = re.sub(r"^\s*(?:[-*+]|\d+[.)])\s+", "", line)
            if ";" in line:
                findings.append(
                    Finding(
                        "ERROR",
                        "semicolon",
                        line_of(source, line),
                        "Do not use a semicolon. Write two sentences.",
                        line,
                    )
                )
            paragraph_sentences.extend(split_sentences(line))

        if kind == "description" and len(paragraph_sentences) > 6:
            findings.append(
                Finding(
                    "ERROR" if mode == "full" else "WARN",
                    "paragraph-length",
                    line_of(source, paragraph_sentences[0]),
                    f"Paragraph has {len(paragraph_sentences)} sentences. Keep 6 or fewer.",
                    paragraph_sentences[0],
                )
            )

        for sentence in paragraph_sentences:
            sentence_count += 1
            count = word_count(sentence)
            longest = max(longest, count)
            where = line_of(source, sentence)
            if count > limit:
                findings.append(
                    Finding(
                        "ERROR",
                        "sentence-length",
                        where,
                        f"{count} words, limit {limit} ({kind}, {mode}).",
                        sentence,
                    )
                )
            if CONTRACTION_RE.search(sentence):
                findings.append(
                    Finding(
                        "ERROR",
                        "contraction",
                        where,
                        "Write the full words. Do not use a contraction.",
                        sentence,
                    )
                )
            if "—" in sentence or "–" in sentence:
                findings.append(
                    Finding(
                        "WARN",
                        "dash",
                        where,
                        "Rewrite the dash as two sentences or a comma.",
                        sentence,
                    )
                )
            if PROGRESSIVE_RE.search(sentence):
                findings.append(
                    Finding(
                        "ERROR",
                        "progressive",
                        where,
                        'Do not use "is/are + -ing". Use simple present, simple past, or a command.',
                        sentence,
                    )
                )
            if PASSIVE_RE.search(sentence):
                # "is blocked" is a state. Flag a description only when "by"
                # names the agent ("is sent by the pump").
                has_agent = re.search(r"\bby\b", sentence, re.I)
                if kind in ("procedure", "safety") or has_agent:
                    severity = "ERROR" if kind in ("procedure", "safety") else "WARN"
                    findings.append(
                        Finding(
                            severity,
                            "passive",
                            where,
                            "Use active voice. Name who does the action.",
                            sentence,
                        )
                    )
            if kind in ("procedure", "safety") and re.search(r"\byou must\b", sentence, re.I):
                findings.append(
                    Finding(
                        "WARN",
                        "you-must",
                        where,
                        'Write the command ("Open the valve."), not "You must open the valve."',
                        sentence,
                    )
                )

            lowered = sentence.lower()
            for phrase, replacement in PHRASE_SWAPS:
                if phrase in lowered:
                    severity = "ERROR" if mode == "full" and phrase in ("carry out", "figure out") else "WARN"
                    findings.append(
                        Finding(
                            severity,
                            "phrase",
                            where,
                            f'Replace "{phrase}" with "{replacement}".',
                            sentence,
                        )
                    )
            for match in re.finditer(r"[A-Za-z]+(?:'[A-Za-z]+)?", sentence):
                word = match.group(0).lower()
                if mode == "full" and word in FULL_WORD_SWAPS:
                    findings.append(
                        Finding(
                            "ERROR",
                            "word-choice",
                            where,
                            f'"{word}" → {FULL_WORD_SWAPS[word]} (public STE example, not a dictionary lookup).',
                            sentence,
                        )
                    )
                elif word in FOG_SWAPS:
                    findings.append(
                        Finding(
                            "WARN",
                            "fog",
                            where,
                            f'"{word}": {FOG_SWAPS[word]}.',
                            sentence,
                        )
                    )

    check_text.last_stats = (sentence_count, longest, limit)  # type: ignore[attr-defined]
    return findings


def format_report(findings: list[Finding], mode: str, kind: str) -> str:
    stats = getattr(check_text, "last_stats", (0, 0, limit_for(mode, kind)))
    sentence_count, longest, limit = stats
    errors = [item for item in findings if item.severity == "ERROR"]
    warnings = [item for item in findings if item.severity == "WARN"]
    lines = []
    if not findings:
        lines.append("OK")
    else:
        for item in findings:
            lines.append(
                f"{item.severity} {item.code} line {item.line}: {item.message}"
            )
            if item.text:
                lines.append(f"  {item.text}")
    lines.append(
        f"{sentence_count} sentences, longest {longest} words, "
        f"limit {limit}, mode={mode}, kind={kind}, "
        f"errors={len(errors)}, warnings={len(warnings)}"
    )
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Check a draft against ELI100 / public STE sentence rules."
    )
    parser.add_argument(
        "--mode",
        choices=MODES,
        default="soften",
        help="soften = about 80 percent (default). full = public STE sentence limits.",
    )
    parser.add_argument(
        "--kind",
        choices=KINDS,
        default="description",
        help="procedure and safety use the shorter limit. description uses the longer limit.",
    )
    parser.add_argument(
        "files",
        nargs="*",
        help="Text or markdown files. Reads stdin when omitted.",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Run built-in checks and exit.",
    )
    return parser


def self_test() -> int:
    failures: list[str] = []

    def expect(condition: bool, message: str) -> None:
        if not condition:
            failures.append(message)

    expect(word_count("off-the-shelf") == 1, "hyphenated word counts as one")
    expect(word_count("The 12 mm bolt is tight.") == 5, f"number+unit, got {word_count('The 12 mm bolt is tight.')}")
    expect(
        word_count("Turn the cover until you get access to the jacks.") == 10,
        "simple sentence count",
    )
    long = (
        "Remove the large cover from the primary hydraulic pump before you "
        "start the test on the unit today please now here."
    )
    expect(word_count(long) == 21, f"21-word sentence, got {word_count(long)}")

    full_hits = check_text(long, "full", "procedure")
    expect(any(item.code == "sentence-length" for item in full_hits), "full mode flags 21 words")
    soften_hits = check_text(long, "soften", "procedure")
    expect(
        not any(item.code == "sentence-length" for item in soften_hits),
        "soften mode allows 21 words in a procedure",
    )

    contraction = check_text("Don't remove the cover.", "soften", "procedure")
    expect(any(item.code == "contraction" for item in contraction), "flags contraction")

    semi = check_text("Open the valve; close the vent.", "soften", "procedure")
    expect(any(item.code == "semicolon" for item in semi), "flags semicolon")

    progressive = check_text("The pump is sending fluid.", "full", "description")
    expect(any(item.code == "progressive" for item in progressive), "flags progressive")

    passive = check_text("The cover is removed.", "full", "procedure")
    expect(
        any(item.severity == "ERROR" and item.code == "passive" for item in passive),
        "procedure passive is an error",
    )
    blocked = check_text("When the filter is blocked, the pump stops.", "full", "description")
    expect(not any(item.code == "passive" for item in blocked), "a state is not a passive")
    by_agent = check_text("The fluid is sent by the pump.", "full", "description")
    expect(any(item.code == "passive" for item in by_agent), "a by-agent passive warns")

    begin = check_text("Begin the test.", "full", "procedure")
    expect(any(item.code == "word-choice" for item in begin), "full mode flags begin")
    begin_soft = check_text("Begin the test.", "soften", "procedure")
    expect(
        not any(item.code == "word-choice" for item in begin_soft),
        "soften mode does not dictionary-flag begin",
    )

    coded = "```\n" + long + "\n```\n\nTurn the cover.\n"
    coded_hits = check_text(coded, "full", "procedure")
    expect(
        not any(item.code == "sentence-length" for item in coded_hits),
        "fenced code is ignored",
    )

    paragraph = " ".join(f"This is sentence {index}." for index in range(1, 8))
    paragraph_hits = check_text(paragraph, "full", "description")
    expect(
        any(item.code == "paragraph-length" for item in paragraph_hits),
        "flags a 7-sentence paragraph in full description",
    )

    ok = check_text(
        "Turn the cover until you get access to the jacks.\n\nDo the test.\n",
        "full",
        "procedure",
    )
    expect(ok == [], f"clean procedure should pass, got {ok}")

    if failures:
        print("SELF-TEST FAILED")
        for item in failures:
            print(f"- {item}")
        return 1
    print("SELF-TEST OK")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test()

    if args.files:
        chunks = []
        for path in args.files:
            with open(path, encoding="utf-8") as handle:
                chunks.append(handle.read())
        text = "\n\n".join(chunks)
    else:
        text = sys.stdin.read()

    findings = check_text(text, args.mode, args.kind)
    print(format_report(findings, args.mode, args.kind))
    return 1 if any(item.severity == "ERROR" for item in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
