export type FaqItem = { q: string; a: string };

/**
 * Visible FAQ text and FAQPage JSON-LD render from the SAME faq array,
 * so the structured data byte-matches the visible text exactly.
 * FAQ wording avoids apostrophes/contractions so React's HTML escaping
 * cannot diverge from the JSON-LD strings.
 */
export function Faq({ faqs }: { faqs: FaqItem[] }) {
  if (faqs.length === 0) return null;
  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    mainEntity: faqs.map((f) => ({
      "@type": "Question",
      name: f.q,
      acceptedAnswer: { "@type": "Answer", text: f.a },
    })),
  };
  return (
    <section aria-label="Frequently asked questions" className="mt-12">
      <h2>Frequently asked questions</h2>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <div className="mt-4 space-y-6">
        {faqs.map((f) => (
          <div key={f.q}>
            <h3>{f.q}</h3>
            <p>{f.a}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
