#!/usr/bin/env python3
"""Source-level 15-word shingle check — NO build needed.
Extracts visible page text from src/lib/content-*.ts(x) PageData objects
(answer/intro/sections/faqs/related labels; title/description/path/crumbs/
service/howTo JSON-LD-only blocks excluded, matching what qa.py sees in <main>)
and compares within-site + vs the sister site's built out/.
Usage: python3 scripts/check-source-shingles.py [page-substring ...]
Exit 0 = 0 shared shingles on the filtered pairs; exit 1 = any remain.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import qa

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIB = os.path.join(SITE, "src", "lib")
SISTER_OUT = qa.SISTER_OUT

STR_RE = re.compile(r'"((?:[^"\\]|\\.)*)"')
# blocks that are NOT visible <main> text (JSON-LD only / head / nav)
DROP_KEYS = ("service:", "howTo:", "crumbs:")


def strip_dropped(block: str) -> str:
    """Remove service/howTo/crumbs blocks (balanced-brace aware, best effort)."""
    out = []
    i = 0
    while i < len(block):
        hit = None
        for key in DROP_KEYS:
            if block.startswith(key, i):
                hit = key
                break
        if hit is None:
            out.append(block[i])
            i += 1
            continue
        # skip to the matching closing brace of the value (object or array)
        j = block.find("{", i)
        k = block.find("[", i)
        if j == -1 and k == -1:
            break
        start = j if k == -1 or (j != -1 and j < k) else k
        open_c, close_c = block[start], ("}" if block[start] == "{" else "]")
        depth = 0
        p = start
        while p < len(block):
            if block[p] == open_c:
                depth += 1
            elif block[p] == close_c:
                depth -= 1
                if depth == 0:
                    break
            p += 1
        i = p + 1
    return "".join(out)


def extract_pages():
    pages = {}
    for fn in sorted(os.listdir(LIB)):
        if not fn.startswith("content-") or not fn.endswith((".ts", ".tsx")):
            continue
        src = open(os.path.join(LIB, fn), encoding="utf-8").read()
        for m in re.finditer(r"export const (\w+): PageData = \{(.*?)\n\};", src, re.S):
            block = m.group(2)
            pm = re.search(r'path: "([^"]+)"', block)
            if not pm:
                continue
            path = pm.group(1)
            block = strip_dropped(block)
            # drop title/description/path lines (head-only, not <main>)
            block = re.sub(r'(?m)^\s*(title|description|path): ".*?",?\s*$', "", block)
            lits = STR_RE.findall(block)
            # drop href literals (links/related arrays) — attributes, not visible text
            lits = [s for s in lits if not re.match(r"^(https?://|/|mailto:|tel:|wa\.me)", s)]
            text = " ".join(lits)
            # markdown links: keep visible text, drop the URL part
            text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
            text = text.replace('\\"', '"')
            pages[path] = text
    return pages


def sister_shingles():
    all_sis = set()
    per_page = {}
    for root, _, files in os.walk(SISTER_OUT):
        for f in files:
            if f != "index.html":
                continue
            fp = os.path.join(root, f)
            rel = os.path.relpath(fp, SISTER_OUT)
            d = os.path.dirname(rel)
            p = "/" + (d.replace(os.sep, "/") + "/" if d else "")
            sh = qa.shingles(qa.main_text(open(fp, encoding="utf-8").read()))
            per_page[p] = sh
            all_sis |= sh
    return all_sis, per_page


def show_pair(a: str, b: str):
    pages = extract_pages()
    sa, sb = qa.shingles(pages[a]), qa.shingles(pages[b])
    print(f"shared {a} x {b} ({len(sa & sb)}):")
    for s in sorted(sa & sb):
        print("  |", s)


def show_cross(a: str):
    pages = extract_pages()
    all_sis, per_page = sister_shingles()
    shared = qa.shingles(pages[a]) & all_sis
    print(f"shared {a} x sister ({len(shared)}):")
    for s in sorted(shared):
        holders = [p for p, sh in per_page.items() if s in sh]
        print(f"  | {s}   [sister: {', '.join(holders[:3])}]")


def main():
    if len(sys.argv) >= 4 and sys.argv[1] == "--show":
        show_pair(sys.argv[2], sys.argv[3])
        return 0
    if len(sys.argv) == 3 and sys.argv[1] == "--show-cross":
        show_cross(sys.argv[2])
        return 0
    only = sys.argv[1:]
    pages = extract_pages()
    print(f"pages extracted: {len(pages)}")
    assert len(pages) == 36, f"expected 36 pages, got {len(pages)}"
    sh = {p: qa.shingles(t) for p, t in pages.items()}
    keys = sorted(sh)
    within = []
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            shared = sh[keys[i]] & sh[keys[j]]
            if shared and (not only or any(o in keys[i] or o in keys[j] for o in only)):
                within.append((keys[i], keys[j], len(shared)))
    cross = []
    all_sis, _ = sister_shingles()
    for p in keys:
        n = len(sh[p] & all_sis)
        if n and (not only or any(o in p for o in only)):
            cross.append((p, n))
    print(f"WITHIN-SITE pairs: {len(within)}")
    for a, b, c in within:
        print(f"  {a} x {b} = {c}")
    print(f"CROSS-SITE pages: {len(cross)}")
    for p, n in cross:
        print(f"  {p} = {n}")
    if within or cross:
        print("RESULT: FAIL")
        return 1
    print("RESULT: PASS (0 shared 15-word shingles)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
