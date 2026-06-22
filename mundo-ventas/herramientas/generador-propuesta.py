"""
Generador automático de propuestas comerciales en PDF
Uso: python generador-propuesta.py --cliente "Empresa X" --servicio "chatbot" --presupuesto 1500
"""
import argparse
import os
import json
from datetime import datetime, timedelta
from pathlib import Path

PLANTILLA_PROPUESTA = """
# PROPUESTA COMERCIAL
**{agencia}** | {fecha}
Propuesta #{numero} — Válida hasta {validez}

---

## Para: {cliente}
**Atención:** {contacto}
**Servicio solicitado:** {servicio}

---

## El Problema que Resolvemos

{descripcion_problema}

## Nuestra Solución

{descripcion_solucion}

## Lo que Incluye

{items_incluidos}

## Timeline de Entrega

{timeline}

## Inversión

| Concepto | Importe |
|---------|---------|
{tabla_precios}
| **TOTAL** | **{precio_total}** |

*Formas de pago: 50% inicio + 50% entrega / Stripe / Transferencia*

## Por Qué Elegirnos

- ✅ Entregamos en los plazos acordados (garantía por escrito)
- ✅ Código propio, sin dependencias de terceros
- ✅ Soporte post-entrega incluido (30 días)
- ✅ Resultados medibles desde el día 1

## Próximos Pasos

1. Aprobación de esta propuesta (firma digital)
2. Pago del 50% para reservar fecha de inicio
3. Reunión de kickoff para recopilar accesos y materiales
4. Inicio del desarrollo: {fecha_inicio}

---

*{agencia} — Agencia de Inteligencia Artificial*
*{email_agencia} | {web_agencia}*
"""

SERVICIOS = {
    "chatbot": {
        "descripcion_problema": "Los negocios pierden clientes potenciales fuera del horario de atención. Un visitante que no recibe respuesta inmediata, se va a la competencia.",
        "descripcion_solucion": "Implementamos un asistente de IA entrenado específicamente con la información de su negocio. Responde al instante, 24/7, en cualquier idioma, y cualifica leads automáticamente.",
        "items": ["✅ Chatbot con IA entrenado con sus datos", "✅ Integración en su web (1 línea de código)", "✅ Panel de administración para ver conversaciones", "✅ Alertas cuando un cliente necesita atención humana", "✅ Soporte y ajustes durante 30 días"],
        "timeline": "| Semana 1 | Recopilación de info y entrenamiento |\n| Semana 2 | Desarrollo e integración |\n| Semana 3 | Pruebas y ajustes |\n| Semana 4 | Entrega y formación |",
    },
    "app-web": {
        "descripcion_problema": "Muchos negocios operan con procesos manuales que consumen tiempo y generan errores. La digitalización ya no es opcional — es supervivencia.",
        "descripcion_solucion": "Desarrollamos la aplicación web a medida que automatiza sus procesos clave. Desde el diseño hasta el deploy, entregamos un producto completo y funcional.",
        "items": ["✅ Diseño UX/UI profesional", "✅ Frontend moderno y responsive", "✅ Backend robusto con base de datos", "✅ Panel de administración", "✅ Deploy en producción con dominio y SSL", "✅ Documentación técnica completa"],
        "timeline": "| Semanas 1-2 | Diseño y arquitectura |\n| Semanas 3-5 | Desarrollo |\n| Semana 6 | Testing y deploy |",
    },
    "social-media": {
        "descripcion_problema": "Mantener presencia constante en redes sociales consume horas que los dueños de negocio no tienen, y si se delega mal, daña la imagen de marca.",
        "descripcion_solucion": "Gestionamos sus redes con IA: generamos contenido personalizado, publicamos en los mejores horarios y monitorizamos resultados, todo en piloto automático.",
        "items": ["✅ 90 posts/mes (3 diarios)", "✅ Diseño visual consistente con su marca", "✅ Copy optimizado para engagement", "✅ Hashtag research mensual", "✅ Reporte mensual de métricas"],
        "timeline": "| Días 1-3 | Onboarding y estrategia |\n| Día 7 | Primeros posts publicados |\n| Mes 2+ | Optimización basada en datos |",
    },
    "auditoria-lopd": {
        "descripcion_problema": "El incumplimiento del RGPD/LOPD puede acarrear multas de hasta 20 millones de euros. La mayoría de empresas desconoce su nivel real de riesgo.",
        "descripcion_solucion": "Realizamos una auditoría completa de cómo su empresa trata los datos personales, identificamos brechas legales y entregamos un plan de acción priorizado.",
        "items": ["✅ Inventario de tratamientos de datos", "✅ Análisis de riesgo por tratamiento", "✅ Revisión de contratos con proveedores", "✅ Informe ejecutivo y técnico", "✅ Plan de acción con prioridades", "✅ Plantillas de avisos legales y políticas"],
        "timeline": "| Semana 1 | Recopilación de información |\n| Semana 2 | Análisis y diagnóstico |\n| Semana 3 | Informe y presentación |",
    },
}

