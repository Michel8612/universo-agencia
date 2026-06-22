"""
Generador de mensajes de outreach personalizados para LinkedIn/Email
Uso: python outreach-linkedin.py --empresa "Clínica Dental López" --sector "salud" --canal "linkedin"
"""
import argparse
import os

MENSAJES = {
    "linkedin": {
        "conexion": """Hola {nombre},

Vi que llevas {empresa} y me llamó la atención cómo están trabajando en {sector}.

Llevo un tiempo ayudando a empresas del sector a {beneficio_principal} con IA. Los resultados que estamos viendo son bastante interesantes.

¿Te parece si conectamos? Me encantaría saber más sobre los retos que tenéis ahora mismo.""",

        "seguimiento_1": """Hola {nombre}, gracias por conectar.

Quería compartirte algo breve: hace poco implementamos {caso_uso} para una empresa similar a {empresa} en el sector {sector}. En 30 días lograron {resultado_ejemplo}.

¿Tienes 20 minutos esta semana para una llamada exploratoria? Sin compromiso, solo para ver si hay encaje.""",

        "seguimiento_2": """Hola {nombre},

Entiendo que estás muy ocupado. Solo un mensaje más y no molesto.

Tenemos un caso de uso específico para {sector} que ha funcionado muy bien: {caso_uso_especifico}.

Si en algún momento quieres explorar cómo podría aplicarse en {empresa}, aquí estaré. Un saludo.""",
    },

    "email": {
        "inicial": """Asunto: {empresa} + IA — {beneficio_corto}

Hola {nombre},

Te escribo porque trabajamos con empresas de {sector} ayudándolas a {beneficio_principal} usando inteligencia artificial.

Recientemente ayudamos a [EMPRESA SIMILAR] a conseguir:
→ {resultado_1}
→ {resultado_2}
→ {resultado_3}

¿Tendría sentido hablar 20 minutos para ver si algo de esto encaja con {empresa}?

Puedes reservar tiempo directamente aquí: {cal_link}

Un saludo,
{nombre_agencia}""",

        "seguimiento_1": """Asunto: Re: {empresa} + IA

Hola {nombre},

Solo quería asegurarme de que te llegó mi email anterior.

Sé que tu bandeja de entrada está llena, así que voy al grano: tenemos una demo específica para {sector} que tarda 15 minutos y suele generar bastantes ideas útiles.

¿Esta semana o la próxima tienes un hueco? {cal_link}""",

        "break_up": """Asunto: ¿Lo dejamos aquí?

Hola {nombre},

He intentado contactarte un par de veces sin respuesta, así que entiendo que o no es el momento o no es relevante para {empresa}.

Si algún día quieres explorar cómo la IA puede {beneficio_principal} en {sector}, aquí estaré.

Mucho éxito con {empresa}.

{nombre_agencia}""",
    },
}

