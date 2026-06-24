import type { MetadataRoute } from "next";

export const dynamic = "force-static";

const BASE = "https://nexia-ia-com.netlify.app";

export default function sitemap(): MetadataRoute.Sitemap {
  return [
    { url: `${BASE}/`,            changeFrequency: "weekly",  priority: 1.0 },
    { url: `${BASE}/#servicios`,  changeFrequency: "monthly", priority: 0.8 },
    { url: `${BASE}/#proceso`,    changeFrequency: "monthly", priority: 0.7 },
    { url: `${BASE}/#fundador`,   changeFrequency: "weekly",  priority: 0.9 },
    { url: `${BASE}/#contacto`,   changeFrequency: "monthly", priority: 0.8 },
  ];
}
