"use client";
import { useState } from "react";

const EMAIL_DESTINO = "romeliskids@gmail.com"; // cambia cuando tengas hola@nexia.io

const NAV_LINKS = [
  { label: "Servicios", href: "#servicios" },
  { label: "Casos de éxito", href: "#casos" },
  { label: "Precios", href: "#precios" },
  { label: "Contacto", href: "#contacto" },
];

const SERVICIOS = [
  {
    icon: "🤖",
    titulo: "Chatbots con IA",
    desc: "Atención al cliente 24/7 entrenada con los datos de tu negocio. Atiende, vende y agenda sin empleados extra.",
    precio: "desde 497€",
    tag: "Más vendido",
    detalle: "Setup en 7 días",
  },
  {
    icon: "💻",
    titulo: "Apps y Sistemas a Medida",
    desc: "Tu idea convertida en producto real. Frontend, backend, base de datos y deploy incluido desde el día 1.",
    precio: "desde 1.497€",
    tag: null,
    detalle: "Entrega en 3 semanas",
  },
  {
    icon: "📱",
    titulo: "Gestión de Redes con IA",
    desc: "Publicamos contenido de calidad cada día en todas tus redes. Tú solo apruebas lo que quieres publicar.",
    precio: "desde 497€/mes",
    tag: "Recurrente",
    detalle: "30 posts/mes incluidos",
  },
  {
    icon: "🎬",
    titulo: "Producción de Vídeo IA",
    desc: "Vídeos personalizados para redes sociales generados con inteligencia artificial. Reels, Shorts y más.",
    precio: "desde 297€/mes",
    tag: "Nuevo",
    detalle: "10 vídeos/mes",
  },
  {
    icon: "📈",
    titulo: "SEO + Contenido",
    desc: "Posicionamiento orgánico real. Artículos optimizados generados por IA y publicados automáticamente.",
    precio: "desde 297€/mes",
    tag: null,
    detalle: "8 artículos/mes",
  },
  {
    icon: "🔒",
    titulo: "Ciberseguridad",
    desc: "Auditorías LOPD/GDPR y test de vulnerabilidades. Cumple la ley y protege tu negocio de ataques.",
    precio: "desde 797€",
    tag: null,
    detalle: "Informe en 5 días",
  },
];

const PAQUETES = [
  {
    nombre: "Starter",
    precio: "497€",
    periodo: "pago único",
    color: "border-gray-700",
    btnColor: "bg-gray-700 hover:bg-gray-600",
    items: [
      "Landing page profesional",
      "Chatbot de atención básico",
      "Integración WhatsApp",
      "Panel de control",
      "Entrega en 5 días",
    ],
    popular: false,
  },
  {
    nombre: "Growth",
    precio: "1.497€",
    periodo: "+ 297€/mes",
    color: "border-blue-500",
    btnColor: "bg-blue-600 hover:bg-blue-500",
    items: [
      "App web completa (5 módulos)",
      "Dashboard de métricas",
      "Chatbot avanzado con IA",
      "Gestión de redes (30 posts/mes)",
      "Soporte prioritario",
      "Entrega en 3 semanas",
    ],
    popular: true,
  },
  {
    nombre: "Agency Pro",
    precio: "4.997€",
    periodo: "+ 997€/mes",
    color: "border-purple-500",
    btnColor: "bg-purple-600 hover:bg-purple-500",
    items: [
      "Sistema completo a medida",
      "Integración con tus sistemas",
      "Equipo dedicado",
      "Formación de tu equipo",
      "SLA garantizado",
      "Soporte 24/7",
    ],
    popular: false,
  },
];

const CASOS = [
  {
    empresa: "Clínica Dental",
    resultado: "40% menos llamadas, 25% más citas",
    servicio: "Chatbot IA",
    tiempo: "30 días",
    emoji: "🦷",
  },
  {
    empresa: "Tienda de Moda",
    resultado: "23% carritos recuperados, +15% ticket medio",
    servicio: "E-commerce + IA",
    tiempo: "45 días",
    emoji: "👗",
  },
  {
    empresa: "Despacho de Abogados",
    resultado: "70% menos tiempo en documentación",
    servicio: "App a medida",
    tiempo: "6 semanas",
    emoji: "⚖️",
  },
];

