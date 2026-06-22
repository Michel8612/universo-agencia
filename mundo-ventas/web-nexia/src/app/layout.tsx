import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "NEXIA — Agencia de Inteligencia Artificial",
  description: "Automatizamos tu negocio con IA: chatbots, apps, redes sociales y más. Consulta gratuita.",
  keywords: "agencia IA, inteligencia artificial, chatbot, automatización, marketing digital",
  openGraph: {
    title: "NEXIA — Tu negocio trabajando 24/7 con IA",
    description: "Chatbots, apps, redes sociales y ciberseguridad con inteligencia artificial.",
    type: "website",
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es">
      <body className="antialiased">{children}</body>
    </html>
  );
}
