#!/usr/bin/env python3
"""
NEXIA — Motor de campaña de leads (multi-nicho × multi-ciudad, en bucle)

Recorre combinaciones de nicho+ciudad, encuentra negocios (OSM), diagnostica
su web, puntúa, redacta el PRIMER email personalizado con Ollama y lo guarda en
el CRM con estado de seguimiento. Sin duplicados entre ejecuciones (estado en JSON).
Pensado para correr en bucle (Task Scheduler/n8n) y llenar el pipeline solo.

IMPORTANTE — ENVÍO: este script SOLO prepara los emails. NO los envía.
Enviar en tandas controladas (20-40/día) con identidad + enlace de baja.
Cold email masivo desde Gmail crudo = cuenta suspendida. Ver CHECKLIST-LEGAL.md.

Uso:
  python campana-leads.py                      # corre las combos por defecto (1 pasada)
  python campana-leads.py --por-combo 5        # 5 leads por combinación
  python campana-leads.py --solo-listar        # ver las combinaciones configuradas
"""
import importlib.util, os, json, time, argparse, csv, urllib.request, sys
from datetime import datetime, timedelta

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(HERE))
from llm import generar as llm_generar

CRM_URL = "http://127.0.0.1:8080/crm/cliente"
STATE_PATH = os.path.join(HERE, "..", "campana-estado.json")
OUT_DIR = os.path.join(HERE, "..", "campanas")

def _load(name, fname):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, fname))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

scraper = _load("scraper_leads", "scraper-leads.py")
diag = _load("diagnostico_web", "diagnostico-web.py")

# Combinaciones por defecto: todas las líneas que vamos a trabajar
COMBOS = [
    ("dentistas", "Madrid"), ("dentistas", "Barcelona"),
    ("restaurantes", "Valencia"), ("restaurantes", "Sevilla"),
    ("fisioterapia", "Barcelona"), ("clinicas", "Madrid"),
    ("peluquerias", "Sevilla"), ("belleza", "Valencia"),
    ("gimnasios", "Madrid"), ("abogados", "Barcelona"),
    ("inmobiliarias", "Valencia"), ("talleres", "Sevilla"),
]

def cargar_estado():
    if os.path.exists(STATE_PATH):
        try:
            return json.load(open(STATE_PATH, encoding="utf-8"))
        except Exception:
            pass
    return {"vistos": []}