const FAQS = [
  {
    q: "¿Necesito saber de tecnología para trabajar con vosotros?",
    a: "Para nada. Nos encargamos de todo: diseño, desarrollo, implementación y formación. Tú recibes un sistema listo para usar.",
  },
  {
    q: "¿Cuánto tiempo tarda en estar listo un chatbot?",
    a: "Entre 5 y 10 días hábiles desde que nos das la información de tu negocio. Los sistemas más complejos pueden llevar 3-4 semanas.",
  },
  {
    q: "¿Puedo empezar con algo pequeño y escalar después?",
    a: "Sí, diseñamos todo pensando en el crecimiento. Muchos clientes empiezan con el pack Starter y van ampliando según resultados.",
  },
  {
    q: "¿Qué pasa si no estoy satisfecho?",
    a: "Ofrecemos 30 días de soporte post-entrega gratuito y garantía de satisfacción. Si algo no funciona como esperabas, lo arreglamos.",
  },
];

function ContactForm() {
  const [form, setForm] = useState({ nombre: "", email: "", empresa: "", mensaje: "" });
  const [estado, setEstado] = useState<"idle" | "enviando" | "ok" | "error">("idle");

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) =>
    setForm((p) => ({ ...p, [e.target.name]: e.target.value }));

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.nombre || !form.email || !form.mensaje) return;
    setEstado("enviando");
    try {
      const res = await fetch(`https://formsubmit.co/ajax/${EMAIL_DESTINO}`, {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify({
          _subject: `[NEXIA] Lead: ${form.empresa || form.nombre}`,
          nombre: form.nombre,
          email: form.email,
          empresa: form.empresa,
          mensaje: form.mensaje,
          _template: "table",
        }),
      });
      if (res.ok) {
        setEstado("ok");
        setForm({ nombre: "", email: "", empresa: "", mensaje: "" });
      } else {
        setEstado("error");
      }
    } catch {
      setEstado("error");
    }
  };

  if (estado === "ok") {
    return (
      <div className="text-center py-12">
        <div className="text-5xl mb-4">✅</div>
        <h3 className="text-2xl font-bold mb-2">¡Mensaje recibido!</h3>
        <p className="text-gray-400">Te respondemos en menos de 24 horas. Revisa tu bandeja de entrada.</p>
        <button onClick={() => setEstado("idle")}
          className="mt-6 text-blue-400 hover:text-blue-300 text-sm underline">
          Enviar otra consulta
        </button>
      </div>
    );
  }

  return (
    <form className="space-y-4 text-left" onSubmit={handleSubmit}>
      <div className="grid md:grid-cols-2 gap-4">
        <input name="nombre" value={form.nombre} onChange={handleChange}
          type="text" placeholder="Tu nombre" required
          className="bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white placeholder-gray-600 focus:border-blue-500 focus:outline-none w-full" />
        <input name="email" value={form.email} onChange={handleChange}
          type="email" placeholder="Tu email" required
          className="bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white placeholder-gray-600 focus:border-blue-500 focus:outline-none w-full" />
      </div>
      <input name="empresa" value={form.empresa} onChange={handleChange}
        type="text" placeholder="Nombre de tu empresa / negocio"
        className="bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white placeholder-gray-600 focus:border-blue-500 focus:outline-none w-full" />
      <textarea name="mensaje" value={form.mensaje} onChange={handleChange}
        placeholder="¿Qué quieres automatizar o mejorar con IA?" rows={4} required
        className="bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white placeholder-gray-600 focus:border-blue-500 focus:outline-none w-full resize-none" />
      {estado === "error" && (
        <p className="text-red-400 text-sm">Error al enviar. Escríbenos directamente a hola@nexia.io</p>
      )}
      <button type="submit" disabled={estado === "enviando"}
        className="w-full bg-blue-600 hover:bg-blue-500 disabled:opacity-60 text-white font-bold py-4 rounded-xl transition-all hover:scale-[1.02] text-lg">
        {estado === "enviando" ? "Enviando..." : "Solicitar consulta gratuita →"}
      </button>
    </form>
  );
}

