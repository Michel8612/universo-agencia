#!/usr/bin/env python3
"""
NEXIA — Diagnostico Web real (gratis, sin API keys obligatorias)

Audita la web de un negocio, detecta problemas concretos y los mapea a
servicios del catalogo con precio. Genera un pitch personalizado con Ollama.

Uso:
  python diagnostico-web.py --url https://restaurante.com
  python diagnostico-web.py --url restaurante.com --pitch --negocio "Restaurante X"
  python diagnostico-web.py --csv ../leads-scrapeados/restaurantes-Valencia-XXXX.csv --pitch
"""
import urllib.request, urllib.parse, json, ssl, socket, time, re, os, argparse, csv

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 NEXIA-Diag/1.0"
OLLAMA = "http://localhost:11434/api/generate"
CAT_PATH = os.path.join(os.path.dirname(__file__), "..", "catalogo-servicios.json")

def cargar_catalogo():
    with open(CAT_PATH, encoding="utf-8") as f:
        return json.load(f)["servicios"]

def norm_url(u):
    u = u.strip()
    if not u.startswith("http"):
        u = "https://" + u
    return u

def fetch(url, timeout=15):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    t0 = time.time()
    r = urllib.request.urlopen(req, timeout=timeout)
    body = r.read()
    return r, body, time.time() - t0

def check_ssl(dominio):
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((dominio, 443), timeout=8) as s:
            with ctx.wrap_socket(s, server_hostname=dominio) as ss:
                ss.getpeercert()
        return True
    except Exception:
        return False

def diagnosticar(url):
    """Devuelve dict con hallazgos (claves = triggers del catalogo)."""
    url = norm_url(url)
    dom = urllib.parse.urlparse(url).netloc.replace("www.", "")
    h = {"url": url, "dominio": dom, "accesible": False, "hallazgos": [], "señales": set()}

    # SSL
    tiene_ssl = check_ssl(dom)
    if not tiene_ssl:
        h["señales"].add("sin_ssl")
        h["hallazgos"].append("La web no tiene certificado SSL valido (https inseguro)")

    # Cargar HTML + medir velocidad
    try:
        r, body, dur = fetch(url if tiene_ssl else "http://" + dom)
        html = body.decode("utf-8", "ignore")
        low = html.lower()
        h["accesible"] = True
        peso_kb = len(body) / 1024
        h["tiempo_carga"] = round(dur, 2)
        h["peso_kb"] = round(peso_kb)
    except Exception as e:
        h["hallazgos"].append(f"La web no carga correctamente ({type(e).__name__})")
        h["señales"].add("sin_web")
        return h

    # Velocidad (heuristica local: tiempo de carga del HTML + peso)
    if h["tiempo_carga"] > 3.5 or h["peso_kb"] > 3000:
        h["señales"].add("web_lenta")
        h["hallazgos"].append(f"Web lenta: carga en {h['tiempo_carga']}s, pesa {h['peso_kb']}KB")

    # Responsive
    if "viewport" not in low:
        h["señales"].add("no_responsive")
        h["hallazgos"].append("No es responsive: se ve mal en moviles (sin meta viewport)")

    # Formulario de contacto
    if "<form" not in low and "mailto:" not in low:
        h["señales"].add("sin_formulario")
        h["hallazgos"].append("No tiene formulario de contacto: pierde clientes potenciales")

    # Analytics
    if not any(x in low for x in ["gtag", "google-analytics", "googletagmanager", "analytics.js", "gtm.js"]):
        h["señales"].add("sin_analytics")
        h["hallazgos"].append("Sin Google Analytics: no sabe de donde vienen sus visitas")

    # WordPress
    if "wp-content" in low or "wp-includes" in low:
        h["señales"].add("wordpress")
        ver = re.search(r'content="WordPress (\d+\.\d+)', html)
        v = f" (v{ver.group(1)})" if ver else ""
        h["hallazgos"].append(f"Hecha en WordPress{v}: requiere mantenimiento y seguridad")

    # Shopify (deteccion estricta para evitar falsos positivos)
    if "cdn.shopify" in low or "myshopify" in low or "shopify.com" in low:
        h["señales"].add("shopify")

    # Chatbot (upsell casi siempre)
    if not any(x in low for x in ["chatbot", "intercom", "tawk", "crisp", "whatsapp", "wa.me", "livechat", "zendesk"]):
        h["señales"].add("sin_chatbot")
        h["hallazgos"].append("Sin chat/chatbot: no atiende clientes 24/7")

    # SEO basico
    sin_title = "<title" not in low
    sin_desc = 'name="description"' not in low
    if sin_title:
        h["hallazgos"].append("Sin etiqueta title (malo para SEO)")
    if sin_desc:
        h["hallazgos"].append("Sin meta description (malo para SEO)")
    if sin_title or sin_desc:
        h["señales"].add("sin_seo")

    # Redes sociales enlazadas
    if not any(x in low for x in ["instagram.com", "facebook.com", "tiktok.com",
                                   "linkedin.com", "twitter.com", "x.com/"]):
        h["señales"].add("sin_redes")
        h["hallazgos"].append("Sin enlaces a redes sociales: poca presencia en RRSS")

    # Newsletter / captacion de emails
    if not any(x in low for x in ["newsletter", "mailchimp", "suscrib", "subscribe"]):
        h["señales"].add("sin_newsletter")

    return h

