"use client";
import { useState, useEffect, useRef } from "react";

// ── CONFIG ──────────────────────────────────────────────────
const EMAIL_DESTINO = "teamorionglobal@gmail.com";
const PLAZAS_FUNDADOR = 3;
// WhatsApp: pon tu número en formato internacional SIN "+" ni espacios (ej: "34600112233").
// Si lo dejas vacío, el botón flotante de WhatsApp simplemente no aparece.
const WHATSAPP = "5356659464";
const WHATSAPP_MSG = "Hola NEXIA, quiero mi diagnóstico web gratis.";
// Telegram: pon el @username de tu bot SIN la "@" (ej: "NexiaAsistenteBot").
// Abre un chat 1-a-1 directo con tu bot. Si lo dejas vacío, el botón no aparece.
const TELEGRAM_BOT = "Jarvistrading2026_bot";

// Qué recibe el cliente con el diagnóstico gratuito (concreta el gancho = más conversión)
const DIAGNOSTICO_INCLUYE = [
  { icon: "⚡", t: "Velocidad y rendimiento", d: "Cuánto tarda en cargar y qué te está costando en visitas perdidas." },
  { icon: "📱", t: "Experiencia en móvil", d: "Si tu web se ve y funciona bien donde está la mayoría de tus clientes." },
  { icon: "🔍", t: "Posicionamiento (SEO)", d: "Por qué Google no te muestra y los arreglos prioritarios." },
  { icon: "🔒", t: "Seguridad y confianza", d: "Certificado, avisos del navegador y señales que espantan clientes." },
  { icon: "💸", t: "Puntos de fuga de ventas", d: "Dónde pierdes contactos y cómo convertir más visitas en clientes." },
  { icon: "🗺️", t: "Plan de acción con precios", d: "Qué arreglar primero y cuánto cuesta. Tuyo aunque no contrates." },
];

// ── DATOS ───────────────────────────────────────────────────
const NAV_LINKS = [
  { label: "Servicios", href: "#servicios" },
  { label: "Cómo trabajamos", href: "#proceso" },
  { label: "Programa Fundador", href: "#fundador" },
  { label: "Contacto", href: "#contacto" },
];

const SERVICIOS = [
  {
    icon: "🌐",
    titulo: "Webs y Landing Pages",
    desc: "Webs rápidas, modernas y que convierten visitas en clientes. Optimizadas para móvil y para Google desde el primer día.",
    items: ["Landing page — desde 250€", "Web de 3 páginas — desde 600€", "Tienda online — desde 800€"],
  },
  {
    icon: "🤖",
    titulo: "Chatbots e IA",
    desc: "Atención 24/7 entrenada con los datos de tu negocio. Responde, vende y agenda citas sin empleados extra.",
    items: ["Chatbot con IA — desde 400€", "Asistente IA a medida — desde 900€", "WhatsApp Business — desde 150€"],
  },
  {
    icon: "⚡",
    titulo: "Automatización",
    desc: "Eliminamos tareas repetitivas: emails, reservas, informes, sincronización de datos. Tu negocio funciona solo.",
    items: ["Automatización de procesos — desde 200€", "Email marketing — desde 150€", "Integraciones / APIs — desde 200€"],
  },
  {
    icon: "📈",
    titulo: "Marketing y SEO",
    desc: "Que te encuentren en Google y en redes. Posicionamiento, contenido y campañas medibles.",
    items: ["Auditoría SEO — desde 150€", "Gestión de redes — desde 200€/mes", "Google / Meta Ads — desde 200€"],
  },
];

const PROCESO = [
  { num: "01", titulo: "Diagnóstico gratis", desc: "Analizamos tu web (o tu falta de ella) y te decimos en 24h exactamente qué falla y qué mejorar. Sin compromiso." },
  { num: "02", titulo: "Propuesta clara", desc: "Te damos un plan con precio fijo y plazos. Sin sorpresas, sin letra pequeña. Tú decides." },
  { num: "03", titulo: "Lo construimos", desc: "Manos a la obra. Entregas rápidas por fases para que veas avances reales cada semana." },
  { num: "04", titulo: "Soporte incluido", desc: "30 días de soporte tras la entrega y opción de mantenimiento mensual. No te dejamos solo." },
];

