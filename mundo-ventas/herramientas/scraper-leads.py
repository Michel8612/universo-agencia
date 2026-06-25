#!/usr/bin/env python3
"""
NEXIA — Scraper de Leads por nicho/sub-nicho (100% gratis, sin API keys)

Fuente: OpenStreetMap (Nominatim + Overpass) — legal, gratuito, sin bloqueos.
Enriquece email visitando la web del negocio. Clasifica con Ollama local.
Guarda en el CRM (Flask) y exporta CSV.

Uso:
  python scraper-leads.py --nicho restaurantes --ciudad "Valencia, Espana"
  python scraper-leads.py --nicho dentistas --ciudad "Madrid" --enriquecer --crm
  python scraper-leads.py --listar-nichos
"""
import urllib.request, urllib.parse, json, time, re, csv, argparse, sys, os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from llm import generar as llm_generar
from notificar import aviso_lead

UA = "NEXIA-LeadScraper/1.0 (contacto: teamorionglobal@gmail.com)"
CRM_URL = "http://127.0.0.1:8080/crm/cliente"
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "leads-scrapeados")

# nicho -> filtros OSM. Sub-nichos via cuisine/extra tags.
NICHOS = {
    # --- Hosteleria y comida ---
    "restaurantes":  ['nwr["amenity"="restaurant"]'],
    "cafeterias":    ['nwr["amenity"="cafe"]'],
    "bares":         ['nwr["amenity"="bar"]', 'nwr["amenity"="pub"]'],
    "comida-rapida": ['nwr["amenity"="fast_food"]'],
    "heladerias":    ['nwr["amenity"="ice_cream"]'],
    "panaderias":    ['nwr["shop"="bakery"]'],
    "pastelerias":   ['nwr["shop"="pastry"]', 'nwr["shop"="confectionery"]'],
    "hoteles":       ['nwr["tourism"="hotel"]', 'nwr["tourism"="guest_house"]'],
    "apartamentos":  ['nwr["tourism"="apartment"]'],
    # --- Belleza y bienestar ---
    "peluquerias":   ['nwr["shop"="hairdresser"]'],
    "belleza":       ['nwr["shop"="beauty"]'],
    "unas":          ['nwr["shop"="beauty"]["beauty"="nails"]'],
    "spa":           ['nwr["leisure"="spa"]', 'nwr["shop"="massage"]'],
    "tatuajes":      ['nwr["shop"="tattoo"]'],
    "gimnasios":     ['nwr["leisure"="fitness_centre"]'],
    "yoga":          ['nwr["leisure"="fitness_centre"]["fitness_centre"="yoga"]', 'nwr["sport"="yoga"]'],
    # --- Salud ---
    "dentistas":     ['nwr["amenity"="dentist"]', 'nwr["healthcare"="dentist"]'],
    "clinicas":      ['nwr["amenity"="clinic"]', 'nwr["healthcare"="clinic"]'],
    "fisioterapia":  ['nwr["healthcare"="physiotherapist"]'],
    "psicologos":    ['nwr["healthcare"="psychotherapist"]', 'nwr["healthcare:speciality"="psychiatry"]'],
    "nutricionistas":['nwr["healthcare"="nutrition_counselling"]'],
    "podologos":     ['nwr["healthcare"="podiatrist"]'],
    "opticas":       ['nwr["shop"="optician"]'],
    "farmacias":     ['nwr["amenity"="pharmacy"]'],
    "veterinarios":  ['nwr["amenity"="veterinary"]'],
    # --- Profesionales / oficinas ---
    "abogados":      ['nwr["office"="lawyer"]'],
    "inmobiliarias": ['nwr["office"="estate_agent"]'],
    "asesorias":     ['nwr["office"="accountant"]', 'nwr["office"="tax_advisor"]'],
    "seguros":       ['nwr["office"="insurance"]'],
    "arquitectos":   ['nwr["office"="architect"]'],
    # --- Oficios (baja competencia digital, alta necesidad) ---
    "fontaneros":    ['nwr["craft"="plumber"]'],
    "electricistas": ['nwr["craft"="electrician"]'],
    "cerrajeros":    ['nwr["craft"="locksmith"]', 'nwr["shop"="locksmith"]'],
    "carpinteros":   ['nwr["craft"="carpenter"]'],
    "pintores":      ['nwr["craft"="painter"]'],
    "reformas":      ['nwr["craft"="builder"]'],
    "jardineria":    ['nwr["craft"="gardener"]', 'nwr["shop"="garden_centre"]'],
    "fotografos":    ['nwr["craft"="photographer"]', 'nwr["shop"="photo"]'],
    # --- Comercio ---
    "talleres":      ['nwr["shop"="car_repair"]'],
    "concesionarios":['nwr["shop"="car"]'],
    "ferreterias":   ['nwr["shop"="hardware"]', 'nwr["shop"="doityourself"]'],
    "tiendas-ropa":  ['nwr["shop"="clothes"]'],
    "joyerias":      ['nwr["shop"="jewelry"]'],
    "floristerias":  ['nwr["shop"="florist"]'],
    "mascotas":      ['nwr["shop"="pet"]'],
    "muebles":       ['nwr["shop"="furniture"]'],
    # --- Formacion ---
    "academias":     ['nwr["amenity"="school"]', 'nwr["office"="educational_institution"]'],
    "autoescuelas":  ['nwr["amenity"="driving_school"]'],
    "idiomas":       ['nwr["amenity"="language_school"]'],
}

