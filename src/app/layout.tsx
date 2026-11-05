import type { Metadata, Viewport } from "next";
import Script from "next/script";
import { SITE, GSC_META, GTM_ID } from "@/lib/site";
import { Header } from "@/components/Header";
import { Footer } from "@/components/Footer";
import { MobileCtaBar } from "@/components/MobileCtaBar";
import "./globals.css";
import "./article.css";

export const metadata: Metadata = {
  metadataBase: new URL(SITE.domain),
  // GSC verification — owner-supplied 2026-11-05 (meta + HTML file both baked).
  ...(GSC_META ? { verification: { google: GSC_META } } : {}),
  title: "Car Locksmith Solihull | 24/7 Car Keys | 07367 634032",
  description:
    "Locked out or lost your car keys in Solihull? Mobile car locksmith, 24 hours. Call or WhatsApp 07367 634032 for a clear quote before work starts.",
  openGraph: {
    siteName: SITE.name,
    type: "website",
    locale: "en_GB",
    images: [{ url: "/og-image.png", width: 1200, height: 630, alt: SITE.name }],
  },
  twitter: { card: "summary_large_image", images: ["/og-image.png"] },
  icons: {
    icon: [
      { url: "/favicon.ico", sizes: "any" },
      { url: "/favicon-16x16.png", sizes: "16x16", type: "image/png" },
      { url: "/favicon-32x32.png", sizes: "32x32", type: "image/png" },
    ],
    apple: [{ url: "/apple-touch-icon.png", sizes: "180x180", type: "image/png" }],
  },
  manifest: "/site.webmanifest",
};

export const viewport: Viewport = {
  themeColor: "#14324a",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en-GB">
      <head>
        <Script
          id="gtm-script"
          strategy="beforeInteractive"
          dangerouslySetInnerHTML={{
            __html: `(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','${GTM_ID}');`,
          }}
        />
      </head>
      <body>
        <noscript>
          <iframe
            src={`https://www.googletagmanager.com/ns.html?id=${GTM_ID}`}
            height="0"
            width="0"
            style={{ display: "none", visibility: "hidden" }}
          />
        </noscript>
        <Header />
        <main className="mx-auto max-w-6xl px-4 pb-28 pt-6 sm:px-6 md:pb-12">{children}</main>
        <Footer />
        <MobileCtaBar />
      </body>
    </html>
  );
}