export default function Home() {
  return (
    <main className="min-h-screen bg-[#08080c] text-white">

      {/* ── NAVBAR ── */}
      <nav className="fixed top-0 inset-x-0 z-50 border-b border-white/5 bg-[#08080c]/90 backdrop-blur-md">
        <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
          <span className="text-xl font-bold tracking-tight">
            NEX<span className="text-blue-400">IA</span>
          </span>
          <div className="hidden md:flex gap-8">
            {NAV_LINKS.map((l) => (
              <a key={l.href} href={l.href}
                className="text-sm text-gray-400 hover:text-white transition-colors">
                {l.label}
              </a>
            ))}
          </div>
          <a href="#contacto"
            className="bg-blue-600 hover:bg-blue-500 text-white text-sm font-semibold px-5 py-2 rounded-lg transition-colors">
            Consulta gratis →
          </a>
        </div>
      </nav>

      {/* ── HERO ── */}
      <section className="max-w-5xl mx-auto px-6 pt-40 pb-24 text-center">
        <div className="inline-flex items-center gap-2 bg-blue-500/10 text-blue-400 text-sm font-medium px-4 py-1.5 rounded-full mb-8 border border-blue-500/20">
          <span className="w-2 h-2 rounded-full bg-blue-400 animate-pulse" />
          Agencia de Inteligencia Artificial
        </div>
        <h1 className="text-5xl md:text-7xl font-extrabold mb-6 leading-tight tracking-tight">
          Tu negocio trabajando
          <br />
          <span className="text-blue-400">24/7 con IA</span>
        </h1>
        <p className="text-xl text-gray-400 mb-10 max-w-2xl mx-auto leading-relaxed">
          Chatbots que venden, apps que automatizan, redes que crecen solas.
          Sin contratar más personal. Sin tecnicismos.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <a href="#contacto"
            className="bg-blue-600 hover:bg-blue-500 text-white font-bold px-8 py-4 rounded-xl transition-all hover:scale-105 text-lg">
            Consulta gratuita de 30 min →
          </a>
          <a href="#casos"
            className="border border-gray-700 hover:border-gray-500 text-gray-300 font-semibold px-8 py-4 rounded-xl transition-colors text-lg">
            Ver resultados reales
          </a>
        </div>
        <p className="text-sm text-gray-600 mt-6">Sin compromiso · Sin tarjeta de crédito · Respuesta en 24h</p>
      </section>

      {/* ── LOGOS / TRUST ── */}
      <div className="border-y border-white/5 py-8">
        <div className="max-w-4xl mx-auto px-6 text-center">
          <p className="text-sm text-gray-600 mb-6 uppercase tracking-widest">Tecnologías que usamos</p>
          <div className="flex flex-wrap justify-center gap-8 text-gray-500 font-mono text-sm">
            {["OpenAI", "Claude AI", "Next.js", "Supabase", "n8n", "WhatsApp API", "Meta Ads", "Vercel"].map((t) => (
              <span key={t} className="hover:text-gray-300 transition-colors">{t}</span>
            ))}
          </div>
        </div>
      </div>

      {/* ── SERVICIOS ── */}
      <section id="servicios" className="max-w-6xl mx-auto px-6 py-24">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold mb-4">Nuestros servicios</h2>
          <p className="text-gray-400 text-lg">Todo lo que necesita tu negocio para crecer con IA</p>
        </div>
        <div className="grid md:grid-cols-3 gap-6">
          {SERVICIOS.map((s) => (
            <div key={s.titulo}
              className="bg-white/[0.03] border border-white/10 rounded-2xl p-6 hover:border-blue-500/40 hover:bg-white/[0.05] transition-all group">
              {s.tag && (
                <span className="inline-block bg-blue-500/10 text-blue-400 text-xs px-3 py-1 rounded-full mb-3 border border-blue-500/20">
                  {s.tag}
                </span>
              )}
              <div className="text-3xl mb-4">{s.icon}</div>
              <h3 className="text-lg font-bold mb-2 group-hover:text-blue-300 transition-colors">{s.titulo}</h3>
              <p className="text-gray-400 text-sm mb-4 leading-relaxed">{s.desc}</p>
              <div className="flex items-center justify-between pt-4 border-t border-white/5">
                <p className="text-blue-400 font-bold">{s.precio}</p>
                <p className="text-gray-600 text-xs">{s.detalle}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* ── CASOS ── */}
      <section id="casos" className="bg-white/[0.02] py-24 border-y border-white/5">
        <div className="max-w-5xl mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4">Resultados reales</h2>
            <p className="text-gray-400 text-lg">Clientes que ya trabajan con IA</p>
          </div>
          <div className="grid md:grid-cols-3 gap-6">
            {CASOS.map((c) => (
              <div key={c.empresa}
                className="bg-[#08080c] border border-white/10 rounded-2xl p-6">
                <p className="text-4xl mb-4">{c.emoji}</p>
                <p className="text-green-400 font-semibold text-sm mb-1">{c.servicio} · {c.tiempo}</p>
                <p className="text-gray-400 text-sm mb-3">{c.empresa}</p>
                <p className="text-xl font-bold text-white leading-tight">{c.resultado}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── PRECIOS ── */}
      <section id="precios" className="max-w-5xl mx-auto px-6 py-24">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold mb-4">Precio claro, sin sorpresas</h2>
          <p className="text-gray-400 text-lg">Elige el plan que se adapta a tu negocio</p>
        </div>
        <div className="grid md:grid-cols-3 gap-6">
          {PAQUETES.map((p) => (
            <div key={p.nombre}
              className={`relative bg-white/[0.03] border-2 ${p.color} rounded-2xl p-8 flex flex-col`}>
              {p.popular && (
                <div className="absolute -top-4 left-1/2 -translate-x-1/2">
                  <span className="bg-blue-600 text-white text-xs font-bold px-4 py-1.5 rounded-full">
                    MÁS POPULAR
                  </span>
                </div>
              )}
              <h3 className="text-xl font-bold mb-2">{p.nombre}</h3>
              <div className="mb-6">
                <span className="text-4xl font-extrabold">{p.precio}</span>
                <span className="text-gray-500 ml-2 text-sm">{p.periodo}</span>
              </div>
              <ul className="space-y-3 mb-8 flex-1">
                {p.items.map((item) => (
                  <li key={item} className="flex gap-3 text-sm text-gray-300">
                    <span className="text-green-400 flex-shrink-0">✓</span>
                    {item}
                  </li>
                ))}
              </ul>
              <a href="#contacto"
                className={`${p.btnColor} text-white text-sm font-bold text-center py-3 rounded-xl transition-colors`}>
                Empezar →
              </a>
            </div>
          ))}
        </div>
      </section>

      {/* ── FAQ ── */}
      <section className="max-w-3xl mx-auto px-6 py-20">
        <h2 className="text-4xl font-bold text-center mb-12">Preguntas frecuentes</h2>
        <div className="space-y-4">
          {FAQS.map((f) => (
            <div key={f.q} className="bg-white/[0.03] border border-white/10 rounded-xl p-6">
              <p className="font-semibold mb-2">{f.q}</p>
              <p className="text-gray-400 text-sm leading-relaxed">{f.a}</p>
            </div>
          ))}
        </div>
      </section>

      {/* ── CONTACTO ── */}
      <section id="contacto" className="max-w-2xl mx-auto px-6 py-24 text-center">
        <h2 className="text-4xl font-bold mb-4">Hablemos de tu proyecto</h2>
        <p className="text-gray-400 mb-10 text-lg">
          30 minutos. Sin compromiso. Te decimos exactamente qué haríamos y cuánto costaría.
        </p>
        <ContactForm />
        <p className="text-xs text-gray-700 mt-4">
          Respondemos en menos de 24 horas · hola@nexia.io
        </p>
      </section>

      {/* ── FOOTER ── */}
      <footer className="border-t border-white/5 py-12">
        <div className="max-w-6xl mx-auto px-6 flex flex-col md:flex-row items-center justify-between gap-4">
          <span className="text-xl font-bold">NEX<span className="text-blue-400">IA</span></span>
          <p className="text-gray-600 text-sm">Agencia de Inteligencia Artificial · 2026</p>
          <div className="flex gap-6 text-sm text-gray-600">
            <a href="#servicios" className="hover:text-gray-400 transition-colors">Servicios</a>
            <a href="#precios"   className="hover:text-gray-400 transition-colors">Precios</a>
            <a href="#contacto"  className="hover:text-gray-400 transition-colors">Contacto</a>
          </div>
        </div>
      </footer>

    </main>
  );
}
