import type { Metadata } from "next";
import { PageShell } from "@/components/PageShell";
import { canonical, SITE } from "@/lib/site";
import { brokenKeyPage } from "@/lib/content-services";

const data = brokenKeyPage;

const OG_IMAGE = { url: "/og-image.png", width: 1200, height: 630, alt: SITE.name };

export const metadata: Metadata = {
  title: data.title,
  description: data.description,
  alternates: { canonical: canonical(data.path) },
  openGraph: {
    title: data.title,
    description: data.description,
    url: canonical(data.path),
    siteName: SITE.name,
    type: "website",
    locale: "en_GB",
    images: [OG_IMAGE],
  },
  twitter: { card: "summary_large_image", images: ["/og-image.png"] },
};

export default function Page() {
  return <PageShell {...data} />;
}