# sub-nichos de restaurante (tag cuisine de OSM)
SUBNICHOS_CUISINE = {
    "vegano":"vegan", "vegetariano":"vegetarian", "italiano":"italian",
    "japones":"japanese", "chino":"chinese", "mexicano":"mexican",
    "indio":"indian", "pizza":"pizza", "hamburguesas":"burger",
    "marisco":"seafood", "tapas":"tapas", "asiatico":"asian",
}

def http_get(url, timeout=40):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=timeout).read().decode("utf-8", "ignore")

def geocodificar(ciudad, pais="Spain"):
    """Devuelve (osm_type, osm_id, display_name) de la ciudad.
    Usa busqueda ESTRUCTURADA (city+country) -> devuelve el limite municipal (relation)."""
    q = urllib.parse.urlencode({"city": ciudad, "country": pais, "format": "json", "limit": 5})
    res = json.loads(http_get(f"https://nominatim.openstreetmap.org/search?{q}"))
    if not res:
        # fallback a busqueda libre
        q = urllib.parse.urlencode({"q": f"{ciudad}, {pais}", "format": "json", "limit": 10})
        res = json.loads(http_get(f"https://nominatim.openstreetmap.org/search?{q}"))
    if not res:
        return None
    for tipo in ("relation", "way", "node"):
        for r in res:
            if r.get("osm_type") == tipo:
                return r["osm_type"], int(r["osm_id"]), r["display_name"]
    r = res[0]
    return r["osm_type"], int(r["osm_id"]), r["display_name"]

def overpass_area_id(osm_type, osm_id):
    """Convierte osm relation/way en area id de Overpass."""
    if osm_type == "relation":
        return 3600000000 + osm_id
    if osm_type == "way":
        return 2400000000 + osm_id
    return None  # node: no es area, usaremos around

def buscar_negocios(nicho, ciudad, subnicho=None, limite=200, pais="Spain"):
    geo = geocodificar(ciudad, pais)
    if not geo:
        print(f"  [!] No se pudo geocodificar '{ciudad}'"); return [], ciudad
    osm_type, osm_id, display = geo
    print(f"  Zona: {display}")
    time.sleep(1.2)  # rate limit Nominatim

    area_id = overpass_area_id(osm_type, osm_id)
    filtros = NICHOS.get(nicho)
    if not filtros:
        print(f"  [!] Nicho '{nicho}' no reconocido. Usa --listar-nichos"); return [], display

    # filtro de sub-nicho (cuisine) para restaurantes
    cuisine = SUBNICHOS_CUISINE.get(subnicho) if subnicho else None
    cuisine_filter = f'["cuisine"~"{cuisine}"]' if cuisine else ""

    partes = []
    for f in filtros:
        if cuisine_filter:
            f = f[:-1] if f.endswith("]") else f  # no aplica; ya esta cerrado
        partes.append(f"{f}{cuisine_filter}(area.searchArea);")
    cuerpo = "\n".join(partes)

    if area_id:
        query = f"""[out:json][timeout:60];
area(id:{area_id})->.searchArea;
({cuerpo});
out center {limite};"""
    else:
        # fallback: alrededor de un punto (nodes/ciudades pequenas)
        query = f"""[out:json][timeout:60];
({cuerpo.replace('(area.searchArea)', '(around:8000,'+str(osm_id)+')')});
out center {limite};"""

    url = "https://overpass-api.de/api/interpreter?data=" + urllib.parse.quote(query)
    data = json.loads(http_get(url, timeout=90))
    return data.get("elements", []), display

