import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Términos de Servicio",
  description: "Condiciones de uso de los servicios de NEXIA.",
  robots: { index: true, follow: true },
};

const EMAIL = "teamorionglobal@gmail.com";

export default function Terminos() {
  return (
    <main className="min-h-screen bg-[#08080c] text-gray-300 px-6 py-20">
      <article className="max-w-3xl mx-auto">
        <Link href="/" className="text-blue-400 text-sm hover:text-blue-300">← Volver al inicio</Link>
        <h1 className="text-3xl font-bold text-white mt-6 mb-2">Términos de Servicio</h1>
        <p className="text-sm text-gray-500 mb-8">Última actualización: 24 de junio de 2026</p>

        <div className="space-y-6 text-sm leading-relaxed">
          <Sec n="1" t="Aceptación">
            <p>Al contactar con NEXIA, solicitar un presupuesto o contratar nuestros servicios, aceptas estos Términos. Si no estás de acuerdo, no uses el servicio.</p>
          </Sec>
          <Sec n="2" t="Descripción del servicio">
            <p>NEXIA presta servicios de desarrollo web, chatbots e inteligencia artificial, automatización y marketing digital. Podemos modificar, mejorar o discontinuar funciones y servicios.</p>
          </Sec>
          <Sec n="3" t="Elegibilidad y cuentas">
            <p>Debes ser mayor de 18 años y facilitar información veraz. Eres responsable de la actividad y de las credenciales de cualquier cuenta o sistema que te entreguemos.</p>
          </Sec>
          <Sec n="4" t="Pagos">
            <p>Salvo acuerdo distinto, los proyectos se abonan <strong>50% al inicio y 50% a la entrega aprobada</strong>. Los servicios recurrentes (mantenimiento, gestión) se facturan por adelantado. Los precios pueden cambiar con aviso previo. Los impuestos aplicables corren según tu jurisdicción.</p>
          </Sec>
          <Sec n="5" t="Cancelaciones y reembolsos">
            <p>Puedes cancelar un servicio recurrente cuando quieras; no se reembolsan periodos ya facturados. En proyectos, el pago inicial cubre el trabajo ya realizado y no es reembolsable una vez comenzado.</p>
          </Sec>
          <Sec n="6" t="Uso aceptable">
            <p>No puedes usar nuestros servicios para actividades ilegales, envío de spam, vulnerar la seguridad, hacer ingeniería inversa ni revender el acceso sin autorización.</p>
          </Sec>
          <Sec n="7" t="Contenido del cliente">
            <p>Conservas la propiedad de los contenidos y datos que nos facilitas. Nos otorgas una licencia limitada para alojarlos y procesarlos con el único fin de prestar el servicio.</p>
          </Sec>
          <Sec n="8" t="Propiedad intelectual">
            <p>El software, marca, diseño y metodología de NEXIA son de nuestra propiedad. Los entregables finales pasan a ser tuyos una vez abonado el importe completo.</p>
          </Sec>
          <Sec n="9" t="Inteligencia Artificial">
            <p>Algunos servicios usan IA. Los resultados pueden contener errores y no constituyen asesoramiento profesional. No prometemos precisión absoluta ni la sustitución de profesionales (legales, médicos, financieros).</p>
          </Sec>
          <Sec n="10" t="Limitación de responsabilidad">
            <p>El servicio se ofrece &quot;tal cual&quot; y &quot;según disponibilidad&quot;. En la medida permitida por la ley, no somos responsables de daños indirectos ni de pérdida de datos o ganancias. Nuestra responsabilidad total se limita al importe que nos hayas abonado en los últimos 6 meses.</p>
          </Sec>
          <Sec n="11" t="Indemnización">
            <p>Aceptas indemnizarnos por reclamaciones derivadas de un uso indebido de los servicios.</p>
          </Sec>
          <Sec n="12" t="Terminación">
            <p>Podemos suspender o cerrar el servicio a quien incumpla estos Términos.</p>
          </Sec>
          <Sec n="13" t="Ley aplicable">
            <p>Estos Términos se rigen por la legislación aplicable en la jurisdicción de NEXIA. Las disputas se resolverán ante los tribunales competentes de dicha jurisdicción.</p>
          </Sec>
          <Sec n="14" t="Cambios y contacto">
            <p>Podemos actualizar estos Términos; te avisaremos por email o aviso en la web. Contacto: <a href={`mailto:${EMAIL}`} className="text-blue-400">{EMAIL}</a>.</p>
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
