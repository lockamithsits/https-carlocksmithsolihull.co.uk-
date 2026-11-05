#!/usr/bin/env python3
"""Generate all 36 page.tsx route files for carlocksmithsolihull.co.uk v1.
og:type: "website" everywhere except blog posts ("article") — Phase 2 V-19.
Run from ~/workspace/car-locksmith-solihull/site after content files exist.
"""
import os

SITE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP = os.path.join(SITE_DIR, "src/app")

# (route path, content module, export name, og type)
ROUTES = [
    ("/", "content-home", "homePage", "website"),
    ("/emergency-car-locksmith-solihull/", "content-services", "emergencyPage", "website"),
    ("/locked-out-of-car-solihull/", "content-services", "lockedOutPage", "website"),
    ("/car-key-replacement-solihull/", "content-services", "keyReplacementPage", "website"),
    ("/all-keys-lost-solihull/", "content-services", "allKeysLostPage", "website"),
    ("/spare-car-key-solihull/", "content-services", "spareKeyPage", "website"),
    ("/car-key-programming-solihull/", "content-services", "programmingPage", "website"),
    ("/car-key-fob-replacement-solihull/", "content-services", "fobPage", "website"),
    ("/broken-car-key-extraction-solihull/", "content-services", "brokenKeyPage", "website"),
    ("/ignition-repair-solihull/", "content-services", "ignitionPage", "website"),
    ("/car-door-lock-repair-solihull/", "content-services", "doorLockPage", "website"),
    ("/nec-birmingham-airport-car-park-lockout/", "content-services", "necAirportPage", "website"),
    ("/proof-of-ownership/", "content-utility", "proofOfOwnershipPage", "website"),
    ("/car-locksmith-faq/", "content-utility", "faqHubPage", "website"),
    ("/car-locksmith-prices-solihull/", "content-utility", "pricesPage", "website"),
    ("/areas-we-cover/", "content-areas", "areasHub", "website"),
    ("/car-locksmith-shirley/", "content-areas", "shirleyPage", "website"),
    ("/car-locksmith-knowle/", "content-areas", "knowlePage", "website"),
    ("/car-locksmith-dorridge/", "content-areas", "dorridgePage", "website"),
    ("/car-locksmith-olton/", "content-areas", "oltonPage", "website"),
    ("/car-locksmith-hockley-heath/", "content-areas", "hockleyHeathPage", "website"),
    ("/car-locksmith-balsall-common/", "content-areas", "balsallCommonPage", "website"),
    ("/car-locksmith-meriden/", "content-areas", "meridenPage", "website"),
    ("/car-locksmith-chelmsley-wood/", "content-areas", "chelmsleyWoodPage", "website"),
    ("/car-locksmith-hampton-in-arden/", "content-areas", "hamptonInArdenPage", "website"),
    ("/car-locksmith-elmdon/", "content-areas", "elmdonPage", "website"),
    ("/car-locksmith-castle-bromwich/", "content-areas", "castleBromwichPage", "website"),
    ("/car-locksmith-marston-green/", "content-areas", "marstonGreenPage", "website"),
    ("/about/", "content-utility", "aboutPage", "website"),
    ("/contact/", "content-utility", "contactPage", "website"),
    ("/privacy/", "content-utility", "privacyPage", "website"),
    ("/reviews/", "content-utility", "reviewsPage", "website"),
    ("/blog/", "content-blog", "blogHub", "website"),
    ("/blog/how-much-does-a-car-key-replacement-cost/", "content-blog", "blogCostPost", "article"),
    ("/blog/why-wont-my-key-fob-work/", "content-blog", "blogFobPost", "article"),
    ("/blog/locked-out-of-your-car-what-to-do/", "content-blog", "blogLockoutPost", "article"),
]

TEMPLATE = '''import type {{ Metadata }} from "next";
import {{ PageShell }} from "@/components/PageShell";
import {{ canonical, SITE }} from "@/lib/site";
import {{ {export} }} from "@/lib/{module}";

const data = {export};

const OG_IMAGE = {{ url: "/og-image.png", width: 1200, height: 630, alt: SITE.name }};

export const metadata: Metadata = {{
  title: data.title,
  description: data.description,
  alternates: {{ canonical: canonical(data.path) }},
  openGraph: {{
    title: data.title,
    description: data.description,
    url: canonical(data.path),
    siteName: SITE.name,
    type: "{ogtype}",
    locale: "en_GB",
    images: [OG_IMAGE],
  }},
  twitter: {{ card: "summary_large_image", images: ["/og-image.png"] }},
}};

export default function Page() {{
  return <PageShell {{...data}} />;
}}
'''

def route_dir(path: str) -> str:
    if path == "/":
        return APP
    return os.path.join(APP, path.strip("/"))

def main():
    assert len(ROUTES) == 36, f"expected 36 routes, got {len(ROUTES)}"
    for path, module, export, ogtype in ROUTES:
        d = route_dir(path)
        os.makedirs(d, exist_ok=True)
        content = TEMPLATE.format(export=export, module=module, ogtype=ogtype)
        with open(os.path.join(d, "page.tsx"), "w") as f:
            f.write(content)
        print(f"wrote {path} -> {export} ({ogtype})")
    print("36 page.tsx files generated.")

if __name__ == "__main__":
    main()
