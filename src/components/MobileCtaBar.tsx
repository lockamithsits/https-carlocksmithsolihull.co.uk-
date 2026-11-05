import { SITE } from "@/lib/site";

/**
 * Call + WhatsApp sticky bar (mobile). Footer and main carry bottom
 * padding so the bar never covers content or CTAs.
 */
export function MobileCtaBar() {
  return (
    <div className="fixed inset-x-0 bottom-0 z-50 flex pb-[env(safe-area-inset-bottom)] md:hidden">
      <a
        href={SITE.telHref}
        data-cta-location="sticky_bar"
        className="block flex-1 bg-[#d32f2f] py-4 text-center text-lg font-bold text-white"
      >
        Call Now
      </a>
      <a
        href={SITE.whatsapp}
        target="_blank"
        rel="noopener"
        data-cta-location="sticky_bar"
        className="block flex-1 bg-[#16a34a] py-4 text-center text-lg font-bold text-white"
      >
        WhatsApp
      </a>
    </div>
  );
}
