import type { Metadata } from "next";
import "./globals.css";

const SITE = "https://nexia-ia-com.netlify.app";

export const metadata: Metadata = {
  metadataBase: new URL(SITE),
  title: {
    default: "NEXIA — Agencia de IA, Webs y Automatización para Pymes",
    template: "%s | NEXIA",
  },
  description:
    "Webs profesionales, chatbots con IA y automatización para pymes y negocios locales. Diagnóstico web gratuito en 24h. Programa fundador con 50% de descuento.",
  keywords: [
    "agencia de IA", "agencia inteligencia artificial", "diseño web pymes",
    "chatbot IA", "automatización negocios", "página web profesional",
    "diagnóstico web gratis", "marketing digital", "desarrollo web",
  ],
  authors: [{ name: "NEXIA" }],
  creator: "NEXIA",
  alternates: { canonical: SITE },
  openGraph: {
    type: "website",
    locale: "es_ES",
    url: SITE,
    siteName: "NEXIA",
    title: "NEXIA — Tu negocio trabajando 24/7 con IA",
    description:
      "Webs, chatbots e IA para pymes. Te hacemos un diagnóstico gratuito de tu web y te decimos exactamente qué mejorar. Programa fundador 50% dto.",
    images: [{ url: "/og.svg", width: 1200, height: 630, alt: "NEXIA — Agencia de IA" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "NEXIA — Agencia de IA para pymes",
    description: "Webs, chatbots e IA. Diagnóstico web gratis. Programa fundador 50% dto.",
    images: ["/og.svg"],
  },
  robots: {
    index: true,
    follow: true,
    googleBot: { index: true, follow: true, "max-image-preview": "large" },
  },
  icons: { icon: "/favicon.svg" },
  verification: {
    google: "q7V4_l7w6znPwtQMvmTyZFMKX2TIewfw9Q2TH7OSxkI",
  },
};

const JSONLD = {
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  name: "NEXIA",
  description:
    "Agencia de inteligencia artificial, desarrollo web y automatización para pymes y negocios locales.",
  url: SITE,
  email: "teamorionglobal@gmail.com",
  areaServed: ["ES", "Spain", "LATAM"],
  serviceType: [
    "Diseño web", "Chatbots con IA", "Automatización", "Marketing digital",
    "SEO", "E-commerce", "Mantenimiento web",
  ],
  priceRange: "€€",
  offers: {
    "@type": "Offer",
    name: "Programa Fundador",
    description: "50% de descuento para los primeros 3 clientes fundadores.",
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es">
      <head>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(JSONLD) }}
        />
      </head>
      <body className="antialiased">{children}</body>
    </html>
  );
}
