#!/usr/bin/env python3
"""
NEXIA — Campaña de leads para TODO Estados Unidos (en bucle infinito, robusto).

Qué hace cada vuelta:
  Para cada combinación NICHO × CIUDAD (todos los estados):
    1. Busca negocios en OpenStreetMap (Overpass + Nominatim).
    2. Para los que tienen web: enriquece email + DIAGNÓSTICO WEB COMPLETO
       (velocidad, móvil, SSL, SEO, chat, formulario, analytics, redes...).
    3. Mapea problemas → servicios del catálogo con precio (rol de la agencia).
    4. Redacta el primer email frío con IA (Groq/Ollama) y guarda en el CRM.
  Sin duplicados entre vueltas (estado JSON). Resume donde se quedó.

DISEÑO ANTI-BLOQUEO ("no quemar la cuenta"):
  - Nominatim: 1.2s por ciudad (límite oficial) + pausa entre combos.
  - Overpass: varios mirrors con fallback + UA de navegador (ya en scraper-leads).
  - Pausa larga entre vueltas completas (no martillea OSM 24/7).
  - NO envía emails (solo los prepara) → imposible quemar la cuenta de correo.
  - Todo en try/except: un fallo NUNCA detiene el bucle (0 crashes).

Uso:
  python campana-usa.py                 # bucle infinito (déjalo corriendo en el servidor)
  python campana-usa.py --once          # una sola vuelta (para probar en vivo)
  python campana-usa.py --solo-listar   # imprime combos y valida nichos (offline, 0 red)
  python campana-usa.py --por-combo 6 --pausa-combo 4 --pausa-vuelta 3600
"""
import importlib.util, os, json, time, argparse, sys, traceback
from datetime import datetime

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import llm

CRM_URL = "http://127.0.0.1:8080/crm/cliente"
STATE_PATH = os.path.join(HERE, "..", "campana-usa-estado.json")
OUT_DIR = os.path.join(HERE, "..", "campanas")
LOG_PATH = os.path.join(HERE, "..", "campana-usa.log")


def _load(name, fname):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, fname))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


scraper = _load("scraper_leads", "scraper-leads.py")
diag = _load("diagnostico_web", "diagnostico-web.py")

PAIS = "United States"

# Ciudades principales por estado (cobertura de los 50 estados + DC).
CIUDADES_USA = [
    "Birmingham, Alabama", "Montgomery, Alabama", "Anchorage, Alaska",
    "Phoenix, Arizona", "Tucson, Arizona", "Mesa, Arizona",
    "Little Rock, Arkansas", "Los Angeles, California", "San Diego, California",
    "San Jose, California", "San Francisco, California", "Sacramento, California",
    "Fresno, California", "Denver, Colorado", "Colorado Springs, Colorado",
    "Hartford, Connecticut", "Bridgeport, Connecticut", "Wilmington, Delaware",
    "Miami, Florida", "Orlando, Florida", "Tampa, Florida", "Jacksonville, Florida",
    "Fort Lauderdale, Florida", "St. Petersburg, Florida", "Atlanta, Georgia",
    "Savannah, Georgia", "Honolulu, Hawaii", "Boise, Idaho",
    "Chicago, Illinois", "Aurora, Illinois", "Indianapolis, Indiana",
    "Fort Wayne, Indiana", "Des Moines, Iowa", "Wichita, Kansas",
    "Kansas City, Kansas", "Louisville, Kentucky", "Lexington, Kentucky",
    "New Orleans, Louisiana", "Baton Rouge, Louisiana", "Portland, Maine",
    "Baltimore, Maryland", "Boston, Massachusetts", "Worcester, Massachusetts",
    "Detroit, Michigan", "Grand Rapids, Michigan", "Minneapolis, Minnesota",
    "St. Paul, Minnesota", "Jackson, Mississippi", "Kansas City, Missouri",
    "St. Louis, Missouri", "Billings, Montana", "Omaha, Nebraska",
    "Lincoln, Nebraska", "Las Vegas, Nevada", "Reno, Nevada",
    "Manchester, New Hampshire", "Newark, New Jersey", "Jersey City, New Jersey",
    "Albuquerque, New Mexico", "New York, New York", "Buffalo, New York",
    "Rochester, New York", "Charlotte, North Carolina", "Raleigh, North Carolina",
    "Greensboro, North Carolina", "Fargo, North Dakota", "Columbus, Ohio",
    "Cleveland, Ohio", "Cincinnati, Ohio", "Oklahoma City, Oklahoma",
    "Tulsa, Oklahoma", "Portland, Oregon", "Philadelphia, Pennsylvania",
    "Pittsburgh, Pennsylvania", "Providence, Rhode Island", "Columbia, South Carolina",
    "Charleston, South Carolina", "Sioux Falls, South Dakota", "Nashville, Tennessee",
    "Memphis, Tennessee", "Knoxville, Tennessee", "Houston, Texas", "San Antonio, Texas",
    "Dallas, Texas", "Austin, Texas", "Fort Worth, Texas", "El Paso, Texas",
    "Salt Lake City, Utah", "Burlington, Vermont", "Virginia Beach, Virginia",
    "Richmond, Virginia", "Seattle, Washington", "Spokane, Washington",
    "Charleston, West Virginia", "Milwaukee, Wisconsin", "Madison, Wisconsin",
    "Cheyenne, Wyoming", "Washington, District of Columbia",
]

