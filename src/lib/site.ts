export const SITE = {
  name: "Car Locksmith Solihull",
  domain: "https://carlocksmithsolihull.co.uk",
  tel: "+447367634032",
  telDisplay: "07367 634032",
  telHref: "tel:+447367634032",
  whatsapp: "https://wa.me/447367634032",
  locality: "Solihull",
  city: "West Midlands",
  postcode: "B91",
  // NO ADDRESS: service-area business (owner supplied no address) — never invent one.
  // Map embeds are service-area framing only, never presented as a business location.
  /** Entity home @id for the Locksmith schema — every service page references this as provider. */
  entityId: "https://carlocksmithsolihull.co.uk/#locksmith",
};

export function canonical(path: string): string {
  return `${SITE.domain}${path}`;
}

/** Google Search Console verification — owner-supplied 2026-11-05 (meta + HTML file both baked). */
export const GSC_META = "evUqxPEx6hweGprFgsMcFNyP7aopv_8SOM2UfWVQ-6I";
export const GSC_FILE = "googleb7d79ba7b0fa42b4.html";

/** Google Tag Manager container — owner-supplied 2026-11-05 (Phase 10 spec). */
export const GTM_ID = "GTM-N7QTF8Q3";

/** Last-updated date shown on every page and in schema dateModified (v1 launch date). */
export const LAST_UPDATED = "2026-11-05";
export const LAST_UPDATED_DISPLAY = "5 November 2026";

export const AREAS = [
  { slug: "shirley", name: "Shirley", postcode: "B90", region: "West Midlands" },
  { slug: "knowle", name: "Knowle", postcode: "B93", region: "West Midlands" },
  { slug: "dorridge", name: "Dorridge", postcode: "B93", region: "West Midlands" },
  { slug: "olton", name: "Olton", postcode: "B92", region: "West Midlands" },
  { slug: "hockley-heath", name: "Hockley Heath", postcode: "B94", region: "West Midlands" },
  { slug: "balsall-common", name: "Balsall Common", postcode: "CV7", region: "West Midlands" },
  { slug: "meriden", name: "Meriden", postcode: "CV7", region: "West Midlands" },
  { slug: "chelmsley-wood", name: "Chelmsley Wood", postcode: "B37", region: "West Midlands" },
  { slug: "hampton-in-arden", name: "Hampton-in-Arden", postcode: "B92", region: "West Midlands" },
  { slug: "elmdon", name: "Elmdon", postcode: "B37", region: "West Midlands" },
  { slug: "castle-bromwich", name: "Castle Bromwich", postcode: "B36", region: "West Midlands" },
  { slug: "marston-green", name: "Marston Green", postcode: "B37", region: "West Midlands" },
] as const;

export const SERVICE_PAGES = [
  { href: "/emergency-car-locksmith-solihull/", label: "Emergency Car Locksmith Solihull" },
  { href: "/locked-out-of-car-solihull/", label: "Locked Out of Car Solihull" },
  { href: "/car-key-replacement-solihull/", label: "Car Key Replacement Solihull" },
  { href: "/all-keys-lost-solihull/", label: "All Keys Lost Solihull" },
  { href: "/spare-car-key-solihull/", label: "Spare Car Key Solihull" },
  { href: "/car-key-programming-solihull/", label: "Car Key Programming Solihull" },
  { href: "/car-key-fob-replacement-solihull/", label: "Key Fob Replacement Solihull" },
  { href: "/broken-car-key-extraction-solihull/", label: "Broken Car Key Extraction Solihull" },
  { href: "/ignition-repair-solihull/", label: "Ignition Repair Solihull" },
  { href: "/car-door-lock-repair-solihull/", label: "Car Door Lock Repair Solihull" },
  { href: "/nec-birmingham-airport-car-park-lockout/", label: "NEC & Airport Car Park Lockout" },
] as const;
