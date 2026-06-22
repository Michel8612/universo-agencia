// Web principal de la agencia — Landing page que convierte
import Link from "next/link";

const SERVICIOS = [
  {
    icon: "🤖",
    titulo: "Chatbots con IA",
    desc: "Atención al cliente 24/7 entrenada con los datos de tu negocio. Sin contratar más personal.",
    precio: "desde 497€",
    tag: "Más vendido",
  },
  {
    icon: "💻",
    titulo: "Desarrollo de Apps",
    desc: "Tu idea convertida en producto real. Frontend, backend, base de datos y deploy incluido.",
    precio: "desde 1.497€",
    tag: null,
  },
  {
    icon: "📱",
    titulo: "Gestión de Redes",
    desc: "Publicamos contenido de calidad cada día en todas tus redes. Tú solo apruebas.",
    precio: "desde 497€/mes",
    tag: "Recurrente",
  },
  {
    icon: "🔒",
    titulo: "Ciberseguridad",
    desc: "Auditorías LOPD/GDPR y test de vulnerabilidades. Cumple la ley y protege tu negocio.",
    precio: "desde 797€",
    tag: null,
  },
  {
    icon: "🛒",
    titulo: "Tiendas Online",
    desc: "E-commerce completo con IA integrada: recomendaciones, chatbot y recuperación de carritos.",
    precio: "desde 1.497€",
    tag: null,
  },
  {
    icon: "📈",
    titulo: "SEO + Ads",
    desc: "Tráfico orgánico a largo plazo y campañas de pago que generan ROI medible desde el día 1.",
    precio: "desde 297€/mes",
    tag: null,
  },
];

const CASOS = [
  {
    empresa: "Clínica Dental",
    resultado: "40% menos llamadas, 25% más citas completadas",
    servicio: "Chatbot IA",
    tiempo: "30 días",
  },
  {
    empresa: "Tienda de moda online",
    resultado: "23% carritos abandonados recuperados, +15% ticket medio",
    servicio: "E-commerce + IA",
    tiempo: "45 días",
  },
  {
    empresa: "Despacho de abogados",
    resultado: "70% menos tiempo en preparación de documentos",
    servicio: "App a medida",
    tiempo: "6 semanas",
  },
];

export default function Home() {
  return (
    <main className="min-h-screen bg-gray-950 text-white">
      {/* Hero */}
      <section className="max-w-5xl mx-auto px-6 pt-24 pb-20 text-center">
        <span className="inline-block bg-indigo-500/10 text-indigo-400 text-sm font-medium px-4 py-1.5 rounded-full mb-6 border border-indigo-500/20">
          Agencia de Inteligencia Artificial
        </span>
        <h1 className="text-5xl md:text-6xl font-bold mb-6 leading-tight">
          Tu negocio trabajando
          <span className="text-indigo-400"> 24/7 con IA</span>
        </h1>
        <p className="text-xl text-gray-400 mb-10 max-w-2xl mx-auto">
          Automatizamos, construimos y escalamos. Chatbots, apps, redes sociales y ciberseguridad — todo con inteligencia artificial.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link href="/contacto"
            className="bg-indigo-600 hover:bg-indigo-500 text-white font-semibold px-8 py-4 rounded-xl transition-colors">
            Quiero una consulta gratis →
          </Link>
          <Link href="#casos"
            className="border border-gray-700 hover:border-gray-500 text-gray-300 font-semibold px-8 py-4 rounded-xl transition-colors">
            Ver casos de éxito
          </Link>
        </div>
      </section>

      {/* Servicios */}
      <section className="max-w-6xl mx-auto px-6 py-20">
        <h2 className="text-3xl font-bold text-center mb-4">Nuestros servicios</h2>
        <p className="text-gray-400 text-center mb-12">Soluciones con IA para cada necesidad de tu negocio</p>
        <div className="grid md:grid-cols-3 gap-6">
          {SERVICIOS.map((s) => (
            <div key={s.titulo} className="bg-gray-900 border border-gray-800 rounded-2xl p-6 hover:border-indigo-500/50 transition-colors">
              {s.tag && (
                <span className="inline-block bg-indigo-500/10 text-indigo-400 text-xs px-3 py-1 rounded-full mb-3">
                  {s.tag}
                </span>
              )}
              <div className="text-3xl mb-3">{s.icon}</div>
              <h3 className="text-lg font-semibold mb-2">{s.titulo}</h3>
              <p className="text-gray-400 text-sm mb-4">{s.desc}</p>
              <p className="text-indigo-400 font-semibold">{s.precio}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Casos de éxito */}
      <section id="casos" className="bg-gray-900/50 py-20">
        <div className="max-w-5xl mx-auto px-6">
          <h2 className="text-3xl font-bold text-center mb-12">Resultados reales</h2>
          <div className="grid md:grid-cols-3 gap-6">
            {CASOS.map((c) => (
              <div key={c.empresa} className="bg-gray-900 border border-gray-800 rounded-2xl p-6">
                <p className="text-green-400 font-semibold text-sm mb-2">✓ {c.servicio} · {c.tiempo}</p>
                <p className="text-gray-300 font-medium mb-3">{c.empresa}</p>
                <p className="text-2xl font-bold text-white">{c.resultado}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Final */}
      <section className="max-w-3xl mx-auto px-6 py-24 text-center">
        <h2 className="text-4xl font-bold mb-6">¿Listo para automatizar tu negocio?</h2>
        <p className="text-gray-400 mb-8 text-lg">Consulta gratuita de 30 minutos. Sin compromiso. Te decimos exactamente qué haríamos y cuánto costaría.</p>
        <Link href="/contacto"
          className="bg-indigo-600 hover:bg-indigo-500 text-white font-semibold px-10 py-5 rounded-xl text-lg transition-colors inline-block">
          Reservar consulta gratuita →
        </Link>
      </section>
    </main>
  );
}
