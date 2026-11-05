import Link from "next/link";
import { SITE, SERVICE_PAGES, AREAS } from "@/lib/site";

export function Footer() {
  return (
    <footer className="bg-[#14324a] pb-28 text-slate-100 md:pb-8">
      <div className="mx-auto grid max-w-6xl gap-8 px-4 py-10 sm:grid-cols-3 sm:px-6">
        <div>
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img src="/logo.svg" alt="Car Locksmith Solihull logo" width="200" height="50" className="mb-3" />
          <p className="text-lg font-bold text-white">{SITE.name}</p>
          <p className="mt-2 text-sm leading-relaxed">
            Mobile car locksmith serving Solihull and the surrounding West
            Midlands towns and villages, 24 hours a day. Car lockouts, lost
            keys, key replacement, key programming and ignition repair — we
            come to you.
          </p>
        </div>
        <nav aria-label="Footer services">
          <p className="font-bold text-white">Services</p>
          <ul className="mt-2 space-y-1 text-sm">
            {SERVICE_PAGES.map((s) => (
              <li key={s.href}>
                <Link href={s.href} className="hover:text-amber-400">
                  {s.label}
                </Link>
              </li>
            ))}
            <li>
              <Link href="/areas-we-cover/" className="hover:text-amber-400">
                Areas we cover
              </Link>
            </li>
            <li>
              <Link href="/reviews/" className="hover:text-amber-400">
                Reviews
              </Link>
            </li>
            <li>
              <Link href="/blog/" className="hover:text-amber-400">
                Blog
              </Link>
            </li>
          </ul>
        </nav>
        <div>
          <p className="font-bold text-white">Where We Cover</p>
          <p className="mt-2 text-sm leading-relaxed">
            We cover{" "}
            <Link href="/" className="hover:text-amber-400">
              Solihull (B91/B92)
            </Link>{" "}
            and nearby areas including{" "}
            {AREAS.slice(0, 8).map((a, i, arr) => (
              <span key={a.slug}>
                <Link href={`/car-locksmith-${a.slug}/`} className="hover:text-amber-400">
                  {a.name}
                </Link>{" "}
                ({a.postcode}){i < arr.length - 1 ? ", " : ""}
              </span>
            ))}
            .
          </p>
          <p className="mt-3 text-sm">
            <Link href="/areas-we-cover/" className="hover:text-amber-400">
              See all areas we cover
            </Link>
          </p>
          <p className="mt-4 font-bold text-white">Contact — 24/7</p>
          <ul className="mt-2 space-y-1 text-sm">
            <li>
              <a href={SITE.telHref} data-cta-location="footer" className="hover:text-amber-400">
                Call {SITE.telDisplay}
              </a>
            </li>
            <li>
              <a
                href={SITE.whatsapp}
                target="_blank"
                rel="noopener"
                data-cta-location="footer"
                className="hover:text-amber-400"
              >
                WhatsApp {SITE.telDisplay}
              </a>
            </li>
            {/* Service-area business — fully mobile, no shop counter, no address to display. */}
            <li className="text-slate-300">
              <span className="font-semibold text-white">Coverage: </span>
              Solihull &amp; West Midlands, 24/7
            </li>
            <li>
              <Link href="/contact/" className="hover:text-amber-400">
                Contact details
              </Link>
            </li>
            <li>
              <Link href="/about/" className="hover:text-amber-400">
                About us
              </Link>
            </li>
            <li>
              <Link href="/privacy/" className="hover:text-amber-400">
                Privacy policy
              </Link>
            </li>
          </ul>
        </div>
      </div>
      <div className="mx-auto max-w-6xl px-4 sm:px-6">
        <p className="border-t border-white/15 pt-4 text-xs text-slate-300">
          © {new Date().getFullYear()} Car Locksmith Solihull. All rights reserved. ·
          Last updated: 5 November 2026
        </p>
      </div>
    </footer>
  );
}