const FAQ = [
  { q: "¿Cuánto tardáis en entregar?", a: "Una landing simple en 3-5 días. Una web completa en 2-3 semanas. Un chatbot en 1-2 semanas. Te damos un plazo cerrado en la propuesta." },
  { q: "¿De verdad el diagnóstico es gratis?", a: "Sí, totalmente. Analizamos tu web (velocidad, SEO, móvil, seguridad, conversión) y te enviamos un informe con los problemas reales y cómo solucionarlos. Sin compromiso de contratar nada." },
  { q: "Sois nuevos, ¿por qué confiar en vosotros?", a: "Por eso existe el Programa Fundador: trabajamos a mitad de precio con los primeros clientes precisamente para construir nuestro historial. Tú ganas un precio que no se repetirá y nosotros un caso de éxito real." },
  { q: "¿Qué pasa si no me gusta el resultado?", a: "Trabajamos por fases con tu visto bueno en cada paso, así nunca hay sorpresas al final. El primer pago es del 50%; el resto solo cuando apruebas la entrega." },
  { q: "¿Trabajáis con negocios fuera de España?", a: "Sí. Trabajamos en remoto con pymes y autónomos de España y LATAM. Toda la comunicación es online." },
];

// ── MOCKUPS (SVG, sin imágenes externas) ─────────────────────
function MockupDashboard() {
  return (
    <svg viewBox="0 0 520 360" className="w-full h-auto drop-shadow-2xl" role="img" aria-label="Panel de control NEXIA">
      <defs>
        <linearGradient id="md-acc" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0" stopColor="#60a5fa" /><stop offset="1" stopColor="#3b82f6" />
        </linearGradient>
      </defs>
      <rect x="2" y="2" width="516" height="356" rx="16" fill="#0d1426" stroke="#1e3a8a" strokeWidth="1.5" />
      <rect x="2" y="2" width="516" height="44" rx="16" fill="#111a33" />
      <circle cx="28" cy="24" r="6" fill="#ef4444" /><circle cx="48" cy="24" r="6" fill="#f59e0b" /><circle cx="68" cy="24" r="6" fill="#22c55e" />
      <rect x="120" y="17" width="280" height="14" rx="7" fill="#1e293b" />
      {/* sidebar */}
      <rect x="16" y="60" width="120" height="284" rx="10" fill="#0a1120" />
      <rect x="32" y="80" width="88" height="10" rx="5" fill="url(#md-acc)" />
      <rect x="32" y="104" width="70" height="8" rx="4" fill="#334155" />
      <rect x="32" y="124" width="80" height="8" rx="4" fill="#334155" />
      <rect x="32" y="144" width="62" height="8" rx="4" fill="#334155" />
      {/* cards */}
      <rect x="152" y="60" width="166" height="72" rx="10" fill="#111a33" />
      <text x="168" y="92" fontFamily="Inter,sans-serif" fontSize="13" fill="#94a3b8">Leads esta semana</text>
      <text x="168" y="118" fontFamily="Inter,sans-serif" fontSize="24" fontWeight="800" fill="#fff">128</text>
      <rect x="334" y="60" width="168" height="72" rx="10" fill="#111a33" />
      <text x="350" y="92" fontFamily="Inter,sans-serif" fontSize="13" fill="#94a3b8">Conversión</text>
      <text x="350" y="118" fontFamily="Inter,sans-serif" fontSize="24" fontWeight="800" fill="#34d399">24%</text>
      {/* chart */}
      <rect x="152" y="148" width="350" height="196" rx="10" fill="#0a1120" />
      <polyline className="draw-line" points="172,300 220,270 268,285 316,230 364,250 412,190 470,210" fill="none" stroke="url(#md-acc)" strokeWidth="3" />
      {[172,220,268,316,364,412,470].map((x,i)=>(<circle key={i} cx={x} cy={[300,270,285,230,250,190,210][i]} r="4" fill="#60a5fa" />))}
      <rect x="172" y="316" width="300" height="6" rx="3" fill="#1e293b" />
    </svg>
  );
}

