#!/usr/bin/env python3
"""
NEXIA — Buscador de trabajos freelance + redactor de propuestas (gratis)

Fuente: API pública de Freelancer.com (proyectos activos, sin login).
Filtra por skills de NEXIA, presupuesto y competencia. Para cada trabajo
genera una propuesta personalizada con Ollama. TÚ revisas y envías manual
(nunca auto-aplicar: viola los términos y banea la cuenta).

Uso:
  python buscar-trabajos.py                         # busca en todas las skills NEXIA
  python buscar-trabajos.py --query chatbot --propuestas
  python buscar-trabajos.py --min-budget 200 --max-competencia 30 --propuestas
"""
import urllib.request, urllib.parse, json, time, re, csv, argparse, os, sys
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import llm

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) NEXIA-JobFinder/1.0"
OLLAMA = "http://localhost:11434/api/generate"
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "trabajos-encontrados")
FL_API = "https://www.freelancer.com/api/projects/0.1/projects/active/"
FL_PROJECT = "https://www.freelancer.com/projects/"

# Skills de NEXIA -> términos de búsqueda en Freelancer.com
SKILLS_NEXIA = [
    "website", "landing page", "wordpress", "shopify", "chatbot",
    "automation", "web scraping", "api integration", "next.js",
    "react", "python script", "ai assistant", "n8n", "make automation",
]

# Conversión aproximada a USD para filtrar presupuestos comparables
USD = {"USD":1, "EUR":1.08, "GBP":1.27, "AUD":0.66, "CAD":0.73, "NZD":0.61,
       "INR":0.012, "PKR":0.0036, "PHP":0.017, "BRL":0.18, "MXN":0.05,
       "ZAR":0.055, "AED":0.27, "SGD":0.74}

# Relevancia: el trabajo debe tocar algún dominio de NEXIA...
INCLUIR = ["web", "site", "página", "pagina", "landing", "wordpress", "shopify",
    "woocommerce", "chatbot", "bot", " ai", "a.i", "automat", "scrap", "api",
    "python", "react", "next.js", "nextjs", "node", "javascript", "php", "laravel",
    "seo", "ecommerce", "e-commerce", "app", "dashboard", "integration", "integración",
    "n8n", "zapier", "make.com", "database", "backend", "frontend", "logo", "brand",
    "video", "reel", "copywrit", "content", "email marketing", "social media", "crm"]
# ...y NO ser de estas categorías que no entregamos
EXCLUIR = ["telecall", "cold call", "commission", "sales rep", "lead generator",
    "resume", "cv writ", "data entry", "voice over", "voiceover", "tee design",
    "t-shirt", "accountant", "legal writ", "translat", "transcription"]

def get(url, timeout=25, intentos=3):
    last = None
    for n in range(intentos):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
            return urllib.request.urlopen(req, timeout=timeout).read().decode("utf-8", "ignore")
        except Exception as e:
            last = e
            time.sleep(1.5 * (n + 1))
    raise last

# Detección de idioma por palabras comunes (sin dependencias)
IDIOMAS = {
    "español": [" el ", " la ", " de ", " que ", " para ", " con ", " una ", " los ", " por ", "ñ", "ción ", " necesito ", " busco ", " página ", " desarrollador "],
    "inglés": [" the ", " and ", " for ", " with ", " you ", " our ", " need ", " looking ", " website ", " want ", " will ", " developer "],
    "portugués": [" não ", " você ", " uma ", " precisa ", " preciso ", " obrigado ", "ção ", " estou ", " olá ", " desenvolvedor "],
    "francés": [" je ", " vous ", " nous ", " votre ", " une ", " pour ", " avec ", " besoin ", " bonjour ", " merci ", " être ", " développeur ", " création ", " site web "],
    "italiano": [" il ", " di ", " che ", " per ", " sono ", " sito ", " grazie ", " abbiamo ", " sviluppatore ", " ciao "],
}
def detectar_idioma(texto):
    t = " " + texto.lower() + " "
    mejor, score = "inglés", 0
    for idioma, marcas in IDIOMAS.items():
        s = sum(t.count(m) for m in marcas)
        if s > score:
            mejor, score = idioma, s
    return mejor

def es_relevante(t):
    texto = (t["titulo"] + " " + t["descripcion"] + " " + " ".join(t["skills"])).lower()
    if any(x in texto for x in EXCLUIR):
        return False
    return any(x in texto for x in INCLUIR)

def buscar(query, limite=20):
    params = urllib.parse.urlencode({
        "query": query, "limit": limite, "full_description": "true",
        "job_details": "true", "sort_field": "time_updated",
    })
    try:
        d = json.loads(get(f"{FL_API}?{params}"))
        return d.get("result", {}).get("projects", [])
    except Exception as e:
        print(f"  [!] error buscando '{query}': {e}")
        return []

