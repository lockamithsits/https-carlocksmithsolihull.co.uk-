#!/usr/bin/env python3
"""QA for carlocksmithsolihull.co.uk v1 export (Phase 2 §9 V-1–V-28).
Run from ~/workspace/car-locksmith-solihull/site after `pnpm build`.
Usage: python3 scripts/qa.py
Exit 0 = all Critical checks pass; exit 1 = any Critical failure.
"""
import json
import os
import re
import sys
import html as htmlmod
from collections import Counter, defaultdict
from html.parser import HTMLParser

SITE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(SITE_DIR, "out")
SISTER_OUT = "/home/hatch/workspace/auto-locksmith-solihull/site/out"
DOMAIN = "https://carlocksmithsolihull.co.uk"
PHONE = "07367 634032"
GSC_META = "evUqxPEx6hweGprFgsMcFNyP7aopv_8SOM2UfWVQ-6I"
GTM = "GTM-N7QTF8Q3"

EXPECTED_36 = [
    "/", "/emergency-car-locksmith-solihull/", "/locked-out-of-car-solihull/",
    "/car-key-replacement-solihull/", "/all-keys-lost-solihull/", "/spare-car-key-solihull/",
    "/car-key-programming-solihull/", "/car-key-fob-replacement-solihull/",
    "/broken-car-key-extraction-solihull/", "/ignition-repair-solihull/",
    "/car-door-lock-repair-solihull/", "/nec-birmingham-airport-car-park-lockout/",
    "/proof-of-ownership/", "/car-locksmith-faq/", "/car-locksmith-prices-solihull/",
    "/areas-we-cover/",
    "/car-locksmith-shirley/", "/car-locksmith-knowle/", "/car-locksmith-dorridge/",
    "/car-locksmith-olton/", "/car-locksmith-hockley-heath/", "/car-locksmith-balsall-common/",
    "/car-locksmith-meriden/", "/car-locksmith-chelmsley-wood/", "/car-locksmith-hampton-in-arden/",
    "/car-locksmith-elmdon/", "/car-locksmith-castle-bromwich/", "/car-locksmith-marston-green/",
    "/about/", "/contact/", "/privacy/", "/reviews/",
    "/blog/", "/blog/how-much-does-a-car-key-replacement-cost/",
    "/blog/why-wont-my-key-fob-work/", "/blog/locked-out-of-your-car-what-to-do/",
]

failures = []
warnings = []

def fail(msg):
    failures.append(msg)
    print(f"  FAIL: {msg}")

def warn(msg):
    warnings.append(msg)
    print(f"  warn: {msg}")

def ok(msg):
    print(f"  ok: {msg}")

class TextExtractor(HTMLParser):
    """Extract <main> visible text, stripping site chrome (nav, scripts,
    CTA row, trust line, last-updated line) so the uniqueness check compares
    real page copy only — per the uniqueness skill's chrome rule."""
    def __init__(self):
        super().__init__()
        self.parts = []
        self.in_main = False
        self.skip_stack = []  # tags whose content is chrome
    def handle_starttag(self, tag, attrs):
        if tag == "main":
            self.in_main = True
        if tag in ("script", "style", "nav"):
            self.skip_stack.append(tag)
            return
        cls = dict(attrs).get("class", "")
        if tag == "div" and "cta-row" in cls:
            self.skip_stack.append(tag)
        elif tag == "p" and ("trust-line" in cls or "mt-8 text-sm text-slate-500" in cls):
            self.skip_stack.append(tag)
    def handle_endtag(self, tag):
        if tag == "main":
            self.in_main = False
        if self.skip_stack and self.skip_stack[-1] == tag:
            self.skip_stack.pop()
    def handle_data(self, data):
        if self.in_main and not self.skip_stack:
            self.parts.append(data)

def main_text(html_text):
    p = TextExtractor()
    p.feed(html_text)
    return " ".join(p.parts)

def path_to_file(path):
    if path == "/":
        return os.path.join(OUT, "index.html")
    return os.path.join(OUT, path.strip("/"), "index.html")

def read_html(path):
    with open(path_to_file(path), encoding="utf-8") as f:
        return f.read()

def shingles(text, n=15):
    words = re.findall(r"[a-z0-9']+", text.lower())
    return {" ".join(words[i:i+n]) for i in range(len(words) - n + 1)}