PRECIOS = {
    "chatbot":        {"base": 800,  "mensual": 79,   "moneda": "€"},
    "app-web":        {"base": 3500, "mensual": 0,    "moneda": "€"},
    "social-media":   {"base": 0,    "mensual": 997,  "moneda": "€"},
    "auditoria-lopd": {"base": 1200, "mensual": 0,    "moneda": "€"},
}

def generar_propuesta(cliente, contacto, servicio, precio_custom=None):
    if servicio not in SERVICIOS:
        print(f"❌ Servicio '{servicio}' no existe. Opciones: {list(SERVICIOS.keys())}")
        return

    info = SERVICIOS[servicio]
    precio_info = PRECIOS[servicio]
    moneda = precio_info["moneda"]
    precio_base = precio_custom or precio_info["base"]
    precio_mensual = precio_info["mensual"]

    tabla = f"| Setup / Implementación | {precio_base}{moneda} |\n"
    total = precio_base
    if precio_mensual:
        tabla += f"| Mantenimiento mensual | {precio_mensual}{moneda}/mes |\n"
        total_str = f"{precio_base}{moneda} + {precio_mensual}{moneda}/mes"
    else:
        total_str = f"{precio_base}{moneda}"

    numero = datetime.now().strftime("%Y%m%d%H%M")
    fecha_inicio = (datetime.now() + timedelta(days=7)).strftime("%d/%m/%Y")
    validez = (datetime.now() + timedelta(days=15)).strftime("%d/%m/%Y")

    propuesta = PLANTILLA_PROPUESTA.format(
        agencia=os.getenv("AGENCIA_NOMBRE", "Agencia IA"),
        email_agencia=os.getenv("AGENCIA_EMAIL", "hola@agencia.com"),
        web_agencia=os.getenv("AGENCIA_WEB", "www.agencia.com"),
        fecha=datetime.now().strftime("%d/%m/%Y"),
        numero=numero,
        validez=validez,
        cliente=cliente,
        contacto=contacto or "Responsable de área",
        servicio=servicio.replace("-", " ").title(),
        descripcion_problema=info["descripcion_problema"],
        descripcion_solucion=info["descripcion_solucion"],
        items_incluidos="\n".join(info["items"]),
        timeline=info["timeline"],
        tabla_precios=tabla,
        precio_total=total_str,
        fecha_inicio=fecha_inicio,
    )

    # Guardar en carpeta de propuestas
    output_dir = Path("D:/Proyectos claude/mundo-agencia/memoria/propuestas")
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = output_dir / f"propuesta_{numero}_{cliente.replace(' ', '_')}.md"
    filename.write_text(propuesta, encoding="utf-8")

    print(f"✅ Propuesta generada: {filename}")
    print(f"   Cliente: {cliente}")
    print(f"   Servicio: {servicio}")
    print(f"   Total: {total_str}")
    print(f"\nPara convertir a PDF:")
    print(f"   pandoc \"{filename}\" -o propuesta.pdf --pdf-engine=xelatex")
    return propuesta

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generador de propuestas comerciales")
    parser.add_argument("--cliente", required=True, help="Nombre de la empresa cliente")
    parser.add_argument("--contacto", default="", help="Nombre del contacto")
    parser.add_argument("--servicio", required=True, choices=list(SERVICIOS.keys()), help="Tipo de servicio")
    parser.add_argument("--precio", type=int, help="Precio personalizado (override del defecto)")
    args = parser.parse_args()
    generar_propuesta(args.cliente, args.contacto, args.servicio, args.precio)
