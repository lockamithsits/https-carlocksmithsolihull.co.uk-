import type { Metadata } from "next";
import Link from "next/link";
import { SITE } from "@/lib/site";

export const metadata: Metadata = {
  robots: { index: false, follow: false },
  title: "Page Not Found | 07367 634032",
  description:
    "This page does not exist. Car Locksmith Solihull is open 24 hours — call or WhatsApp 07367 634032.",
};

export default function NotFound() {
  return (
    <article className="prose-article">
      <h1>Wrong turn — this page is not here</h1>
      <p className="lead">
        The link you followed leads nowhere on this site. If you have a car key
        or lock problem, do not waste time hunting — get straight through to us.
      </p>
      <div className="cta-row">
        <a href={SITE.telHref} data-cta-location="not_found" className="cta-call">
          Call {SITE.telDisplay}
        </a>
        <a
          href={SITE.whatsapp}
          target="_blank"
          rel="noopener"
          data-cta-location="not_found"
          className="cta-whatsapp"
        >
          WhatsApp Us
        </a>
      </div>
      <p>
        <Link href="/">Back to the home page</Link>
      </p>
    </article>
  );
}
