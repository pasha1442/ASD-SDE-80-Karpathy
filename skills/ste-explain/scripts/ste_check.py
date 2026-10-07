#!/usr/bin/env python3
"""Check text against the mechanical rules of STE-style writing.

    ste_check.py FILE [FILE ...]        style findings for each file
    echo "text" | ste_check.py          style findings for stdin
    ste_check.py --compare SRC DRAFT    facts in SRC that are missing from DRAFT
    ste_check.py --selftest             run the built-in tests

Options:
    --limit 20|25|auto   sentence limit in words (default auto: 20 for an
                         instruction, 25 for a description)
    --json               print findings as JSON
    --max-hard N         exit 0 if there are N hard findings or fewer (default 0)

Hard findings make the exit code 1. Advisory findings never do.
The script finds patterns. It does not prove compliance with ASD-STE100, and
it does not prove that a rewrite kept the meaning. Standard library only.
"""
import json
import re
import sys

ABBREV = r"\b(?:e\.g|i\.e|etc|vs|approx|fig|no|mr|mrs|ms|dr|st|inc|ltd)\.$"
IMPERATIVES = set("""add adjust apply ask attach build call change check choose clean clear click close
connect copy create delete disable disconnect do download edit enable enter examine export find fill fix
follow get give go hold import install keep let list load look make measure move open paste press pull push
put read record release remove rename replace restart run save select send set show start stop tell
turn type uninstall update upload use wait write""".split())

FILLER = [
    r"it is (?:important|worth|useful) (?:to note|noting|mentioning)(?: that)?",
    r"it should be noted that", r"please note that", r"needless to say",
    r"as (?:mentioned|stated|noted) (?:above|earlier|previously)",
    r"at the end of the day", r"in order to", r"basically", r"essentially",
    r"great question", r"i hope this helps",
]
FORMAL = {
    r"utili[sz](?:e|es|ed|ing)": "use", r"commenc(?:e|es|ed|ing)": "start", r"prior to": "before",
    r"ensur(?:e|es|ed|ing)": "make sure", r"replenish(?:es|ed|ing)?": "fill",
    r"subsequently": "then", r"facilitat(?:e|es|ed|ing)": "help", r"leverag(?:e|es|ed|ing)": "use",
    r"numerous": "many", r"sufficient": "enough", r"terminat(?:e|es|ed|ing)": "stop",
    r"in the event that": "if", r"due to the fact that": "because", r"with regard to": "about",
    r"a (?:large )?number of": "many", r"at this point in time": "now",
}
PHRASAL = r"spin(?:s|ning)? up|spun up|kick(?:s|ed|ing)? off|reach(?:es|ed|ing)? out|div(?:e|es|ed|ing) into|circl(?:e|es|ed|ing) back|touch(?:es|ed|ing)? base"
NOMINAL = r"(?:perform|performs|performed|conduct|conducts|conducted|carry out|carries out|carried out|make|makes|made)\s+(?:a|an|the)\s+\w+(?:tion|sion|ment|ysis|ance)\s+(?:of|to|on)"
PARTICIPLES = "made|done|given|taken|shown|written|sent|built|found|kept|set|run|read|held|left|put|known|seen"
PASSIVE = rf"\b(?:is|are|was|were|be|been|being)\s+(?:not\s+)?(?:\w+ed|{PARTICIPLES})\b"
PERFECT = rf"\b(?:has|have|had)\s+(?:not\s+)?(?:been\s+)?(?:\w+ed|\w+en|{PARTICIPLES})\b"
PROGRESSIVE = r"\b(?:is|are|was|were|am)\s+(?:not\s+)?\w{3,}ing\b"
MODAL_BEFORE = re.compile(r"\b(?:may|might|could|should|would|must|can|will)(?:\s+not)?\s+$", re.I)
HEDGES = ["may", "might", "could", "can", "probably", "possibly", "sometimes", "usually",
          "unless", "if", "only", "except", "not", "never", "approximately"]


def strip_markup(text):
    """Remove code and Markdown structure. Return a list of (kind, text) blocks."""
    text = re.sub(r"^---\n.*?\n---\n", "", text, count=1, flags=re.S)        # frontmatter
    text = re.sub(r"(```|~~~).*?\1", "\n\n", text, flags=re.S)                 # fenced code
    text = re.sub(r"`[^`\n]+`", "CODE", text)                                  # inline code
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)                     # links
    text = re.sub(r"https?://\S+", "URL", text)
    blocks, para = [], []

    def flush():
        if para:
            blocks.append(("para", " ".join(para)))
            para.clear()

    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith(("#", "|", ">", "<")) or re.fullmatch(r"[-=*_ ]{3,}", s):
            flush()
            continue
        m = re.match(r"(?:[-*+]|\d+[.)])\s+(.*)", s)
        if m:
            flush()
            blocks.append(("item", m.group(1)))
        else:
            para.append(s)
    flush()
    return [(k, re.sub(r"[*_]{1,3}", "", t)) for k, t in blocks]