NICHOS = {
    "salud": {
        "beneficio_principal": "reducir el tiempo de atención al paciente y automatizar citas",
        "beneficio_corto": "30% menos tiempo en gestión administrativa",
        "caso_uso": "un chatbot de citas y atención al paciente 24/7",
        "caso_uso_especifico": "automatización de recordatorios de cita + chatbot de triaje",
        "resultado_ejemplo": "redujeron un 40% las llamadas entrantes y aumentaron un 25% las citas completadas",
        "resultado_1": "40% menos llamadas telefónicas entrantes",
        "resultado_2": "25% más citas completadas (menos no-shows)",
        "resultado_3": "Atención 24/7 sin contratar más personal",
    },
    "hosteleria": {
        "beneficio_principal": "automatizar reservas y mejorar la experiencia del huésped",
        "beneficio_corto": "reservas automáticas 24/7 sin intervención humana",
        "caso_uso": "un sistema de reservas con chatbot integrado",
        "caso_uso_especifico": "chatbot de reservas + upselling automático de servicios",
        "resultado_ejemplo": "aumentaron las reservas directas un 35% en 2 meses",
        "resultado_1": "35% más reservas directas (menos comisión a OTAs)",
        "resultado_2": "Respuesta instantánea a consultas en 5 idiomas",
        "resultado_3": "Upselling automático: +18% en ingreso por reserva",
    },
    "legal": {
        "beneficio_principal": "automatizar documentación y liberar tiempo de los abogados",
        "beneficio_corto": "contratos en minutos, no en horas",
        "caso_uso": "un sistema de generación automática de contratos",
        "caso_uso_especifico": "chatbot de primera consulta + generador de documentos legales",
        "resultado_ejemplo": "redujeron el tiempo de preparación de documentos un 70%",
        "resultado_1": "70% menos tiempo en preparación de documentos",
        "resultado_2": "Primera consulta automatizada (ahorra 1h/día por abogado)",
        "resultado_3": "Captación de leads 24/7 con cualificación automática",
    },
    "ecommerce": {
        "beneficio_principal": "aumentar conversiones y reducir el abandono de carrito",
        "beneficio_corto": "+20% conversión con IA en 30 días",
        "caso_uso": "un chatbot de ventas y recomendación de productos",
        "caso_uso_especifico": "recuperación automática de carritos abandonados con IA",
        "resultado_ejemplo": "recuperaron un 23% de carritos abandonados en el primer mes",
        "resultado_1": "23% de carritos abandonados recuperados",
        "resultado_2": "Recomendaciones personalizadas: +15% ticket medio",
        "resultado_3": "Atención al cliente 24/7 sin aumentar equipo",
    },
    "inmobiliaria": {
        "beneficio_principal": "cualificar leads automáticamente y agendar visitas sin intermediarios",
        "beneficio_corto": "leads cualificados 24/7, visitas agendadas solas",
        "caso_uso": "un chatbot que cualifica compradores y agenda visitas automáticamente",
        "caso_uso_especifico": "asistente IA que responde dudas de propiedades + agenda visitas en tiempo real",
        "resultado_ejemplo": "pasaron de 5 a 18 visitas semanales sin contratar más agentes",
        "resultado_1": "18 visitas/semana (3.6x más sin más personal)",
        "resultado_2": "Respuesta inmediata a leads: 0% abandonan por espera",
        "resultado_3": "Cualificación automática: solo ven pisos quienes pueden comprar",
    },
    "restaurante": {
        "beneficio_principal": "gestionar reservas y pedidos online sin perder ninguna llamada",
        "beneficio_corto": "cero llamadas perdidas, más mesas llenas",
        "caso_uso": "un sistema de reservas online con recordatorios automáticos por WhatsApp",
        "caso_uso_especifico": "chatbot de reservas + gestión de alérgenos + upselling de menú del día",
        "resultado_ejemplo": "eliminaron el 100% de las llamadas perdidas y llenaron el 90% de mesas",
        "resultado_1": "0 reservas perdidas por llamada no contestada",
        "resultado_2": "90% de ocupación vs 65% anterior",
        "resultado_3": "Recordatorios automáticos: -60% de no-shows",
    },
    "formacion": {
        "beneficio_principal": "automatizar captación de alumnos y soporte post-venta",
        "beneficio_corto": "alumnos captados 24/7 sin equipo de ventas",
        "caso_uso": "un funnel de ventas automatizado con chatbot de orientación",
        "caso_uso_especifico": "chatbot que orienta al alumno, resuelve dudas del curso y gestiona matrículas",
        "resultado_ejemplo": "triplicaron las matrículas sin contratar comerciales",
        "resultado_1": "3x más matrículas en 60 días",
        "resultado_2": "Soporte al alumno 24/7 sin personal adicional",
        "resultado_3": "Conversión landing→matrícula de 8% a 23%",
    },
    "logistica": {
        "beneficio_principal": "automatizar el seguimiento de envíos y reducir llamadas al servicio de atención",
        "beneficio_corto": "-70% llamadas al SAC con IA de seguimiento",
        "caso_uso": "un chatbot de seguimiento de pedidos en tiempo real",
        "caso_uso_especifico": "integración con tu sistema de tracking + chatbot WhatsApp para clientes",
        "resultado_ejemplo": "redujeron las llamadas al SAC un 70% en el primer mes",
        "resultado_1": "70% menos llamadas al servicio al cliente",
        "resultado_2": "Seguimiento en tiempo real vía WhatsApp automático",
        "resultado_3": "Ahorro de 2 FTEs en el equipo de atención",
    },
    "clinica_estetica": {
        "beneficio_principal": "llenar la agenda de tratamientos y reducir cancelaciones",
        "beneficio_corto": "agenda llena, cancelaciones eliminadas con IA",
        "caso_uso": "un sistema de gestión de citas con IA y recordatorios automáticos",
        "caso_uso_especifico": "chatbot de asesoramiento de tratamientos + agenda online + recordatorios WhatsApp",
        "resultado_ejemplo": "pasaron de 60% a 95% de ocupación y eliminaron cancelaciones de última hora",
        "resultado_1": "95% de ocupación de agenda (antes 60%)",
        "resultado_2": "-80% cancelaciones con recordatorios inteligentes",
        "resultado_3": "Upselling automático de tratamientos complementarios",
    },
}

def generar_secuencia(empresa, nombre_contacto, sector, canal, agencia_nombre=None, cal_link=None):
    nicho = NICHOS.get(sector, NICHOS["ecommerce"])
    agencia = agencia_nombre or os.getenv("AGENCIA_NOMBRE", "NEXIA")
    cal = cal_link or os.getenv("CAL_LINK", "https://cal.com/nexia-ia")

    plantillas = MENSAJES.get(canal, MENSAJES["email"])
    secuencia = []

    for key, template in plantillas.items():
        msg = template.format(
            nombre=nombre_contacto,
            empresa=empresa,
            sector=sector,
            agencia=agencia,
            nombre_agencia=agencia,
            cal_link=cal,
            **nicho,
        )
        secuencia.append({"tipo": key, "mensaje": msg})

    print(f"\n{'='*60}")
    print(f"SECUENCIA DE OUTREACH — {empresa} ({canal.upper()})")
    print(f"{'='*60}")
    for i, item in enumerate(secuencia, 1):
        print(f"\n--- MENSAJE {i}: {item['tipo'].upper()} ---")
        print(item["mensaje"])

    return secuencia

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--empresa", required=True)
    parser.add_argument("--contacto", default="equipo")
    parser.add_argument("--sector", required=True, choices=list(NICHOS.keys()),
                        metavar=f"SECTOR ({'/'.join(NICHOS.keys())})")
    parser.add_argument("--canal", default="email", choices=["linkedin", "email"])
    args = parser.parse_args()
    generar_secuencia(args.empresa, args.contacto, args.sector, args.canal)
