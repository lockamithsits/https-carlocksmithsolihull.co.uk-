import type { ReactNode } from "react";
import Link from "next/link";
import { SITE, AREAS, LAST_UPDATED, LAST_UPDATED_DISPLAY } from "@/lib/site";
import { Faq } from "./Faq";
import type { PageData } from "@/lib/page-data";

/**
 * Renders strings with inline [anchor text](/path/) markdown links as real
 * links. Non-string nodes pass through untouched.
 */
function RichText({ text }: { text: ReactNode }) {
  if (typeof text !== "string") return <>{text}</>;
  const parts: ReactNode[] = [];
  const re = /\[([^\]]+)\]\(([^)]+)\)/g;
  let last = 0;
  let m: RegExpExecArray | null;
  let k = 0;
  while ((m = re.exec(text)) !== null) {
    if (m.index > last) parts.push(text.slice(last, m.index));
    const href = m[2];
    const label = m[1];
    parts.push(
      href.startsWith("http") ? (
        <a key={k++} href={href} target="_blank" rel="noopener">
          {label}
        </a>
      ) : (
        <Link key={k++} href={href}>
          {label}
        </Link>
      ),
    );
    last = m.index + m[0].length;
  }
  if (last < text.length) parts.push(text.slice(last));
  return <>{parts}</>;
}

export function jsonLdFor(path: string, crumbs: PageData["crumbs"]) {
  // Pure "Locksmith" type ONLY (Phase 4 §1.3 / Phase 8 §1.2 resolution).
  // Never stack "AutomotiveBusiness" — the automotive nature is expressed
  // in content, service names and areaServed, not by stacking types.
  const org = {
    "@context": "https://schema.org",
    "@type": "Locksmith",
    "@id": SITE.entityId,
    name: SITE.name,
    url: SITE.domain + "/",
    telephone: SITE.tel,
    // No street address: service-area business (owner supplied no address) — never invent one.
    description:
      "Mobile car locksmith in Solihull, West Midlands — open 24 hours. Car lockouts, lost keys, key replacement, key programming, key fob repair and ignition repair at your car.",
    // Verified entity references (Wikipedia — informational only, names only, no sameAs).
    about: [
      { "@type": "Thing", name: "Car locksmith" },
      { "@type": "Place", name: "Solihull" },
    ],
    openingHoursSpecification: [
      {
        "@type": "OpeningHoursSpecification",
        dayOfWeek: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        opens: "00:00",
        closes: "23:59",
      },
    ],
    areaServed: [
      { "@type": "Place", name: `Solihull, West Midlands` },
      ...AREAS.map((a) => ({ "@type": "Place", name: `${a.name}, ${a.region}` })),
    ],
    knowsAbout: [
      "Car key replacement",
      "Emergency car lockout",
      "Car key programming",
      "Car key cutting",
      "Key fob repair",
      "Key fob replacement",
      "Broken car key extraction",
      "Ignition repair",
      "Car door lock repair",
    ],
  };
  const crumbsLd = {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    itemListElement: crumbs.map((c, i) => ({
      "@type": "ListItem",
      position: i + 1,
      name: c.name,
      item: SITE.domain + c.path,
    })),
  };
  return [org, crumbsLd];
}

