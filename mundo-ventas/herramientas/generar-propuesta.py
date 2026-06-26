"""
NEXIA — Generador de Propuestas Comerciales
Uso: python generar-propuesta.py --empresa "Clínica García" --sector "salud" --presupuesto 1497
"""
import argparse, json, datetime, os, sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import llm

OUT_DIR = Path(__file__).resolve().parent.parent / "propuestas"
OUT_DIR.mkdir(parents=True, exist_ok=True)

PAQUETES = {
    497:  ("Starter",      "Landing page + chatbot básico",   "5 días hábiles"),
    1497: ("Growth",       "App web completa + dashboard",    "3 semanas"),
    4997: ("Agency Pro",   "Sistema a medida + integración",  "6 semanas"),
}

def generar(empresa, sector, presupuesto, contacto="", necesidad=""):
    paquete_key = min(PAQUETES.keys(), key=lambda k: abs(k - presupuesto))
    nombre_paquete, descripcion_paquete, entrega = PAQUETES[paquete_key]

    prompt = f"""Genera una propuesta comercial profesional de NEXIA para:

CLIENTE: {empresa}
SECTOR: {sector}
CONTACTO: {contacto or 'Equipo directivo'}
NECESIDAD: {necesidad or 'Automatizar procesos con IA'}
PAQUETE: {nombre_paquete} — {descripcion_paquete}
INVERSIÓN: {presupuesto}€
ENTREGA: {entrega}

ESTRUCTURA OBLIGATORIA:
# Propuesta NEXIA para {empresa}
*Referencia: NEXIA-{datetime.date.today().strftime('%Y%m%d')}-{empresa[:4].upper()}*

## 1. Resumen Ejecutivo
[3 líneas: contexto, solución, resultado esperado]

## 2. El Problema que Resolvemos
[Diagnóstico específico del sector {sector}]

## 3. Nuestra Solución
[Descripción técnica del {nombre_paquete}: qué incluye, cómo funciona]

## 4. Plan de Implementación
[Fases con duración, hitos claros]

## 5. Inversión
| Concepto | Precio |
|---------|--------|
| {nombre_paquete} (pago único) | {presupuesto}€ |
| Soporte primer mes | INCLUIDO |
| Hosting/mantenimiento | Desde 49€/mes (opcional) |

**Total: {presupuesto}€ + IVA**

## 6. Garantías
- 30 días de ajustes sin coste adicional
- Soporte técnico incluido durante la implementación
- Si no cumple los objetivos en 60 días, devolvemos el 50%

## 7. Próximos Pasos
1. Reunión de kickoff (15 min) para validar requisitos
2. Firma de contrato y pago del 50% inicial
3. Inicio del proyecto en menos de 48h

---
*NEXIA — nexia.io | hola@nexia.io*
*"Tu negocio trabajando 24/7 con IA"*

Escribe la propuesta completa, profesional y convincente. Adapta el contenido al sector {sector}."""

    print(f"Generando propuesta para {empresa} ({sector}, {presupuesto}€)...")
    contenido = llm.generar(prompt, max_tokens=1000)

    fecha = datetime.date.today().isoformat()
    nombre_archivo = f"propuesta_{empresa.lower().replace(' ','_').replace('/','_')}_{fecha}.md"
    ruta = OUT_DIR / nombre_archivo
    ruta.write_text(contenido, encoding="utf-8")

    print(f"\n{'='*60}")
    print(f"[OK] Propuesta guardada:")
    print(f"  {ruta}")
    print(f"{'='*60}")
    print(contenido[:500] + "..." if len(contenido) > 500 else contenido)
    return str(ruta)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--empresa", required=True, help="Nombre de la empresa")
    parser.add_argument("--sector", default="pyme", help="Sector/industria")
    parser.add_argument("--presupuesto", type=int, default=1497, help="Presupuesto en euros (497/1497/4997)")
    parser.add_argument("--contacto", default="", help="Nombre del contacto")
    parser.add_argument("--necesidad", default="", help="Necesidad específica del cliente")
    args = parser.parse_args()
    generar(args.empresa, args.sector, args.presupuesto, args.contacto, args.necesidad)