def recomendar_servicios(señales, catalogo):
    """Mapea señales del diagnostico a servicios del catalogo."""
    recs = []
    for s in catalogo:
        trig = s.get("trigger")
        if trig and trig in señales:
            recs.append(s)
    # ordenar por valor medio descendente
    recs.sort(key=lambda x: (x["min"] + x["max"]) / 2, reverse=True)
    return recs

def fmt_precio(s):
    suf = {"fijo": "", "mes": "/mes", "hr": "/hr"}[s["tipo"]]
    return f"${s['min']}-{s['max']}{suf}"

def generar_pitch(negocio, hallazgos, recs):
    problemas = "; ".join(hallazgos[:5]) or "mejoras de presencia digital"
    servicios = ", ".join(f"{s['nombre']} ({fmt_precio(s)})" for s in recs[:4])
    prompt = f"""Eres comercial de NEXIA (agencia de IA y desarrollo web). Escribe un email corto (max 120 palabras), profesional y cercano en espanol, para el negocio "{negocio}".
Detectamos estos problemas reales en su web: {problemas}.
Ofrecemos: {servicios}.
El email debe: 1) mencionar 1-2 problemas concretos sin sonar agresivo, 2) explicar el beneficio de arreglarlo, 3) invitar a una llamada gratuita. NO inventes datos. Firma como "Equipo NEXIA"."""
    body = json.dumps({"model": "qwen2.5:14b", "prompt": prompt, "stream": False}).encode()
    try:
        req = urllib.request.Request(OLLAMA, data=body, headers={"Content-Type": "application/json"})
        return json.loads(urllib.request.urlopen(req, timeout=120).read())["response"].strip()
    except Exception as e:
        return f"(No se pudo generar pitch: {e})"

def informe(h, catalogo, con_pitch=False, negocio=None):
    print(f"\n{'='*55}")
    print(f"DIAGNOSTICO: {h.get('dominio', h['url'])}")
    print('='*55)
    if not h["accesible"] and "sin_web" in h["señales"]:
        print("  [X] La web no carga / no existe -> oportunidad: Landing o Website nuevo")
    if h.get("tiempo_carga"):
        print(f"  Carga: {h['tiempo_carga']}s | Peso: {h.get('peso_kb','?')}KB")
    print(f"\n  PROBLEMAS DETECTADOS ({len(h['hallazgos'])}):")
    for x in h["hallazgos"]:
        print(f"    - {x}")
    recs = recomendar_servicios(h["señales"], catalogo)
    if recs:
        tot_min = sum(s["min"] for s in recs)
        tot_max = sum(s["max"] for s in recs)
        print(f"\n  SERVICIOS RECOMENDADOS ({len(recs)}) -> valor: ${tot_min}-{tot_max}:")
        for s in recs:
            print(f"    [{s['id']:>2}] {s['nombre']:42} {fmt_precio(s)}")
    else:
        print("\n  Sin servicios auto-recomendados (web en buen estado).")
    if con_pitch and (recs or h["hallazgos"]):
        print(f"\n  --- PITCH GENERADO (Ollama) ---")
        print("  " + generar_pitch(negocio or h["dominio"], h["hallazgos"], recs).replace("\n", "\n  "))
    return recs

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url")
    ap.add_argument("--negocio", default=None)
    ap.add_argument("--csv", help="diagnosticar todos los leads con web de un CSV del scraper")
    ap.add_argument("--pitch", action="store_true", help="genera email personalizado con Ollama")
    ap.add_argument("--limite", type=int, default=20)
    args = ap.parse_args()

    catalogo = cargar_catalogo()

    if args.csv:
        with open(args.csv, encoding="utf-8-sig") as f:
            rows = [r for r in csv.DictReader(f) if r.get("web")]
        print(f"Diagnosticando {min(len(rows), args.limite)} webs del CSV...")
        for row in rows[:args.limite]:
            h = diagnosticar(row["web"])
            informe(h, catalogo, con_pitch=args.pitch, negocio=row.get("nombre"))
            time.sleep(0.5)
        return

    if not args.url:
        print("Falta --url o --csv. Ej: --url restaurante.com --pitch")
        return

    h = diagnosticar(args.url)
    informe(h, catalogo, con_pitch=args.pitch, negocio=args.negocio)

if __name__ == "__main__":
    main()