EMAIL_RE = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
# dominios de tracking/ruido que NO son emails de contacto reales
DOMINIOS_RUIDO = ("wixpress.com", "sentry.io", "sentry-next", "wix.com",
                  "example.com", "domain.com", "godaddy", "@2x", "wordpress.com",
                  ".png", ".jpg", "schema.org", "w3.org")

def email_valido(e):
    el = e.lower()
    if any(d in el for d in DOMINIOS_RUIDO):
        return False
    if el.startswith(("example@", "email@", "tu@", "your@", "nombre@", "usuario@")):
        return False
    return True

def enriquecer_email(web):
    """Visita la web y busca un email. Devuelve '' si no encuentra."""
    if not web:
        return ""
    if not web.startswith("http"):
        web = "https://" + web
    for path in ["", "/contacto", "/contact", "/aviso-legal", "/about"]:
        try:
            html = http_get(web.rstrip("/") + path, timeout=12)
            # mailto primero
            m = re.search(r'mailto:([^"\'>\s?]+)', html)
            if m and "@" in m.group(1) and email_valido(m.group(1)):
                return m.group(1).strip()
            emails = EMAIL_RE.findall(html)
            # filtrar imagenes/ejemplos/tracking
            emails = [e for e in emails if not re.search(r'\.(png|jpg|jpeg|gif|webp|svg)$', e, re.I)
                      and email_valido(e)]
            if emails:
                # preferir el del propio dominio
                dom = urllib.parse.urlparse(web).netloc.replace("www.", "")
                propios = [e for e in emails if dom.split(".")[0] in e]
                return (propios or emails)[0].strip()
        except Exception:
            continue
    return ""

def clasificar_lead(negocio):
    """Puntua el lead (1-10) y sugiere servicio NEXIA. Usa Groq o Ollama (ver llm.py)."""
    prompt = f"""Eres analista comercial de NEXIA (agencia de IA). Evalua este negocio como lead potencial.
Negocio: {negocio['nombre']} | Tipo: {negocio['categoria']} | Web: {negocio['web'] or 'SIN WEB'} | Tel: {negocio['telefono'] or 'no'}
Devuelve SOLO JSON: {{"puntuacion": 1-10, "servicio": "...", "motivo": "una frase"}}
Criterio: sin web = oportunidad alta para Landing+Chatbot. Con web antigua = automatizacion. Puntua mayor si falta presencia digital."""
    try:
        resp = llm_generar(prompt, temperature=0.3)
        m = re.search(r'\{[\s\S]*\}', resp)
        if m:
            j = json.loads(m.group(0))
            return j.get("puntuacion", 5), j.get("servicio", "Consultoria IA"), j.get("motivo", "")
    except Exception:
        pass
    return 5, "Consultoria IA", "sin analisis"

