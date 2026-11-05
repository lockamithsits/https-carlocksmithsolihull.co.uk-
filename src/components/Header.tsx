import Link from "next/link";
import { SITE } from "@/lib/site";

const NAV: Array<{ href: string; label: string }> = [
  { href: "/emergency-car-locksmith-solihull/", label: "Emergency" },
  { href: "/car-key-replacement-solihull/", label: "Key Replacement" },
  { href: "/car-key-programming-solihull/", label: "Programming" },
  { href: "/areas-we-cover/", label: "Areas" },
  { href: "/reviews/", label: "Reviews" },
  { href: "/blog/", label: "Blog" },
  { href: "/contact/", label: "Contact" },
];

export function Header() {
  return (
    <header className="bg-[#14324a] text-white">
      <div className="mx-auto flex max-w-6xl flex-wrap items-center gap-x-6 gap-y-3 px-4 py-4 sm:px-6">
        <Link href="/" className="flex items-center gap-3" aria-label="Home">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img src="/logo.svg" alt="Car Locksmith Solihull logo" width="180" height="45" />
          <span className="leading-tight">
            <span className="block text-lg font-bold">Car Locksmith Solihull</span>
            <span className="block text-xs font-semibold tracking-widest text-amber-300">
              CAR KEYS &amp; LOCKOUTS · OPEN 24 HOURS
            </span>
          </span>
        </Link>
        <nav aria-label="Main" className="flex flex-wrap gap-x-5 gap-y-2 text-sm font-medium">
          {NAV.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className="inline-block min-h-[44px] content-center py-2 hover:text-amber-300"
            >
              {item.label}
            </Link>
          ))}
        </nav>
        <div className="ml-auto flex flex-wrap gap-2">
          <a
            href={SITE.telHref}
            data-cta-location="header"
            className="inline-block rounded-full bg-amber-500 px-5 py-3 text-sm font-bold text-[#14324a] hover:bg-amber-400"
          >
            Call {SITE.telDisplay}
          </a>
          <a
            href={SITE.whatsapp}
            target="_blank"
            rel="noopener"
            data-cta-location="header"
            className="inline-block rounded-full bg-green-600 px-5 py-3 text-sm font-bold text-white hover:bg-green-500"
          >
            WhatsApp
          </a>
        </div>
      </div>
    </header>
  );
}