# Nichos de alto valor para la agencia (necesitan web/chatbot/automatización).
NICHOS_USA = [
    "restaurantes", "dentistas", "abogados", "clinicas", "fisioterapia",
    "gimnasios", "inmobiliarias", "talleres", "veterinarios", "peluquerias",
    "belleza", "fontaneros", "electricistas", "reformas", "seguros",
]


def log(msg):
    linea = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    print(linea, flush=True)
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(linea + "\n")
    except Exception:
        pass


def cargar_estado():
    if os.path.exists(STATE_PATH):
        try:
            return json.load(open(STATE_PATH, encoding="utf-8"))
        except Exception:
            pass
    return {"vistos": [], "vueltas": 0}


def guardar_estado(s):
    try:
        json.dump(s, open(STATE_PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    except Exception as e:
        log(f"  [!] no se pudo guardar estado: {e}")


def email_primer_contacto(negocio, d, recs):
    problemas = "; ".join(d["hallazgos"][:3]) or "improving their online presence"
    servicios = ", ".join(f"{s['nombre']} ({diag.fmt_precio(s)})" for s in recs[:3]) or "web development and automation"
    prompt = f"""You are a senior sales rep for NEXIA (AI, web development and automation agency). Write a SHORT, PERSUASIVE cold email (max 120 words) in ENGLISH for the US business "{negocio['nombre']}". Professional, warm and confident — never pushy or spammy.

We detected on their website: {problemas}.
Services that fit: {servicios}.

Persuasion rules:
1. Subject: specific and benefit-driven, include the business name (focus on getting more customers from their site). No clickbait, no ALL CAPS.
2. Open with ONE concrete issue from THEIR site and its real cost in one relatable line (lost customers, missed bookings, lost trust).
3. Promise ONE clear outcome, not a feature list (more enquiries, a faster site, 24/7 booking).
4. Light credibility: we're selecting a few local businesses this month for a free website audit.
5. ONE clear call to action: reply to get a free, no-obligation audit within 24h.
6. Skimmable: short sentences, line breaks, no jargon. Sign as "NEXIA Team".
7. End with: "If this isn't for you, reply STOP and we won't email again."
Return format:
SUBJECT: ...
BODY: ..."""
    return llm.generar(prompt, max_tokens=400)


def guardar_crm(negocio, d, recs, ciudad, nicho):
    valor = f"${sum(s['min'] for s in recs)}-{sum(s['max'] for s in recs)}" if recs else "?"
    payload = json.dumps({
        "nombre": negocio["nombre"],
        "contacto": negocio.get("email") or negocio.get("telefono") or "",
        "mundo": "mundo-ventas",
        "estado": "lead_usa_t0",
        "presupuesto": 0,
        "notas": f"{nicho}/{ciudad} | web:{negocio.get('web','')} | problemas:{len(d['hallazgos'])} | valor:{valor} | {datetime.now().strftime('%Y-%m-%d')}",
    }).encode()
    try:
        req = scraper.urllib.request.Request(CRM_URL, data=payload, headers={"Content-Type": "application/json"})
        scraper.urllib.request.urlopen(req, timeout=8)
        return True
    except Exception:
        return False


def procesar_combo(nicho, ciudad, catalogo, vistos, por_combo, sin_email):
    """Procesa una combinación. Devuelve lista de leads nuevos. Nunca lanza."""
    resultados = []
    try:
        elementos, display = scraper.buscar_negocios(nicho, ciudad, None, 50, PAIS)
    except Exception as e:
        log(f"  [!] error buscando {nicho}/{ciudad}: {e}")
        return resultados
    nuevos = 0
    for el in elementos:
        if nuevos >= por_combo:
            break
        try:
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
            if not negocio["email"]:
                negocio["email"] = scraper.enriquecer_email(web)
            d = diag.diagnosticar(web)                      # ← análisis web completo
            recs = diag.recomendar_servicios(d["señales"], catalogo)
            negocio["email_draft"] = "" if sin_email else email_primer_contacto(negocio, d, recs)
            guardar_crm(negocio, d, recs, ciudad, nicho)
            vistos.add(clave)
            resultados.append({"nicho": nicho, "ciudad": ciudad, **negocio,
                               "problemas": len(d["hallazgos"]),
                               "valor_min": sum(s["min"] for s in recs),
                               "valor_max": sum(s["max"] for s in recs)})
            nuevos += 1
            mail = "@" if negocio["email"] else "."
            log(f"   {mail} {nombre[:34]:34} | {len(d['hallazgos'])} problemas | ${sum(s['min'] for s in recs)}-{sum(s['max'] for s in recs)}")
            time.sleep(0.5)
        except Exception as e:
            log(f"  [!] error procesando un negocio en {nicho}/{ciudad}: {e}")
            continue
    return resultados


def guardar_campana(resultados):
    if not resultados:
        return None
    try:
        os.makedirs(OUT_DIR, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d-%H%M")
        md = os.path.join(OUT_DIR, f"usa-{stamp}.md")
        with open(md, "w", encoding="utf-8") as f:
            f.write(f"# Campaña USA — {stamp}\n\n{len(resultados)} leads nuevos. Revisa y ENVÍA en tandas de 20-40/día (con opt-out).\n\n")
            for r in resultados:
                f.write(f"## {r['nombre']} ({r['nicho']}/{r['ciudad']})\n")
                f.write(f"- web: {r['web']} | email: {r.get('email') or 'sin email'} | tel: {r.get('telefono') or '-'}\n")
                f.write(f"- {r['problemas']} problemas | valor potencial ${r['valor_min']}-{r['valor_max']}\n")
                if r.get("email_draft"):
                    f.write(f"\n{r['email_draft']}\n")
                f.write("\n---\n\n")
        return md
    except Exception as e:
        log(f"  [!] no se pudo guardar la campaña: {e}")
        return None


def una_vuelta(args, catalogo, estado):
    vistos = set(estado["vistos"])
    combos = [(n, c) for c in CIUDADES_USA for n in NICHOS_USA]
    total = len(combos)
    log(f"=== VUELTA {estado['vueltas']+1}: {total} combos ({len(NICHOS_USA)} nichos × {len(CIUDADES_USA)} ciudades) ===")
    acumulado = []
    for i, (nicho, ciudad) in enumerate(combos, 1):
        log(f"[{i}/{total}] {nicho} · {ciudad}")
        res = procesar_combo(nicho, ciudad, catalogo, vistos, args.por_combo, args.sin_email)
        acumulado.extend(res)
        # persistir progreso tras cada combo (resume seguro si se corta)
        estado["vistos"] = list(vistos)
        guardar_estado(estado)
        if res:
            guardar_campana(res)
        time.sleep(args.pausa_combo)   # respeta OSM entre combos
    estado["vueltas"] += 1
    guardar_estado(estado)
    con_email = sum(1 for r in acumulado if r.get("email"))
    log(f"=== Vuelta completa: {len(acumulado)} leads nuevos | {con_email} con email | histórico: {len(vistos)} ===")
    return acumulado


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--once", action="store_true", help="una sola vuelta (no bucle)")
    ap.add_argument("--solo-listar", action="store_true", help="lista combos y valida nichos (offline)")
    ap.add_argument("--por-combo", type=int, default=6, help="leads con web por combinación")
    ap.add_argument("--pausa-combo", type=float, default=4.0, help="segundos entre combos (anti-bloqueo OSM)")
    ap.add_argument("--pausa-vuelta", type=int, default=3600, help="segundos entre vueltas completas")
    ap.add_argument("--sin-email", action="store_true", help="no generar emails (solo encontrar + diagnosticar)")
    args = ap.parse_args()

    combos = [(n, c) for c in CIUDADES_USA for n in NICHOS_USA]
    if args.solo_listar:
        invalidos = [n for n in NICHOS_USA if n not in scraper.NICHOS]
        print(f"Ciudades: {len(CIUDADES_USA)} | Nichos: {len(NICHOS_USA)} | Combos/vuelta: {len(combos)}")
        print(f"Nichos invalidos (deben ser 0): {invalidos}")
        print(f"Pais: {PAIS}")
        print("Ejemplos de combo:", combos[:3], "...", combos[-2:])
        return

    catalogo = diag.cargar_catalogo()
    estado = cargar_estado()
    log(f"INICIO campaña USA | por-combo={args.por_combo} pausa-combo={args.pausa_combo}s pausa-vuelta={args.pausa_vuelta}s")
    try:
        while True:
            una_vuelta(args, catalogo, estado)
            if args.once:
                log("Modo --once: fin.")
                break
            log(f"Durmiendo {args.pausa_vuelta}s antes de la próxima vuelta...")
            time.sleep(args.pausa_vuelta)
    except KeyboardInterrupt:
        log("Detenido por el usuario (Ctrl+C). Estado guardado.")


if __name__ == "__main__":
    main()
