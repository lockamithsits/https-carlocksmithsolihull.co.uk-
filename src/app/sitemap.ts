import type { MetadataRoute } from "next";
import { statSync } from "node:fs";
import { join } from "node:path";
import { SITE } from "@/lib/site";
import { homePage } from "@/lib/content-home";
import { servicePages } from "@/lib/content-services";
import { areasHub, areaPages } from "@/lib/content-areas";
import { blogHub, blogCostPost, blogFobPost, blogLockoutPost } from "@/lib/content-blog";
import {
  aboutPage,
  contactPage,
  privacyPage,
  reviewsPage,
  proofOfOwnershipPage,
  faqHubPage,
  pricesPage,
} from "@/lib/content-utility";
import type { PageData } from "@/lib/page-data";

export const dynamic = "force-static";

/**
 * lastmod from the page source file's actual mtime at build time
 * (Phase 2 §3.1 — never a hardcoded single date for all URLs).
 * Route dir matches the URL slug for every v1 page.
 */
function sourceFileFor(path: string): string {
  if (path === "/") return join(process.cwd(), "src/app/page.tsx");
  const clean = path.replace(/^\/|\/$/g, "");
  return join(process.cwd(), "src/app", clean, "page.tsx");
}

function lastModifiedFor(page: PageData): Date {
  try {
    return statSync(sourceFileFor(page.path)).mtime;
  } catch {
    return new Date("2026-11-05");
  }
}

export default function sitemap(): MetadataRoute.Sitemap {
  const pages: PageData[] = [
    homePage,
    ...servicePages,
    areasHub,
    ...areaPages,
    aboutPage,
    contactPage,
    privacyPage,
    reviewsPage,
    proofOfOwnershipPage,
    faqHubPage,
    pricesPage,
    blogHub,
    blogCostPost,
    blogFobPost,
    blogLockoutPost,
  ];
  return pages.map((p) => ({
    url: `${SITE.domain}${p.path}`,
    lastModified: lastModifiedFor(p),
  }));
}