def sentences(text):
    out, start = [], 0
    for m in re.finditer(r"[.!?]+[\"')\]]*(?=\s+|$)", text):
        chunk = text[start:m.end()].strip()
        if re.search(ABBREV, chunk, re.I):
            continue
        if chunk:
            out.append(chunk)
        start = m.end()
    rest = text[start:].strip()
    if rest:
        out.append(rest)
    return out


def word_count(s):
    return len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'’\-/.%]*", s))


def is_instruction(s):
    s = re.sub(r"^(?:WARNING|CAUTION|NOTE)\s*:\s*", "", s)
    s = re.sub(r"^(?:if|when|before|after)\b[^,]*,\s*", "", s, flags=re.I)
    first = re.match(r"[A-Za-z]+", s)
    return bool(first) and (first.group(0).lower() in IMPERATIVES or s.lower().startswith("do not"))


def check(text, limit="auto"):
    findings = []

    def add(level, rule, sentence, detail):
        findings.append({"level": level, "rule": rule, "detail": detail,
                         "sentence": sentence if len(sentence) < 160 else sentence[:157] + "..."})

    for kind, block in strip_markup(text):
        sents = sentences(block)
        if kind == "para" and len(sents) > 6:
            add("hard", "paragraph-length", sents[0], f"{len(sents)} sentences in one paragraph, limit 6")
        for s in sents:
            n = word_count(s)
            lim = (20 if is_instruction(s) else 25) if limit == "auto" else int(limit)
            if n > lim:
                add("hard", "sentence-length", s, f"{n} words, limit {lim}")
            if ";" in s:
                add("hard", "semicolon", s, "write two sentences")
            for pat in FILLER:
                for m in re.finditer(rf"\b{pat}\b", s, re.I):
                    add("hard", "filler", s, f'delete or shorten "{m.group(0)}"')
            for pat, plain in FORMAL.items():
                for m in re.finditer(rf"\b{pat}\b", s, re.I):
                    add("hard", "formal-word", s, f'"{m.group(0)}" -> "{plain}"')
            for m in re.finditer(rf"\b(?:{PHRASAL})\b", s, re.I):
                add("hard", "phrasal-verb", s, f'use one plain verb for "{m.group(0)}"')
            for m in re.finditer(rf"\b{NOMINAL}\b", s, re.I):
                add("hard", "noun-for-verb", s, f'use the verb for "{m.group(0)}"')
            for m in re.finditer(PASSIVE, s, re.I):
                add("advisory", "passive-voice", s, f'"{m.group(0)}": name who does the action')
            for m in re.finditer(PERFECT, s, re.I):
                if not MODAL_BEFORE.search(s[:m.start()]):
                    add("advisory", "perfect-tense", s, f'"{m.group(0)}": use a simple tense if the meaning stays the same')
            for m in re.finditer(PROGRESSIVE, s, re.I):
                add("advisory", "progressive-tense", s, f'"{m.group(0)}": use the simple present')
    return findings


def facts(text):
    """Tokens that a rewrite must keep: code, identifiers, numbers."""
    found = set(re.findall(r"`([^`\n]+)`", text))
    plain = re.sub(r"`[^`\n]+`", " ", text)
    found |= set(re.findall(r"\b\d+(?:[.,]\d+)*\s?(?:%|ms|s|sec|min|h|kb|mb|gb|tb|px|x|k|m)?\b", plain, re.I))
    found |= set(re.findall(r"\b[A-Za-z]+(?:_[A-Za-z0-9]+)+\b", plain))                 # snake_case
    found |= set(re.findall(r"\b[a-z]+(?:[A-Z][a-z0-9]+)+\b", plain))                   # camelCase
    found |= set(re.findall(r"\b(?:[A-Z][a-z0-9]+){2,}\b", plain))                      # PascalCase
    found |= set(re.findall(r"\b[A-Z][A-Z0-9]{1,}(?:-[A-Z0-9]+)*\b", plain))            # ACRONYM, STE-100
    found |= set(re.findall(r"(?<![\w/])(?:\.{0,2}/)?[\w\-]+(?:/[\w\-.]+)+", plain))      # paths
    found |= set(re.findall(r"\b[\w\-]+\.(?:py|js|ts|json|ya?ml|md|toml|sh|html|css|sql|csv|txt)\b", plain))
    return {f.strip() for f in found if f.strip()}


