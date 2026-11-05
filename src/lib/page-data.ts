import type { ReactNode } from "react";
import type { FaqItem } from "@/components/Faq";

export type Crumb = { name: string; path: string };
export type Section = {
  h: string;
  paras: string[];
  bullets?: string[];
  links?: Array<{ href: string; label: string; note?: string }>;
  /** Responsive Google Maps embed rendered at the end of the section. */
  mapEmbed?: { src: string; title: string };
  /** Comparison table rendered after paras/bullets. */
  table?: { head: string[]; rows: string[][] };
};

export type ServiceBlock = {
  /** Display name of the service, e.g. "Emergency Car Locksmith in Solihull". */
  name: string;
  /** Short service type, e.g. "Emergency car locksmith service". */
  serviceType: string;
};

export type HowToBlock = {
  /** HowTo name, e.g. "What to do when locked out of your car". */
  name: string;
  /** Ordered steps (plain-language actions a person takes — never bypass methods). */
  steps: string[];
};

export type PageData = {
  path: string;
  title: string;
  description: string;
  h1: string;
  /** Service JSON-LD (Phase 8 §5) — present on service + area pages only. */
  service?: ServiceBlock;
  /** HowTo JSON-LD (Phase 8 §9) — present only on genuine how-to blog posts. */
  howTo?: HowToBlock;
  /** Direct-answer block (40-60 words) rendered right after the H1 for AEO/AIO. */
  answer?: string;
  /** Key-takeaways box rendered after the answer (blog posts). */
  takeaways?: string[];
  /** Intro paragraphs. Plain strings everywhere except the homepage, which
   * uses inline contextual links (ReactNode) for the semantic anchor strategy. */
  intro: ReactNode[];
  sections: Section[];
  faqs: FaqItem[];
  related: Array<{ href: string; label: string }>;
  crumbs: Crumb[];
  ogTitle?: string;
};