def guardar_crm(negocio):
    payload = json.dumps({
        "nombre": negocio["nombre"],
        "contacto": negocio["email"] or negocio["telefono"] or "",
        "mundo": "mundo-ventas",
        "estado": "lead_scrapeado",
        "presupuesto": 0,
        "notas": f"{negocio['categoria']} | {negocio['direccion']} | tel:{negocio['telefono']} | web:{negocio['web']} | score:{negocio.get('puntuacion','')} | {negocio.get('servicio','')}",
    }).encode()
    try:
        req = urllib.request.Request(CRM_URL, data=payload, headers={"Content-Type": "application/json"})
        urllib.request.urlopen(req, timeout=8)
        # Aviso interno a Slack (best-effort; solo si SLACK_WEBHOOK_URL esta configurado)
        aviso_lead(
            negocio["nombre"],
            score=negocio.get("puntuacion"),
            servicio=negocio.get("servicio", ""),
            extra=f"{negocio['categoria']} · {negocio['direccion']} · web:{negocio['web'] or 'NO'}",
        )
        return True
    except Exception:
        return False

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nicho")
    ap.add_argument("--subnicho", default=None, help="ej: vegano, italiano, japones")
    ap.add_argument("--ciudad", default="")
    ap.add_argument("--pais", default="Spain")
    ap.add_argument("--limite", type=int, default=200)
    ap.add_argument("--enriquecer", action="store_true", help="visita webs para sacar email (mas lento)")
    ap.add_argument("--clasificar", action="store_true", help="puntua cada lead con Ollama (lento)")
    ap.add_argument("--crm", action="store_true", help="guarda los leads en el CRM")
    ap.add_argument("--solo-con-web", action="store_true", help="filtra solo negocios con web")
    ap.add_argument("--listar-nichos", action="store_true")
    args = ap.parse_args()

    if args.listar_nichos:
        print("Nichos disponibles:")
        for n in sorted(NICHOS): print(f"  - {n}")
        print("\nSub-nichos (restaurantes):", ", ".join(sorted(SUBNICHOS_CUISINE)))
        return

    if not args.nicho or not args.ciudad:
        print("Faltan --nicho y --ciudad. Ej: --nicho restaurantes --ciudad \"Valencia, Espana\"")
        return

    print(f"\n=== Buscando '{args.nicho}'{' ('+args.subnicho+')' if args.subnicho else ''} en '{args.ciudad}' ===")
    elementos, zona = buscar_negocios(args.nicho, args.ciudad, args.subnicho, args.limite, args.pais)
    print(f"  Negocios encontrados en OSM: {len(elementos)}")

    leads = []
    for e in elementos:
        t = e.get("tags", {})
        nombre = t.get("name")
        if not nombre:
            continue
        web = t.get("website") or t.get("contact:website") or ""
        if args.solo_con_web and not web:
            continue
        direccion = " ".join(filter(None, [
            t.get("addr:street",""), t.get("addr:housenumber",""), t.get("addr:city","")
        ])).strip()
        leads.append({
            "nombre": nombre,
            "categoria": args.nicho + (f"/{args.subnicho}" if args.subnicho else ""),
            "telefono": t.get("phone") or t.get("contact:phone") or "",
            "web": web,
            "email": t.get("email") or t.get("contact:email") or "",
            "direccion": direccion,
        })

    print(f"  Leads validos (con nombre): {len(leads)}")

    # Enriquecimiento de email
    if args.enriquecer:
        print("  Enriqueciendo emails (visitando webs)...")
        for i, l in enumerate(leads):
            if not l["email"] and l["web"]:
                l["email"] = enriquecer_email(l["web"])
                if l["email"]:
                    print(f"    [{i+1}/{len(leads)}] {l['nombre'][:25]} -> {l['email']}")
                time.sleep(0.3)
        con_email = sum(1 for l in leads if l["email"])
        print(f"  Con email: {con_email}/{len(leads)}")

    # Clasificacion IA
    if args.clasificar:
        print("  Clasificando con Ollama (puede tardar)...")
        for i, l in enumerate(leads):
            p, s, m = clasificar_lead(l)
            l["puntuacion"], l["servicio"], l["motivo"] = p, s, m
            print(f"    [{i+1}/{len(leads)}] {l['nombre'][:25]} -> {p}/10 ({s})")
        leads.sort(key=lambda x: x.get("puntuacion", 0), reverse=True)

    # Guardar CSV
    os.makedirs(OUT_DIR, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M")
    fname = os.path.join(OUT_DIR, f"{args.nicho}-{args.ciudad.split(',')[0].strip().replace(' ','_')}-{stamp}.csv")
    campos = ["nombre","categoria","telefono","email","web","direccion","puntuacion","servicio","motivo"]
    with open(fname, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=campos, extrasaction="ignore")
        w.writeheader()
        for l in leads: w.writerow(l)
    print(f"\n  CSV guardado: {fname}")

    # Guardar en CRM
    if args.crm:
        ok = sum(1 for l in leads if guardar_crm(l))
        print(f"  Guardados en CRM: {ok}/{len(leads)}")

    print(f"\n=== {len(leads)} leads listos ===")

if __name__ == "__main__":
    main()
