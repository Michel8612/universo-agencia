import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Política de Cookies",
  description: "Qué cookies usa la web de NEXIA.",
  robots: { index: true, follow: true },
};

export default function Cookies() {
  return (
    <main className="min-h-screen bg-[#08080c] text-gray-300 px-6 py-20">
      <article className="max-w-3xl mx-auto">
        <Link href="/" className="text-blue-400 text-sm hover:text-blue-300">← Volver al inicio</Link>
        <h1 className="text-3xl font-bold text-white mt-6 mb-2">Política de Cookies</h1>
        <p className="text-sm text-gray-500 mb-8">Última actualización: 24 de junio de 2026</p>

        <div className="space-y-6 text-sm leading-relaxed">
          <p>Una cookie es un pequeño archivo que un sitio web guarda en tu navegador. Te explicamos cuáles usamos.</p>

          <section>
            <h2 className="text-lg font-semibold text-white mb-2">Cookies que usamos</h2>
            <p>Actualmente esta web usa <strong>únicamente cookies técnicas esenciales</strong> necesarias para que funcione correctamente. No usamos cookies de publicidad ni de seguimiento de terceros.</p>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-white mb-2">Si en el futuro usamos analítica</h2>
            <p>Si activamos herramientas de analítica (por ejemplo, para entender qué páginas se visitan), te lo pediremos mediante el banner de consentimiento y actualizaremos esta política con el detalle de cada cookie, su finalidad y su duración.</p>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-white mb-2">Cómo gestionarlas</h2>
            <p>Puedes bloquear o eliminar cookies desde la configuración de tu navegador. Bloquear las esenciales puede afectar al funcionamiento de la web.</p>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-white mb-2">Más información</h2>
            <p>Consulta también nuestra <Link href="/privacidad" className="text-blue-400">Política de Privacidad</Link>.</p>
          </section>
        </div>
      </article>
    </main>
  );
}
