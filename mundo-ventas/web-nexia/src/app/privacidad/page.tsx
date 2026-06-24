import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Política de Privacidad",
  description: "Cómo NEXIA recoge, usa y protege tus datos personales.",
  robots: { index: true, follow: true },
};

const EMAIL = "teamorionglobal@gmail.com";

export default function Privacidad() {
  return (
    <main className="min-h-screen bg-[#08080c] text-gray-300 px-6 py-20">
      <article className="max-w-3xl mx-auto">
        <Link href="/" className="text-blue-400 text-sm hover:text-blue-300">← Volver al inicio</Link>
        <h1 className="text-3xl font-bold text-white mt-6 mb-2">Política de Privacidad</h1>
        <p className="text-sm text-gray-500 mb-8">Última actualización: 24 de junio de 2026</p>

        <div className="space-y-6 text-sm leading-relaxed">
          <p>En NEXIA respetamos tu privacidad. Esta política explica qué datos recogemos, para qué los usamos y qué derechos tienes.</p>

          <Sec n="1" t="Quiénes somos">
            <p><strong>NEXIA</strong>, agencia de inteligencia artificial, desarrollo web y automatización. Responsable del tratamiento de tus datos. Contacto: <a href={`mailto:${EMAIL}`} className="text-blue-400">{EMAIL}</a>.</p>
          </Sec>

          <Sec n="2" t="Qué datos recogemos">
            <ul className="list-disc pl-5 space-y-1">
              <li><strong>Datos de contacto</strong> que nos facilitas en el formulario: nombre, email, nombre del negocio y la dirección de tu web.</li>
              <li><strong>El mensaje</strong> que nos escribes voluntariamente.</li>
              <li><strong>Datos técnicos básicos</strong> de navegación (dirección IP, navegador) que genera el alojamiento de la web.</li>
            </ul>
            <p className="mt-2">No recogemos datos de pago en esta web. No solicitamos datos sensibles.</p>
          </Sec>

          <Sec n="3" t="Para qué los usamos">
            <p>Para responder a tu solicitud, prepararte el diagnóstico web gratuito, enviarte una propuesta y, si nos lo autorizas, hacerte seguimiento comercial. También para cumplir obligaciones legales.</p>
          </Sec>

          <Sec n="4" t="Base legal (GDPR)">
            <p>Tratamos tus datos sobre la base de tu <strong>consentimiento</strong> (al enviar el formulario) y de nuestro <strong>interés legítimo</strong> en responder a solicitudes comerciales.</p>
          </Sec>

          <Sec n="5" t="Con quién los compartimos">
            <p>Usamos proveedores (subprocesadores) que tratan datos por nosotros únicamente para operar el servicio:</p>
            <ul className="list-disc pl-5 space-y-1 mt-2">
              <li><strong>Netlify</strong> — alojamiento de la web.</li>
              <li><strong>FormSubmit</strong> — procesa el envío del formulario de contacto hasta nuestro email.</li>
              <li><strong>Proveedor de correo</strong> (Google / Gmail) — recepción y gestión de tus mensajes.</li>
              <li><strong>Modelos de IA</strong> — usados internamente para análisis; cuando aplica, sobre infraestructura local.</li>
            </ul>
            <p className="mt-2"><strong>No vendemos tus datos</strong> a terceros.</p>
          </Sec>

          <Sec n="6" t="Cuánto tiempo los guardamos">
            <p>Conservamos tus datos mientras gestionamos tu solicitud y la relación comercial, y el tiempo necesario para cumplir obligaciones legales. Puedes pedir su borrado en cualquier momento.</p>
          </Sec>

          <Sec n="7" t="Tus derechos">
            <p>Puedes solicitar acceso, corrección, borrado, portabilidad u oposición al tratamiento de tus datos escribiendo a <a href={`mailto:${EMAIL}`} className="text-blue-400">{EMAIL}</a>. Responderemos en el plazo que exija la ley.</p>
          </Sec>

          <Sec n="8" t="Cookies">
            <p>Esta web usa únicamente cookies esenciales para su funcionamiento. Consulta nuestra <Link href="/cookies" className="text-blue-400">Política de Cookies</Link>.</p>
          </Sec>

          <Sec n="9" t="Uso de Inteligencia Artificial">
            <p>NEXIA utiliza sistemas de IA para analizar webs y generar contenido. Los resultados de la IA pueden contener errores y no sustituyen el asesoramiento profesional. No utilizamos tus datos para entrenar modelos sin tu consentimiento explícito.</p>
          </Sec>

          <Sec n="10" t="Menores">
            <p>Este servicio no está dirigido a menores de 16 años y no recogemos sus datos de forma consciente.</p>
          </Sec>

          <Sec n="11" t="Cambios">
            <p>Podemos actualizar esta política. Publicaremos siempre la fecha de la última revisión al inicio.</p>
          </Sec>

          <Sec n="12" t="Contacto">
            <p>Para cualquier cuestión sobre tus datos: <a href={`mailto:${EMAIL}`} className="text-blue-400">{EMAIL}</a>.</p>
          </Sec>
        </div>
      </article>
    </main>
  );
}

function Sec({ n, t, children }: { n: string; t: string; children: React.ReactNode }) {
  return (
    <section>
      <h2 className="text-lg font-semibold text-white mb-2">{n}. {t}</h2>
      {children}
    </section>
  );
}