export function PageShell({
  path,
  crumbs,
  h1,
  description,
  answer,
  takeaways,
  intro,
  sections,
  faqs,
  related,
  service,
  howTo,
  children,
}: PageData & { children?: ReactNode }) {
  const [org, crumbsLd] = jsonLdFor(path, crumbs);
  const pagePath = path;
  const isBlogPost = pagePath.startsWith("/blog/") && pagePath !== "/blog/";
  const isHome = pagePath === "/";
  const webPageLd = {
    "@context": "https://schema.org",
    "@type": "WebPage",
    "@id": SITE.domain + pagePath,
    url: SITE.domain + pagePath,
    name: h1,
    description,
    inLanguage: "en-GB",
    dateModified: LAST_UPDATED,
    isPartOf: { "@id": `${SITE.domain}/#website` },
  };
  const webSiteLd = isHome
    ? {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "@id": `${SITE.domain}/#website`,
        url: SITE.domain + "/",
        name: SITE.name,
        inLanguage: "en-GB",
      }
    : null;
  const serviceLd = service
    ? {
        "@context": "https://schema.org",
        "@type": "Service",
        name: service.name,
        serviceType: service.serviceType,
        description,
        provider: { "@id": SITE.entityId },
        areaServed: { "@type": "Place", name: "Solihull, West Midlands" },
      }
    : null;
  const articleLd = isBlogPost
    ? {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        headline: h1,
        description,
        author: {
          "@type": "Organization",
          name: SITE.name,
          url: SITE.domain + "/",
        },
        publisher: {
          "@type": "Organization",
          name: SITE.name,
          url: SITE.domain + "/",
        },
        mainEntityOfPage: SITE.domain + pagePath,
        datePublished: LAST_UPDATED,
        dateModified: LAST_UPDATED,
        inLanguage: "en-GB",
      }
    : null;
  const howToLd = howTo
    ? {
        "@context": "https://schema.org",
        "@type": "HowTo",
        name: howTo.name,
        step: howTo.steps.map((s, i) => ({
          "@type": "HowToStep",
          position: i + 1,
          text: s,
        })),
      }
    : null;
  return (
    <article className="prose-article">
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(org) }} />
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(crumbsLd) }} />
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(webPageLd) }} />
      {webSiteLd && (
        <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(webSiteLd) }} />
      )}
      {serviceLd && (
        <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(serviceLd) }} />
      )}
      {articleLd && (
        <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(articleLd) }} />
      )}
      {howToLd && (
        <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(howToLd) }} />
      )}
      <nav aria-label="Breadcrumb" className="text-sm text-slate-500">
        {crumbs.map((c, i) => (
          <span key={c.path}>
            {i > 0 && " / "}
            {i < crumbs.length - 1 ? (
              <Link href={c.path} className="hover:text-orange-700">
                {c.name}
              </Link>
            ) : (
              <span aria-current="page">{c.name}</span>
            )}
          </span>
        ))}
      </nav>
      <h1>{h1}</h1>
      {answer && <p className="answer-box">{answer}</p>}
      {takeaways && takeaways.length > 0 && (
        <aside className="takeaways-box" aria-label="Key takeaways">
          <p className="takeaways-title">Key takeaways</p>
          <ul>
            {takeaways.map((t, i) => (
              <li key={i}>
                <RichText text={t} />
              </li>
            ))}
          </ul>
        </aside>
      )}
      {intro.map((p, i) => (
        <p key={i} className="lead">
          <RichText text={p} />
        </p>
      ))}
      <div className="cta-row">
        <a href={SITE.telHref} data-cta-location="content_cta" className="cta-call">
          Call {SITE.telDisplay}
        </a>
        <a
          href={SITE.whatsapp}
          target="_blank"
          rel="noopener"
          data-cta-location="content_cta"
          className="cta-whatsapp"
        >
          WhatsApp Us
        </a>
      </div>
      <p className="trust-line">
        Open 24 hours · Fully mobile · Clear quote before any work starts
      </p>
      {children}
      {sections.map((s) => (
        <section key={s.h}>
          <h2>{s.h}</h2>
          {s.paras.map((p, i) => (
            <p key={i}>
              <RichText text={p} />
            </p>
          ))}
          {s.bullets && (
            <ul>
              {s.bullets.map((b) => (
                <li key={b}>
                  <RichText text={b} />
                </li>
              ))}
            </ul>
          )}
          {s.table && (
            <div className="table-wrap">
              <table>
                <thead>
                  <tr>
                    {s.table.head.map((h, i) => (
                      <th key={i}>{h}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {s.table.rows.map((row, i) => (
                    <tr key={i}>
                      {row.map((cell, j) => (
                        <td key={j}>
                          <RichText text={cell} />
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
          {s.links && (
            <ul className="link-list">
              {s.links.map((l) => (
                <li key={l.href}>
                  {l.href.startsWith("http") ? (
                    <a href={l.href} target="_blank" rel="noopener">
                      {l.label}
                    </a>
                  ) : (
                    <Link href={l.href}>{l.label}</Link>
                  )}
                  {l.note ? ` — ${l.note}` : ""}
                </li>
              ))}
            </ul>
          )}
          {s.mapEmbed && (
            <div
              className="map-embed"
              style={{ width: "100%", aspectRatio: "4 / 3", marginTop: "1rem" }}
            >
              <iframe
                src={s.mapEmbed.src}
                title={s.mapEmbed.title}
                style={{ width: "100%", height: "100%", border: 0 }}
                allowFullScreen
                loading="lazy"
                referrerPolicy="strict-origin-when-cross-origin"
              />
            </div>
          )}
        </section>
      ))}
      <section className="related">
        <h2>Related pages</h2>
        <ul>
          {related.map((r) => (
            <li key={r.href}>
              <Link href={r.href}>{r.label}</Link>
            </li>
          ))}
        </ul>
      </section>
      <Faq faqs={faqs} />
      <p className="mt-8 text-sm text-slate-500">Last updated: {LAST_UPDATED_DISPLAY}</p>
    </article>
  );
}