def guardar_estado(s):
    json.dump(s, open(STATE_PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

def email_primer_contacto(negocio, diagnostico, recs):
    problemas = "; ".join(diagnostico["hallazgos"][:3]) or "mejoras de presencia digital"
    servicios = ", ".join(f"{s['nombre']} ({diag.fmt_precio(s)})" for s in recs[:3]) or "desarrollo web y automatización"
    prompt = f"""Eres comercial de NEXIA (agencia de IA, web y automatización). Escribe un email FRÍO corto (máx 110 palabras), en español, profesional y nada agresivo, para el negocio "{negocio['nombre']}".

Detectamos en su web: {problemas}.
Servicios que encajan: {servicios}.

El email debe:
1. Asunto corto y concreto (incluye el nombre del negocio).
2. Mencionar 1-2 hallazgos reales de SU web (sin sonar a ataque).
3. Ofrecer un diagnóstico web gratuito completo.
4. Cerrar invitando a responder. Firmar como "Equipo NEXIA".
5. Acabar con una línea: "Si no te interesa, responde BAJA y no te volvemos a escribir."
Devuelve formato:
ASUNTO: ...
CUERPO: ..."""
    try:
        return llm_generar(prompt, temperature=0.7)
    except Exception as e:
        return f"(no se pudo generar: {e})"

def guardar_crm(negocio, diagnostico, recs, ciudad, nicho):
    valor = f"${sum(s['min'] for s in recs)}-{sum(s['max'] for s in recs)}" if recs else "?"
    payload = json.dumps({
        "nombre": negocio["nombre"],
        "contacto": negocio.get("email") or negocio.get("telefono") or "",
        "mundo": "mundo-ventas",
        "estado": "lead_campana_t0",  # t0 = primer contacto pendiente de enviar
        "presupuesto": 0,
        "notas": f"{nicho}/{ciudad} | web:{negocio.get('web','')} | problemas:{len(diagnostico['hallazgos'])} | valor:{valor} | {datetime.now().strftime('%Y-%m-%d')}",
    }).encode()
    try:
        req = urllib.request.Request(CRM_URL, data=payload, headers={"Content-Type": "application/json"})
        urllib.request.urlopen(req, timeout=8)
        return True
    except Exception:
        return False

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--por-combo", type=int, default=4, help="leads (con web) por combinación")
    ap.add_argument("--combos", type=int, default=len(COMBOS), help="cuántas combinaciones procesar")
    ap.add_argument("--sin-email", action="store_true", help="no generar emails (solo encontrar + diagnosticar)")
    ap.add_argument("--solo-listar", action="store_true")
    args = ap.parse_args()

    if args.solo_listar:
        print("Combinaciones configuradas:")
        for n, c in COMBOS:
            print(f"  - {n} en {c}")
        return

    estado = cargar_estado()
    vistos = set(estado["vistos"])
    catalogo = diag.cargar_catalogo()
    resultados = []

    print(f"=== Campaña NEXIA — {min(args.combos, len(COMBOS))} líneas, {args.por_combo} leads/línea ===\n")
    for nicho, ciudad in COMBOS[:args.combos]:
        print(f"▶ {nicho} en {ciudad}")
        try:
            elementos, _ = scraper.buscar_negocios(nicho, ciudad, None, 60, "Spain")
        except Exception as e:
            print(f"   error: {e}"); continue
        nuevos = 0
        for el in elementos:
            if nuevos >= args.por_combo:
                break
            t = el.get("tags", {})
            nombre = t.get("name")
            web = t.get("website") or t.get("contact:website")
            if not nombre or not web:
                continue
            clave = f"{nombre}|{ciudad}".lower()
            if clave in vistos:
                continue
            negocio = {"nombre": nombre, "web": web,
                       "telefono": t.get("phone") or t.get("contact:phone") or "",
                       "email": t.get("email") or t.get("contact:email") or ""}
            # enriquecer email desde la web
            if not negocio["email"]:
                negocio["email"] = scraper.enriquecer_email(web)
            # diagnosticar
            d = diag.diagnosticar(web)
            recs = diag.recomendar_servicios(d["señales"], catalogo)
            negocio["email_draft"] = "" if args.sin_email else email_primer_contacto(negocio, d, recs)
            guardar_crm(negocio, d, recs, ciudad, nicho)
            vistos.add(clave)
            resultados.append({"nicho": nicho, "ciudad": ciudad, **negocio,
                               "problemas": len(d["hallazgos"]),
                               "valor_min": sum(s["min"] for s in recs),
                               "valor_max": sum(s["max"] for s in recs)})
            nuevos += 1
            mail = "✉" if negocio["email"] else "·"
            print(f"   {mail} {nombre[:32]:32} | {len(d['hallazgos'])} problemas | ${sum(s['min'] for s in recs)}-{sum(s['max'] for s in recs)}")
            time.sleep(0.3)
        print(f"   → {nuevos} leads nuevos\n")

    estado["vistos"] = list(vistos)
    guardar_estado(estado)

    # guardar campaña
    os.makedirs(OUT_DIR, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M")
    md = os.path.join(OUT_DIR, f"campana-{stamp}.md")
    with open(md, "w", encoding="utf-8") as f:
        f.write(f"# Campaña NEXIA — {stamp}\n\n{len(resultados)} leads nuevos. Revisa, y ENVÍA en tandas de 20-40/día.\n\n")
        for r in resultados:
            f.write(f"## {r['nombre']} ({r['nicho']}/{r['ciudad']})\n")
            f.write(f"- 🌐 {r['web']} | ✉ {r.get('email') or 'sin email'} | ☎ {r.get('telefono') or '-'}\n")
            f.write(f"- {r['problemas']} problemas detectados | valor potencial ${r['valor_min']}-{r['valor_max']}\n")
            if r.get("email_draft"):
                f.write(f"\n{r['email_draft']}\n")
            f.write("\n---\n\n")

    con_email = sum(1 for r in resultados if r.get("email"))
    print(f"=== {len(resultados)} leads nuevos | {con_email} con email | total histórico: {len(vistos)} ===")
    print(f"Campaña guardada: {md}")

if __name__ == "__main__":
    main()