function MockupChatbot() {
  return (
    <svg viewBox="0 0 240 420" className="w-full h-auto drop-shadow-2xl" role="img" aria-label="Chatbot de NEXIA en el móvil">
      <rect x="6" y="6" width="228" height="408" rx="34" fill="#0d1426" stroke="#1e3a8a" strokeWidth="2" />
      <rect x="18" y="18" width="204" height="384" rx="24" fill="#070b16" />
      <rect x="86" y="26" width="68" height="8" rx="4" fill="#1e293b" />
      {/* header */}
      <circle cx="44" cy="66" r="14" fill="#3b82f6" />
      <text x="44" y="71" fontFamily="Inter,sans-serif" fontSize="13" fontWeight="700" fill="#fff" textAnchor="middle">N</text>
      <text x="66" y="62" fontFamily="Inter,sans-serif" fontSize="12" fontWeight="700" fill="#fff">Asistente NEXIA</text>
      <text x="66" y="77" fontFamily="Inter,sans-serif" fontSize="9" fill="#34d399"><tspan className="anim-blink">●</tspan> En línea</text>
      {/* bubbles */}
      <rect x="30" y="100" width="150" height="44" rx="12" fill="#16213f" />
      <text x="42" y="120" fontFamily="Inter,sans-serif" fontSize="9.5" fill="#cbd5e1">Hola 👋 ¿En qué puedo</text>
      <text x="42" y="134" fontFamily="Inter,sans-serif" fontSize="9.5" fill="#cbd5e1">ayudarte hoy?</text>
      <rect x="84" y="156" width="126" height="30" rx="12" fill="#2563eb" />
      <text x="98" y="175" fontFamily="Inter,sans-serif" fontSize="9.5" fill="#fff">Quiero reservar mesa</text>
      <rect x="30" y="198" width="160" height="58" rx="12" fill="#16213f" />
      <text x="42" y="218" fontFamily="Inter,sans-serif" fontSize="9.5" fill="#cbd5e1">¡Perfecto! ¿Para cuántas</text>
      <text x="42" y="232" fontFamily="Inter,sans-serif" fontSize="9.5" fill="#cbd5e1">personas y a qué hora?</text>
      <text x="42" y="246" fontFamily="Inter,sans-serif" fontSize="9.5" fill="#60a5fa">Tengo hueco hoy 21:00 ✓</text>
      {/* input */}
      <rect x="24" y="368" width="150" height="26" rx="13" fill="#16213f" />
      <text x="38" y="385" fontFamily="Inter,sans-serif" fontSize="9.5" fill="#64748b">Escribe un mensaje…</text>
      <circle cx="196" cy="381" r="14" fill="#3b82f6" />
      <path d="M190 381l12-5-5 12-2-5z" fill="#fff" />
    </svg>
  );
}

// ── COMPONENTES ─────────────────────────────────────────────
function FAQItem({ q, a }: { q: string; a: string }) {
  const [open, setOpen] = useState(false);
  return (
    <div className="border border-white/10 rounded-xl overflow-hidden bg-white/[0.02]">
      <button onClick={() => setOpen(!open)} className="w-full flex items-center justify-between px-6 py-5 text-left">
        <span className="font-semibold text-white">{q}</span>
        <span className={`text-blue-400 text-xl transition-transform ${open ? "rotate-45" : ""}`}>+</span>
      </button>
      {open && <div className="px-6 pb-5 text-gray-400 text-sm leading-relaxed border-t border-white/5 pt-4">{a}</div>}
    </div>
  );
}