def normalizar(p):
    b = p.get("budget", {}) or {}
    bs = p.get("bid_stats", {}) or {}
    moneda = (p.get("currency") or {}).get("code", "USD")
    minimo = b.get("minimum") or 0
    return {
        "id": p.get("id"),
        "titulo": p.get("title", ""),
        "descripcion": (p.get("preview_description") or p.get("description") or "")[:600],
        "min": minimo,
        "max": b.get("maximum") or 0,
        "usd_min": round(minimo * USD.get(moneda, 0.5)),
        "moneda": moneda,
        "tipo": p.get("type", ""),
        "pujas": bs.get("bid_count") or 0,
        "skills": [j.get("name") for j in (p.get("jobs") or [])][:6],
        "url": FL_PROJECT + p.get("seo_url", ""),
    }

def generar_propuesta(t):
    idioma = detectar_idioma(t["titulo"] + " " + t["descripcion"])
    prompt = f"""You are a professional freelancer from NEXIA (web development, chatbots, AI and automation). Write a WINNING, SHORT proposal (max 90 words) for this Freelancer.com project.

Project: {t['titulo']}
Description: {t['descripcion']}
Skills: {', '.join(t['skills'])}

CRITICAL LANGUAGE RULE: The ENTIRE proposal MUST be written ONLY in {idioma}. Every single word in {idioma}. Do NOT mix languages. Do NOT use any other language.

Other rules:
- Start by referring to something concrete about THEIR project (not "Dear Sir").
- 2-3 sentences: show you understand their need + how you would solve it.
- End with ONE concrete question to start a conversation.
- Professional, warm tone. No false promises, no filler. Do not invent specific past experience.
- Return ONLY the proposal text, no headers, no "Proposal:" label.
- REMEMBER: write everything in {idioma}."""
    return llm.generar(prompt, max_tokens=350)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--query", help="término concreto (si no, usa todas las skills NEXIA)")
    ap.add_argument("--min-budget", type=int, default=100, help="presupuesto mínimo (filtra proyectos pequeños)")
    ap.add_argument("--max-competencia", type=int, default=60, help="máx nº de pujas (menos = más opciones)")
    ap.add_argument("--limite", type=int, default=15, help="proyectos por término de búsqueda")
    ap.add_argument("--propuestas", action="store_true", help="genera propuesta con Ollama para cada trabajo (lento)")
    ap.add_argument("--top", type=int, default=15, help="máximo de trabajos a procesar")
    args = ap.parse_args()

    queries = [args.query] if args.query else SKILLS_NEXIA
    print(f"=== Buscando trabajos en Freelancer.com ({len(queries)} términos) ===")

    vistos, trabajos = set(), []
    for q in queries:
        for p in buscar(q, args.limite):
            t = normalizar(p)
            if t["id"] in vistos:
                continue
            if t["usd_min"] < args.min_budget:
                continue
            if t["pujas"] > args.max_competencia:
                continue
            if not es_relevante(t):
                continue
            vistos.add(t["id"])
            trabajos.append(t)
        time.sleep(0.4)

    # ordenar: menos competencia primero, luego mayor presupuesto (en USD)
    trabajos.sort(key=lambda x: (x["pujas"], -x["usd_min"]))
    trabajos = trabajos[:args.top]
    print(f"  {len(trabajos)} trabajos relevantes (min ${args.min_budget} USD, max {args.max_competencia} pujas)\n")

    if args.propuestas:
        print("  Generando propuestas con Ollama (puede tardar)...")
        for i, t in enumerate(trabajos):
            t["propuesta"] = generar_propuesta(t)
            print(f"    [{i+1}/{len(trabajos)}] {t['titulo'][:45]}")

    os.makedirs(OUT_DIR, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M")

    # CSV
    csv_path = os.path.join(OUT_DIR, f"trabajos-{stamp}.csv")
    with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["titulo", "presupuesto", "moneda", "pujas", "skills", "url", "propuesta"])
        for t in trabajos:
            w.writerow([t["titulo"], f"{t['min']}-{t['max']}", t["moneda"], t["pujas"],
                        ", ".join(t["skills"]), t["url"], t.get("propuesta", "")])

    # Markdown legible para revisar y copiar
    md_path = os.path.join(OUT_DIR, f"trabajos-{stamp}.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"# Trabajos encontrados — {stamp}\n\n{len(trabajos)} oportunidades. Revisa, ajusta la propuesta y aplica TÚ manualmente.\n\n")
        for t in trabajos:
            f.write(f"## {t['titulo']}\n")
            f.write(f"- 💰 **{t['min']}-{t['max']} {t['moneda']}** | 🧑‍💻 {t['pujas']} pujas | {t['tipo']}\n")
            f.write(f"- Skills: {', '.join(t['skills'])}\n")
            f.write(f"- 🔗 {t['url']}\n")
            if t.get("propuesta"):
                f.write(f"\n**Propuesta sugerida:**\n\n> {t['propuesta'].replace(chr(10), chr(10)+'> ')}\n")
            f.write("\n---\n\n")

    print(f"\n  CSV: {csv_path}")
    print(f"  Markdown (para revisar): {md_path}")
    # Resumen en consola
    print(f"\n=== TOP {min(8, len(trabajos))} oportunidades ===")
    for t in trabajos[:8]:
        print(f"  ~${t['usd_min']}+ USD ({t['min']}-{t['max']} {t['moneda']}) | {t['pujas']} pujas | {t['titulo'][:48]}")

if __name__ == "__main__":
    main()