def extract_faq_visible(html_text):
    """Return list of (q, a) from the visible FAQ section."""
    m = re.search(r'<section aria-label="Frequently asked questions".*?</section>', html_text, re.S)
    if not m:
        return []
    sec = m.group(0)
    pairs = re.findall(r"<h3>(.*?)</h3>\s*<p>(.*?)</p>", sec, re.S)
    out = []
    for q, a in pairs:
        q = htmlmod.unescape(re.sub(r"<[^>]+>", "", q)).strip()
        a = htmlmod.unescape(re.sub(r"<[^>]+>", "", a)).strip()
        out.append((q, a))
    return out

def extract_faq_jsonld(html_text):
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html_text, re.S)
    for b in blocks:
        try:
            data = json.loads(htmlmod.unescape(b))
        except Exception:
            continue
        if isinstance(data, dict) and data.get("@type") == "FAQPage":
            return [(e["name"], e["acceptedAnswer"]["text"]) for e in data.get("mainEntity", [])]
    return None

def main():
    print("== V-4/V-5 sitemap ==")
    sm_path = os.path.join(OUT, "sitemap.xml")
    if not os.path.exists(sm_path):
        fail("sitemap.xml missing from out/")
        sm_urls = set()
    else:
        sm = open(sm_path, encoding="utf-8").read()
        sm_urls = set(re.findall(r"<loc>(.*?)</loc>", sm))
        exp_urls = {DOMAIN + p for p in EXPECTED_36}
        if sm_urls == exp_urls:
            ok(f"sitemap == expected 36 URLs")
        else:
            fail(f"sitemap mismatch: missing={sorted(exp_urls - sm_urls)} extra={sorted(sm_urls - exp_urls)}")

    print("== titles / metas / h1 ==")
    title_bad, meta_bad, h1_bad, qual_bad = [], [], [], []
    faq_total = 0
    faq_mismatch = []
    faq_wc_bad = []
    for p in EXPECTED_36:
        fp = path_to_file(p)
        if not os.path.exists(fp):
            fail(f"missing export file for {p}")
            continue
        h = read_html(p)
        mt = re.search(r"<title>(.*?)</title>", h, re.S)
        title = htmlmod.unescape(mt.group(1)).strip() if mt else ""
        if not (50 <= len(title) <= 60) or PHONE not in title:
            title_bad.append((p, len(title), title))
        md = re.search(r'<meta name="description" content="(.*?)"', h, re.S)
        meta = htmlmod.unescape(md.group(1)).strip() if md else ""
        if not (140 <= len(meta) <= 155) or PHONE not in meta:
            meta_bad.append((p, len(meta), meta))
        h1s = re.findall(r"<h1[^>]*>(.*?)</h1>", h, re.S)
        h1_text = [htmlmod.unescape(re.sub(r"<[^>]+>", "", x)).strip() for x in h1s]
        if len(h1_text) != 1:
            h1_bad.append((p, h1_text))
        else:
            first100 = main_text(h)[:600].lower()
            # Phase-4-verbatim H1 exceptions (no car/auto/vehicle word by design):
            # /reviews/ H1 "Reviews", /blog/why-wont-my-key-fob-work/ H1 "Why Won't My Key Fob Work?",
            # /car-key-fob-replacement-solihull/ "Key Fob Repair and Replacement in Solihull" (Phase 4 §6.2),
            # /nec-birmingham-airport-car-park-lockout/ "Locked Out at the NEC or Birmingham Airport" (Phase 4 §5.x),
            # /privacy/ "Privacy Policy" (Phase 4 §10.3). URLs + titles carry the qualifier on all five.
            if p in ("/reviews/", "/blog/why-wont-my-key-fob-work/",
                     "/car-key-fob-replacement-solihull/",
                     "/nec-birmingham-airport-car-park-lockout/", "/privacy/"):
                pass
            elif not any(k in h1_text[0].lower() for k in ("car", "auto", "vehicle")):
                qual_bad.append((p, "h1", h1_text[0]))
            if not any(k in first100 for k in ("car", "auto", "vehicle")):
                qual_bad.append((p, "first-paras", ""))
        # FAQ byte-match
        vis = extract_faq_visible(h)
        jld = extract_faq_jsonld(h)
        faq_total += len(vis)
        if jld is None:
            if vis:
                faq_mismatch.append((p, "visible FAQs but no FAQPage JSON-LD"))
        elif vis != jld:
            faq_mismatch.append((p, f"visible={len(vis)} jsonld={len(jld)}"))
        for q, a in vis:
            wc = len(a.split())
            if not (40 <= wc <= 60):
                faq_wc_bad.append((p, q[:40], wc))
    if title_bad: fail(f"titles out of range/missing phone: {title_bad}")
    else: ok("all 36 titles 50-60 chars + phone")
    if meta_bad: fail(f"metas out of range/missing phone: {meta_bad}")
    else: ok("all 36 metas 140-155 chars + phone")
    if h1_bad: fail(f"H1 count != 1: {h1_bad}")
    else: ok("exactly 1 H1 per page")
    if qual_bad: fail(f"missing car/auto/vehicle qualifier: {qual_bad}")
    else: ok("car qualifier in every H1 + first paragraphs")
    if faq_mismatch: fail(f"FAQ byte-match failures: {faq_mismatch}")
    else: ok(f"FAQ JSON-LD byte-matches visible text ({faq_total} FAQs total)")
    if faq_wc_bad: fail(f"FAQ answers outside 40-60w: {faq_wc_bad}")
    else: ok("all FAQ answers 40-60 words")

    print("== canonicals / GSC / GTM ==")
    canon_bad, gsc_bad, gtm_bad = [], [], []
    for p in EXPECTED_36:
        h = read_html(p)
        cm = re.search(r'<link rel="canonical" href="(.*?)"', h)
        if not cm or cm.group(1) != DOMAIN + p:
            canon_bad.append((p, cm.group(1) if cm else None))
        if GSC_META not in h:
            gsc_bad.append(p)
        if GTM not in h or f"ns.html?id={GTM}" not in h:
            gtm_bad.append(p)
    if canon_bad: fail(f"canonical mismatches: {canon_bad}")
    else: ok("all 36 self-canonicals apex + trailing slash")
    if gsc_bad: fail(f"GSC meta missing on: {gsc_bad}")
    else: ok("GSC meta on 36/36 pages")
    if gtm_bad: fail(f"GTM missing on: {gtm_bad}")
    else: ok("GTM script + noscript on 36/36 pages")
    if os.path.exists(os.path.join(OUT, "googleb7d79ba7b0fa42b4.html")):
        ok("GSC HTML file in out/")
    else:
        fail("GSC HTML file missing from out/")

    print("== links / orphans ==")
    link_graph = defaultdict(set)
    broken = []
    all_html = {}
    for p in EXPECTED_36:
        all_html[p] = read_html(p)
    for p, h in all_html.items():
        for href in re.findall(r'href="(/[^"#]*?)"', h):
            if href.startswith("//"):
                continue
            target = href.split("?")[0]
            if not target.endswith("/"):
                target += "/"
            if target in EXPECTED_36 or target == "/404/":
                link_graph[target].add(p)
            else:
                # allow asset-ish internal links
                if target.startswith(("/_next/", "/favicon", "/logo", "/og-image", "/site.webmanifest",
                                       "/robots.txt", "/sitemap.xml", "/llms.txt", "/google",
                                       "/apple-touch-icon", "/android-chrome", "/icon.svg")):
                    continue
                broken.append((p, href))
    if broken: fail(f"broken internal links: {broken[:20]}")
    else: ok("0 broken internal links")
    orphans = [p for p in EXPECTED_36 if p != "/" and not link_graph.get(p)]
    if orphans: fail(f"orphan pages (no inbound link): {orphans}")
    else: ok("0 orphans (every page linked)")

    print("== JSON-LD inventory ==")
    type_counts = Counter()
    parse_errors = []
    for p in EXPECTED_36:
        h = all_html[p]
        for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
            try:
                data = json.loads(htmlmod.unescape(b))
            except Exception as e:
                parse_errors.append((p, str(e)[:80]))
                continue
            t = data.get("@type")
            if isinstance(t, list):
                for x in t:
                    type_counts[x] += 1
            elif t:
                type_counts[t] += 1
            blob = json.dumps(data)
            for bad in ("aggregateRating", "AutomotiveBusiness", "sameAs", '"geo"'):
                if bad in blob:
                    parse_errors.append((p, f"forbidden token {bad} in JSON-LD"))
    print(f"  types: {dict(type_counts)}")
    if parse_errors: fail(f"JSON-LD errors: {parse_errors[:10]}")
    else: ok("0 JSON-LD parse errors, no forbidden tokens")
    # FAQPage 36: every v1 page carries its own FAQs (Phase 8 estimated 31
    # assuming 5 pages FAQ-less; the build gives FAQs to all 36 pages).
    for want, n in [("Locksmith", 36), ("BreadcrumbList", 36), ("WebPage", 36),
                    ("Service", 23), ("FAQPage", 36), ("BlogPosting", 3), ("HowTo", 2), ("WebSite", 1)]:
        got = type_counts.get(want, 0)
        if got != n:
            fail(f"schema count {want}: got {got}, want {n}")
        else:
            ok(f"schema {want}: {got}")

    print("== shingles (15-word) ==")
    def site_shingles(out_dir, pages):
        per_page = {}
        for p in pages:
            fp = os.path.join(out_dir, "index.html") if p == "/" else os.path.join(out_dir, p.strip("/"), "index.html")
            if not os.path.exists(fp):
                continue
            per_page[p] = shingles(main_text(open(fp, encoding="utf-8").read()))
        return per_page
    ours = site_shingles(OUT, EXPECTED_36)
    within = []
    keys = list(ours)
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            shared = ours[keys[i]] & ours[keys[j]]
            if shared:
                within.append((keys[i], keys[j], len(shared)))
    if within: fail(f"within-site shared 15-word shingles: {within[:10]}")
    else: ok("0 shared 15-word shingles within site")
    # vs sister
    if os.path.isdir(SISTER_OUT):
        sister_pages = []
        for root, _, files in os.walk(SISTER_OUT):
            for f in files:
                if f == "index.html":
                    rel = os.path.relpath(os.path.join(root, f), SISTER_OUT)
                    sister_pages.append("/" + os.path.dirname(rel).replace(os.sep, "/") + ("/" if os.path.dirname(rel) else ""))
        sister = site_shingles(SISTER_OUT, sister_pages)
        all_sister = set().union(*sister.values()) if sister else set()
        cross = []
        for p, sh in ours.items():
            shared = sh & all_sister
            if shared:
                cross.append((p, len(shared)))
        if cross: fail(f"cross-site shared 15-word shingles vs sister: {cross[:10]}")
        else: ok("0 shared 15-word shingles vs sister site")
    else:
        warn("sister out/ not found — cross-site check skipped")

    print("== banned content / leaks ==")
    banned = [("£", re.compile(r"£")), ("no call-out fee", re.compile(r"no call-out fee", re.I)),
              ("DBS", re.compile(r"\bDBS\b")), ("guarantee", re.compile(r"guarantee", re.I)),
              ("slim jim", re.compile(r"slim jim", re.I)), ("unlock any car free", re.compile(r"unlock any car free", re.I)),
              ("cheapest", re.compile(r"cheapest", re.I)), ("fastest", re.compile(r"fastest", re.I)),
              ("Auto Locksmith Solihull", re.compile(r"Auto Locksmith Solihull")),
              ("autolocksmithsolihull", re.compile(r"autolocksmithsolihull")),
              ("AutomotiveBusiness", re.compile(r"AutomotiveBusiness")),
              ("aggregateRating", re.compile(r"aggregateRating"))]
    hits = defaultdict(list)
    for p in EXPECTED_36:
        h = all_html[p]
        for name, rx in banned:
            if rx.search(h):
                hits[name].append(p)
    # "insured" as a claim — allow the word only in "not insured" style denials? treat any hit as fail, review manually
    for p in EXPECTED_36:
        if re.search(r"\binsured\b", all_html[p], re.I):
            hits["insured"].append(p)
    if hits:
        for k, v in hits.items():
            fail(f"banned/leak term '{k}' on {len(v)} pages: {v[:6]}")
    else:
        ok("0 banned terms / sister-brand leaks in export")

    print("== files / headers / misc ==")
    if os.path.exists(os.path.join(OUT, "robots.txt")):
        rt = open(os.path.join(OUT, "robots.txt"), encoding="utf-8").read()
        if rt.strip() == "User-agent: *\nAllow: /\n\nSitemap: https://carlocksmithsolihull.co.uk/sitemap.xml":
            ok("robots.txt exact")
        else:
            fail(f"robots.txt differs: {rt!r}")
    else:
        fail("robots.txt missing")
    if os.path.exists(os.path.join(OUT, "llms.txt")):
        ok("llms.txt present")
    else:
        fail("llms.txt missing")
    hdrs = open(os.path.join(OUT, "_headers"), encoding="utf-8").read() if os.path.exists(os.path.join(OUT, "_headers")) else ""
    if "Strict-Transport-Security" in hdrs and "X-Frame-Options: DENY" in hdrs:
        ok("_headers has HSTS + security headers")
    else:
        fail("_headers missing HSTS/security headers")
    red = open(os.path.join(OUT, "_redirects"), encoding="utf-8").read() if os.path.exists(os.path.join(OUT, "_redirects")) else ""
    if "http" in red or "carlocksmithsolihull.co.uk" in red:
        fail("_redirects contains URLs (must be comment-only)")
    else:
        ok("_redirects comment-only")
    root_txt = [f for f in os.listdir(OUT) if f.startswith("__next") and f.endswith(".txt")]
    if root_txt:
        fail(f"build artifacts in out/ root: {root_txt}")
    else:
        ok("no __next.*.txt artifacts in out/ root")
    # noindex only on 404
    noindex_pages = []
    for p in EXPECTED_36:
        if "noindex" in all_html[p]:
            noindex_pages.append(p)
    if noindex_pages:
        fail(f"noindex on indexable pages: {noindex_pages}")
    else:
        ok("no noindex on indexable pages")
    f404 = os.path.join(OUT, "404.html")
    if os.path.exists(f404):
        h404 = open(f404, encoding="utf-8").read()
        if "noindex" in h404:
            ok("404 page noindexed")
        else:
            fail("404 page missing noindex")
        # Next.js 16 emits its own noindex meta on the not-found page PLUS the
        # explicit one from not-found.tsx metadata — expect exactly those two
        # (sister site identical). Both say noindex; crawlers take the strictest.
        meta_noindex = re.findall(r'<meta name="robots" content="([^"]*)"', h404)
        if sorted(meta_noindex) == ["noindex", "noindex, nofollow"]:
            ok("404 has the two expected noindex robots metas (framework + explicit)")
        else:
            fail(f"404 robots metas = {meta_noindex} (want ['noindex', 'noindex, nofollow'])")
    else:
        fail("404.html missing")
    # nosnippet
    if any("nosnippet" in all_html[p] or "max-snippet" in all_html[p] for p in EXPECTED_36):
        fail("nosnippet/max-snippet found")
    else:
        ok("no nosnippet/max-snippet")
    # mixed content
    mixed = [p for p in EXPECTED_36 if re.search(r'(?:src|href)="http://', all_html[p])]
    if mixed:
        fail(f"mixed content http:// links on: {mixed}")
    else:
        ok("no mixed content")
    # og:type
    og_bad = []
    for p in EXPECTED_36:
        h = all_html[p]
        m = re.search(r'<meta property="og:type" content="([^"]+)"', h)
        want = "article" if (p.startswith("/blog/") and p != "/blog/") else "website"
        if not m or m.group(1) != want:
            og_bad.append((p, m.group(1) if m else None, want))
    if og_bad: fail(f"og:type mismatches: {og_bad}")
    else: ok("og:type correct (website except blog posts article)")
    # data-cta-location
    cta_missing = [p for p in EXPECTED_36 if "data-cta-location" not in all_html[p]]
    if cta_missing: fail(f"data-cta-location missing on: {cta_missing}")
    else: ok("data-cta-location present on all pages")
    # file count
    total = sum(len(files) for _, _, files in os.walk(OUT))
    print(f"  info: out/ file count = {total}")

    print()
    print(f"FAILURES: {len(failures)}  WARNINGS: {len(warnings)}")
    for f in failures:
        print(f"  - {f}")
    sys.exit(1 if failures else 0)

if __name__ == "__main__":
    main()