function ContactForm() {
  const [form, setForm] = useState({ nombre: "", email: "", empresa: "", web: "", mensaje: "" });
  const [estado, setEstado] = useState<"idle" | "enviando" | "ok" | "error">("idle");
  const onChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) =>
    setForm((p) => ({ ...p, [e.target.name]: e.target.value }));

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.nombre || !form.email) return;
    setEstado("enviando");
    try {
      const res = await fetch(`https://formsubmit.co/ajax/${EMAIL_DESTINO}`, {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify({
          _subject: `[NEXIA] Solicitud Programa Fundador: ${form.empresa || form.nombre}`,
          Nombre: form.nombre, Email: form.email, Empresa: form.empresa,
          Web: form.web || "—", Mensaje: form.mensaje || "—", _template: "table",
        }),
      });
      if (res.ok) { setEstado("ok"); setForm({ nombre: "", email: "", empresa: "", web: "", mensaje: "" }); }
      else setEstado("error");
    } catch { setEstado("error"); }
  };

  if (estado === "ok") {
    return (
      <div className="text-center py-16">
        <div className="text-6xl mb-6">✅</div>
        <h3 className="text-2xl font-bold mb-3">¡Solicitud recibida!</h3>
        <p className="text-gray-400">Te enviamos tu diagnóstico web gratuito en menos de 24h laborables.</p>
        <p className="text-gray-500 text-sm mt-2">Revisa también tu carpeta de spam.</p>
      </div>
    );
  }

  return (
    <form onSubmit={onSubmit} className="space-y-4">
      <div className="grid sm:grid-cols-2 gap-4">
        <input name="nombre" value={form.nombre} onChange={onChange} required placeholder="Tu nombre *"
          className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:border-blue-500 focus:outline-none" />
        <input name="email" type="email" value={form.email} onChange={onChange} required placeholder="Tu email *"
          className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:border-blue-500 focus:outline-none" />
      </div>
      <div className="grid sm:grid-cols-2 gap-4">
        <input name="empresa" value={form.empresa} onChange={onChange} placeholder="Nombre de tu negocio"
          className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:border-blue-500 focus:outline-none" />
        <input name="web" value={form.web} onChange={onChange} placeholder="Tu web actual (si tienes)"
          className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:border-blue-500 focus:outline-none" />
      </div>
      <textarea name="mensaje" value={form.mensaje} onChange={onChange} rows={4} placeholder="¿Qué necesitas? (opcional)"
        className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:border-blue-500 focus:outline-none resize-none" />
      <button type="submit" disabled={estado === "enviando"}
        className="btn-shine w-full bg-blue-600 hover:bg-blue-500 disabled:opacity-60 text-white font-semibold py-4 rounded-lg transition-colors">
        {estado === "enviando" ? "Enviando…" : "Quiero mi diagnóstico gratis →"}
      </button>
      {estado === "error" && <p className="text-red-400 text-sm text-center">Algo falló. Escríbenos directo a {EMAIL_DESTINO}</p>}
      <p className="text-xs text-gray-600 text-center">Sin compromiso · Respuesta en 24h · 100% gratuito</p>
    </form>
  );
}

// ── REVEAL al hacer scroll ──────────────────────────────────
function Reveal({ children, delay = 0, className = "" }: { children: React.ReactNode; delay?: number; className?: string }) {
  const ref = useRef<HTMLDivElement>(null);
  const [visible, setVisible] = useState(false);
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const obs = new IntersectionObserver(
      ([entry]) => { if (entry.isIntersecting) { setVisible(true); obs.disconnect(); } },
      { threshold: 0.15 }
    );
    obs.observe(el);
    return () => obs.disconnect();
  }, []);
  return (
    <div ref={ref} className={`reveal ${visible ? "is-visible" : ""} ${className}`} style={{ transitionDelay: `${delay}ms` }}>
      {children}
    </div>
  );
}