def compare(src, draft):
    findings, low = [], re.sub(r"\s+", " ", draft).lower()
    for f in sorted(facts(src), key=str.lower):
        if re.sub(r"\s+", " ", f).lower() not in low:
            findings.append({"level": "hard", "rule": "lost-fact", "sentence": "",
                             "detail": f'"{f}" is in the source and not in the rewrite'})
    for h in HEDGES:
        a = len(re.findall(rf"\b{h}\b", src, re.I))
        b = len(re.findall(rf"\b{h}\b", draft, re.I))
        if b < a:
            findings.append({"level": "advisory", "rule": "hedge-count", "sentence": "",
                             "detail": f'"{h}": {a} in the source, {b} in the rewrite. Check that no condition or doubt was lost'})
    return findings


def report(name, findings, as_json):
    hard = [f for f in findings if f["level"] == "hard"]
    if as_json:
        return {"file": name, "hard": len(hard), "advisory": len(findings) - len(hard), "findings": findings}
    lines = [f"{name}: {len(hard)} hard, {len(findings) - len(hard)} advisory"]
    for f in findings:
        tag = "HARD    " if f["level"] == "hard" else "advisory"
        lines.append(f"  {tag} {f['rule']}: {f['detail']}")
        if f["sentence"]:
            lines.append(f"           > {f['sentence']}")
    return "\n".join(lines)


def selftest():
    rules = lambda t, **k: {f["rule"] for f in check(t, **k)}
    assert rules("Check the log. Restart the service.") == set()
    assert "sentence-length" in rules("Open " + "the big red door " * 6 + "now.")
    assert "sentence-length" not in rules("The server sends " + "one more small item " * 4 + "to the client.")
    assert "semicolon" in rules("The cache is full; the service stops.")
    assert "formal-word" in rules("Utilize the tool prior to the upgrade.")
    assert "filler" in rules("It is important to note that the port is 80.")
    assert "passive-voice" in rules("The file is deleted by the script.")
    assert "perfect-tense" in rules("The server has received the request.")
    assert "perfect-tense" not in rules("The request may have failed.")
    assert "noun-for-verb" in rules("Perform an analysis of the log.")
    assert rules("Run `rm -rf build; make` now.") == set()
    assert rules("```\nx = utilize(y); z = 1\n```\nStart the job.") == set()
    assert len(sentences("Use a tool, e.g. curl. Then stop.")) == 2
    lost = {f["detail"] for f in compare("The `debounce` call waits 200 ms. It may fail.", "The call waits. It fails.")}
    assert any("debounce" in d for d in lost) and any("200 ms" in d for d in lost) and any('"may"' in d for d in lost)
    assert compare("Set max_retries to 3 in config.yaml.", "In config.yaml, set max_retries to 3.") == []
    print("selftest: all checks passed")


def main(argv):
    if "-h" in argv or "--help" in argv:
        print(__doc__)
        return 0
    if "--selftest" in argv:
        selftest()
        return 0
    as_json = "--json" in argv
    limit, max_hard, files, i = "auto", 0, [], 0
    args = [a for a in argv if a != "--json"]
    if "--compare" in args:
        k = args.index("--compare")
        try:
            src, draft = open(args[k + 1], encoding="utf-8").read(), open(args[k + 2], encoding="utf-8").read()
        except (IndexError, OSError) as e:
            print(f"--compare needs two readable files: SOURCE DRAFT ({e})", file=sys.stderr)
            return 2
        res = [("compare", compare(src, draft))]
        if "--style" not in args:
            res.append((args[k + 2], check(draft)))
    else:
        while i < len(args):
            if args[i] == "--limit" and i + 1 < len(args):
                limit, i = args[i + 1], i + 2
            elif args[i] == "--max-hard" and i + 1 < len(args):
                max_hard, i = int(args[i + 1]), i + 2
            else:
                files.append(args[i])
                i += 1
        if limit not in ("auto", "20", "25"):
            print("--limit must be 20, 25 or auto", file=sys.stderr)
            return 2
        res = []
        if not files:
            res.append(("stdin", check(sys.stdin.read(), limit)))
        for f in files:
            try:
                res.append((f, check(open(f, encoding="utf-8").read(), limit)))
            except OSError as e:
                print(f"cannot read {f}: {e}", file=sys.stderr)
                return 2
    out = [report(n, f, as_json) for n, f in res]
    print(json.dumps(out, indent=2) if as_json else "\n".join(out))
    hard = sum(1 for _, fs in res for f in fs if f["level"] == "hard")
    return 1 if hard > max_hard else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