// ── PÁGINA ──────────────────────────────────────────────────
export default function Home() {
  const [menuOpen, setMenuOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener("scroll", onScroll);
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <main className="min-h-screen bg-[#08080c] text-white overflow-x-hidden">
      {/* NAVBAR */}
      <nav className={`fixed top-0 inset-x-0 z-50 transition-all duration-300 ${scrolled ? "border-b border-white/10 bg-[#08080c]/95 backdrop-blur-md" : "bg-transparent"}`}>
        <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
          <a href="#" className="text-xl font-bold tracking-tight">NEX<span className="text-blue-400">IA</span></a>
          <div className="hidden md:flex gap-8">
            {NAV_LINKS.map((l) => (
              <a key={l.href} href={l.href} className="text-sm text-gray-400 hover:text-white transition-colors">{l.label}</a>
            ))}
          </div>
          <a href="#contacto" className="hidden md:block bg-blue-600 hover:bg-blue-500 text-white text-sm font-semibold px-5 py-2 rounded-lg transition-colors">Diagnóstico gratis →</a>
          <button onClick={() => setMenuOpen(!menuOpen)} className="md:hidden text-gray-400" aria-label="Menú">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              {menuOpen ? <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" /> : <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />}
            </svg>
          </button>
        </div>
        {menuOpen && (
          <div className="md:hidden border-t border-white/10 bg-[#08080c] px-6 py-4 space-y-3">
            {NAV_LINKS.map((l) => (<a key={l.href} href={l.href} onClick={() => setMenuOpen(false)} className="block text-gray-300 py-1">{l.label}</a>))}
            <a href="#contacto" onClick={() => setMenuOpen(false)} className="block bg-blue-600 text-center text-white font-semibold py-2 rounded-lg">Diagnóstico gratis →</a>
          </div>
        )}
      </nav>

      {/* HERO */}
      <section className="relative pt-32 pb-20 px-6">
        <div className="absolute top-0 right-0 w-[600px] h-[600px] bg-blue-600/10 rounded-full blur-3xl -z-0 anim-pulseGlow" />
        <div className="absolute top-40 -left-20 w-[400px] h-[400px] bg-indigo-600/10 rounded-full blur-3xl -z-0 anim-pulseGlow" style={{ animationDelay: "2s" }} />
        <div className="max-w-6xl mx-auto grid lg:grid-cols-2 gap-12 items-center relative z-10">
          <div>
            <span className="anim-fadeUp inline-flex items-center gap-2 bg-blue-500/10 border border-blue-500/20 text-blue-300 text-xs font-medium px-3 py-1.5 rounded-full mb-6">
              <span className="anim-blink">🚀</span> Programa Fundador abierto · {PLAZAS_FUNDADOR} plazas
            </span>
            <h1 className="anim-fadeUp d-1 text-4xl sm:text-5xl lg:text-6xl font-extrabold leading-tight mb-6">
              Tu negocio,<br /><span className="text-gradient-anim">trabajando 24/7 con IA</span>
            </h1>
            <p className="anim-fadeUp d-2 text-lg text-gray-400 mb-8 max-w-lg">
              Webs profesionales, chatbots inteligentes y automatización para pymes. Empezamos con un <strong className="text-white">diagnóstico gratuito</strong> de tu web: te decimos exactamente qué falla y cuánto cuesta arreglarlo.
            </p>
            <div className="anim-fadeUp d-3 flex flex-col sm:flex-row gap-4">
              <a href="#contacto" className="btn-shine bg-blue-600 hover:bg-blue-500 text-white font-semibold px-7 py-4 rounded-lg text-center transition-colors">Quiero mi diagnóstico gratis</a>
              <a href="#servicios" className="border border-white/15 hover:bg-white/5 text-white font-semibold px-7 py-4 rounded-lg text-center transition-colors">Ver servicios</a>
            </div>
            <div className="anim-fadeUp d-3 flex flex-wrap items-center gap-x-5 gap-y-2 mt-6 text-sm text-gray-500">
              <span className="flex items-center gap-1.5"><span className="text-green-400">✓</span> Sin tarjeta</span>
              <span className="flex items-center gap-1.5"><span className="text-green-400">✓</span> Respuesta en 24h</span>
              <span className="flex items-center gap-1.5"><span className="text-green-400">✓</span> Sin permanencia</span>
            </div>
          </div>
          <div className="anim-fadeIn d-2 relative">
            <div className="anim-float"><MockupDashboard /></div>
            <div className="absolute -bottom-8 -left-4 w-28 sm:w-36 anim-floatSlow"><MockupChatbot /></div>
          </div>
        </div>
      </section>

      {/* TECH / HONESTIDAD */}
      <section className="py-12 px-6 border-y border-white/5">
        <div className="max-w-5xl mx-auto text-center">
          <p className="text-xs uppercase tracking-widest text-gray-500 mb-6">Construido con tecnología profesional</p>
          <div className="flex flex-wrap justify-center gap-x-10 gap-y-4 text-gray-400 font-semibold">
            <span>Next.js</span><span>React</span><span>Inteligencia Artificial</span><span>n8n</span><span>WhatsApp Business</span><span>SEO</span>
          </div>
        </div>
      </section>

      {/* SERVICIOS */}
      <section id="servicios" className="py-24 px-6">
        <div className="max-w-6xl mx-auto">
          <Reveal className="text-center mb-14">
            <h2 className="text-3xl sm:text-4xl font-bold mb-4">Lo que hacemos por tu negocio</h2>
            <p className="text-gray-400 max-w-2xl mx-auto">Soluciones concretas con precio cerrado. Sin paquetes inflados: pagas por lo que necesitas.</p>
          </Reveal>
          <div className="grid md:grid-cols-2 gap-6">
            {SERVICIOS.map((s, i) => (
              <Reveal key={s.titulo} delay={i * 100}>
                <div className="card-lift h-full bg-white/[0.02] border border-white/10 rounded-2xl p-8 hover:border-blue-500/40">
                  <div className="text-4xl mb-4">{s.icon}</div>
                  <h3 className="text-xl font-bold mb-2">{s.titulo}</h3>
                  <p className="text-gray-400 text-sm mb-5 leading-relaxed">{s.desc}</p>
                  <ul className="space-y-2">
                    {s.items.map((it) => (
                      <li key={it} className="flex items-center gap-2 text-sm text-gray-300">
                        <span className="text-blue-400">✓</span>{it}
                      </li>
                    ))}
                  </ul>
                </div>
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      {/* PROCESO */}
      <section id="proceso" className="py-24 px-6 bg-white/[0.015] border-y border-white/5">
        <div className="max-w-6xl mx-auto">
          <Reveal className="text-center mb-14">
            <h2 className="text-3xl sm:text-4xl font-bold mb-4">Cómo trabajamos</h2>
            <p className="text-gray-400 max-w-2xl mx-auto">Empezamos siempre por un diagnóstico real y gratuito. Tú decides con datos, no con promesas.</p>
          </Reveal>
          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {PROCESO.map((p, i) => (
              <Reveal key={p.num} delay={i * 100}>
                <div className="card-lift relative bg-[#0d1426] border border-white/10 rounded-2xl p-7 h-full hover:border-blue-500/40">
                  <span className="text-5xl font-extrabold text-blue-500/20 absolute top-4 right-5">{p.num}</span>
                  <h3 className="text-lg font-bold mb-2 relative z-10">{p.titulo}</h3>
                  <p className="text-gray-400 text-sm leading-relaxed relative z-10">{p.desc}</p>
                </div>
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      {/* PROGRAMA FUNDADOR */}
      <section id="fundador" className="py-24 px-6">
        <Reveal className="max-w-4xl mx-auto bg-gradient-to-br from-blue-600/15 to-blue-900/10 border border-blue-500/25 rounded-3xl p-10 sm:p-14 text-center">
          <span className="inline-block bg-blue-500/20 text-blue-300 text-xs font-semibold px-3 py-1.5 rounded-full mb-6">⭐ Solo {PLAZAS_FUNDADOR} plazas</span>
          <h2 className="text-3xl sm:text-4xl font-bold mb-5">Programa Fundador</h2>
          <p className="text-gray-300 max-w-2xl mx-auto mb-8 leading-relaxed">
            Somos nuevos y lo decimos claro. Buscamos <strong className="text-white">3 negocios fundadores</strong> dispuestos a ser nuestros primeros casos de éxito. A cambio:
          </p>
          <div className="grid sm:grid-cols-3 gap-5 mb-10 text-left">
            {[
              { t: "50% de descuento", d: "En tu primer proyecto. Un precio que no se repetirá." },
              { t: "Soporte prioritario", d: "Acceso directo y atención preferente durante el proyecto." },
              { t: "Diagnóstico completo", d: "Auditoría web profesional gratuita, tuya aunque no contrates." },
            ].map((b) => (
              <div key={b.t} className="bg-white/5 border border-white/10 rounded-xl p-5">
                <h3 className="font-bold text-blue-300 mb-1">{b.t}</h3>
                <p className="text-gray-400 text-sm">{b.d}</p>
              </div>
            ))}
          </div>
          <a href="#contacto" className="btn-shine inline-block bg-blue-600 hover:bg-blue-500 text-white font-semibold px-8 py-4 rounded-lg transition-colors">Solicitar plaza fundador →</a>
        </Reveal>
      </section>

      {/* FAQ */}
      <section className="py-24 px-6 bg-white/[0.015] border-y border-white/5">
        <div className="max-w-3xl mx-auto">
          <Reveal><h2 className="text-3xl sm:text-4xl font-bold text-center mb-12">Preguntas frecuentes</h2></Reveal>
          <Reveal className="space-y-3">{FAQ.map((f) => <FAQItem key={f.q} {...f} />)}</Reveal>
        </div>
      </section>

      {/* CONTACTO */}
      <section id="contacto" className="py-24 px-6">
        <div className="max-w-2xl mx-auto">
          <Reveal className="text-center mb-10">
            <h2 className="text-3xl sm:text-4xl font-bold mb-4">Tu diagnóstico web gratis</h2>
            <p className="text-gray-400">Déjanos tus datos y en 24h te enviamos un informe real de tu web con qué mejorar y cuánto cuesta. Sin compromiso.</p>
          </Reveal>
          <Reveal delay={50} className="mb-10">
            <p className="text-center text-xs uppercase tracking-widest text-gray-500 mb-5">Qué analizamos por ti</p>
            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {DIAGNOSTICO_INCLUYE.map((d) => (
                <div key={d.t} className="flex gap-3 bg-white/[0.02] border border-white/10 rounded-xl p-4">
                  <span className="text-xl shrink-0">{d.icon}</span>
                  <div>
                    <h3 className="font-semibold text-sm text-white">{d.t}</h3>
                    <p className="text-gray-400 text-xs leading-relaxed mt-0.5">{d.d}</p>
                  </div>
                </div>
              ))}
            </div>
          </Reveal>
          <Reveal delay={100} className="bg-white/[0.02] border border-white/10 rounded-2xl p-8"><ContactForm /></Reveal>
          {TELEGRAM_BOT && (
            <Reveal delay={150} className="mt-6 text-center">
              <p className="text-gray-500 text-sm mb-3">¿Prefieres chatear ahora mismo?</p>
              <a href={`https://t.me/${TELEGRAM_BOT}`} target="_blank" rel="noopener noreferrer"
                className="inline-flex items-center gap-2 bg-[#229ED9] hover:bg-[#1b8ec2] text-white font-semibold px-6 py-3 rounded-lg transition-colors">
                <svg className="w-5 h-5" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                  <path d="M21.94 4.5L18.6 20.2c-.25 1.1-.9 1.38-1.83.86l-5.05-3.72-2.44 2.35c-.27.27-.5.5-1 .5l.36-5.13L18.05 6.5c.4-.36-.09-.56-.62-.2L6.5 13.2l-4.96-1.55c-1.08-.34-1.1-1.08.23-1.6l19.4-7.48c.9-.34 1.68.2 1.39 1.43z"/>
                </svg>
                Habla con nuestro asistente en Telegram
              </a>
            </Reveal>
          )}
        </div>
      </section>

      {/* FOOTER */}
      <footer className="border-t border-white/10 py-12 px-6">
        <div className="max-w-6xl mx-auto flex flex-col sm:flex-row items-start justify-between gap-6">
          <div>
            <p className="text-lg font-bold">NEX<span className="text-blue-400">IA</span></p>
            <p className="text-gray-500 text-sm max-w-xs">Agencia de IA, webs y automatización para pymes. Algunos servicios usan inteligencia artificial; los resultados pueden contener errores y no sustituyen asesoramiento profesional.</p>
          </div>
          <div className="text-gray-500 text-sm sm:text-right">
            <div className="flex flex-wrap gap-x-5 gap-y-2 sm:justify-end mb-3">
              <a href="/terminos/" className="hover:text-white transition-colors">Términos</a>
              <a href="/privacidad/" className="hover:text-white transition-colors">Privacidad</a>
              <a href="/cookies/" className="hover:text-white transition-colors">Cookies</a>
            </div>
            <a href={`mailto:${EMAIL_DESTINO}`} className="hover:text-white transition-colors">{EMAIL_DESTINO}</a>
            <p className="mt-1">© {new Date().getFullYear()} NEXIA · Hecho con IA</p>
          </div>
        </div>
      </footer>

      <FloatingActions />
      <CookieBanner />
    </main>
  );
}

// ── ACCIONES FLOTANTES (WhatsApp + CTA fija en móvil) ────────
function FloatingActions() {
  const [show, setShow] = useState(false);
  useEffect(() => {
    const onScroll = () => setShow(window.scrollY > 500);
    window.addEventListener("scroll", onScroll);
    return () => window.removeEventListener("scroll", onScroll);
  }, []);
  const waHref = WHATSAPP ? `https://wa.me/${WHATSAPP}?text=${encodeURIComponent(WHATSAPP_MSG)}` : null;
  const tgHref = TELEGRAM_BOT ? `https://t.me/${TELEGRAM_BOT}` : null;
  return (
    <>
      {tgHref && (
        <a href={tgHref} target="_blank" rel="noopener noreferrer" aria-label="Habla con nuestro asistente en Telegram"
          className="fixed bottom-36 right-5 z-40 w-14 h-14 rounded-full bg-[#229ED9] shadow-lg flex items-center justify-center hover:scale-105 transition-transform">
          <svg className="w-7 h-7" viewBox="0 0 24 24" fill="#fff" aria-hidden="true">
            <path d="M21.94 4.5L18.6 20.2c-.25 1.1-.9 1.38-1.83.86l-5.05-3.72-2.44 2.35c-.27.27-.5.5-1 .5l.36-5.13L18.05 6.5c.4-.36-.09-.56-.62-.2L6.5 13.2l-4.96-1.55c-1.08-.34-1.1-1.08.23-1.6l19.4-7.48c.9-.34 1.68.2 1.39 1.43z"/>
          </svg>
        </a>
      )}
      {waHref && (
        <a href={waHref} target="_blank" rel="noopener noreferrer" aria-label="Escríbenos por WhatsApp"
          className="fixed bottom-20 right-5 z-40 w-14 h-14 rounded-full bg-[#25D366] shadow-lg flex items-center justify-center hover:scale-105 transition-transform">
          <svg className="w-7 h-7" viewBox="0 0 24 24" fill="#fff" aria-hidden="true">
            <path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2 22l5.25-1.38a9.9 9.9 0 0 0 4.79 1.22h.01c5.46 0 9.91-4.45 9.91-9.91C21.96 6.45 17.5 2 12.04 2zm5.8 14.06c-.24.68-1.4 1.3-1.93 1.38-.49.07-1.12.1-1.8-.11-.42-.13-.95-.31-1.64-.6-2.88-1.24-4.76-4.14-4.9-4.33-.14-.19-1.17-1.56-1.17-2.97 0-1.42.74-2.11 1-2.4.26-.29.57-.36.76-.36h.55c.18 0 .42-.07.65.5.24.58.82 2 .89 2.14.07.14.12.31.02.5-.1.19-.14.31-.29.48-.14.17-.3.38-.43.51-.14.14-.29.29-.12.58.17.29.74 1.22 1.59 1.98 1.1.98 2.02 1.28 2.31 1.43.29.14.46.12.63-.07.17-.19.72-.84.91-1.13.19-.29.39-.24.65-.14.26.1 1.67.79 1.96.93.29.14.48.22.55.34.07.12.07.7-.17 1.38z"/>
          </svg>
        </a>
      )}
      {/* Barra CTA fija solo en móvil, aparece tras hacer scroll */}
      <div className={`md:hidden fixed bottom-0 inset-x-0 z-30 p-3 bg-[#08080c]/95 backdrop-blur-md border-t border-white/10 transition-transform duration-300 ${show ? "translate-y-0" : "translate-y-full"}`}>
        <a href="#contacto" className="block bg-blue-600 hover:bg-blue-500 text-white text-center font-semibold py-3 rounded-lg">
          Quiero mi diagnóstico gratis →
        </a>
      </div>
    </>
  );
}

// ── BANNER DE COOKIES ───────────────────────────────────────
function CookieBanner() {
  const [visible, setVisible] = useState(false);
  useEffect(() => {
    try { if (!localStorage.getItem("nexia-cookies-ok")) setVisible(true); } catch {}
  }, []);
  if (!visible) return null;
  const aceptar = () => { try { localStorage.setItem("nexia-cookies-ok", "1"); } catch {} setVisible(false); };
  return (
    <div className="fixed bottom-0 inset-x-0 z-50 bg-[#0d1426] border-t border-white/10 px-6 py-4">
      <div className="max-w-5xl mx-auto flex flex-col sm:flex-row items-center gap-4 justify-between">
        <p className="text-gray-400 text-sm">
          Usamos solo cookies esenciales para que la web funcione. Más info en nuestra{" "}
          <a href="/cookies/" className="text-blue-400 underline">Política de Cookies</a>.
        </p>
        <button onClick={aceptar} className="bg-blue-600 hover:bg-blue-500 text-white text-sm font-semibold px-6 py-2 rounded-lg whitespace-nowrap transition-colors">Entendido</button>
      </div>
    </div>
  );
}
