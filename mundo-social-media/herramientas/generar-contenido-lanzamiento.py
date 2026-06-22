"""
NEXIA — Generador de Contenido de Lanzamiento
Genera 30 posts para Instagram + 15 para LinkedIn usando Ollama
"""
import json, urllib.request, datetime
from pathlib import Path

OLLAMA = "http://localhost:11434/api/generate"
OUT_DIR = Path(r"D:\Proyectos claude\mundo-social-media\contenido-nexia")
OUT_DIR.mkdir(parents=True, exist_ok=True)

AGENCIA = {
    "nombre": "NEXIA",
    "tagline": "Tu negocio trabajando 24/7 con IA",
    "servicios": ["chatbots IA", "apps a medida", "gestión redes sociales", "vídeo con IA", "SEO automático"],
    "precio_entrada": "497€",
    "web": "nexia.io",
    "email": "hola@nexia.io",
}


def ollama(prompt, system="", retries=3):
    for attempt in range(retries):
        try:
            req = urllib.request.Request(OLLAMA,
                data=json.dumps({"model": "qwen2.5:14b", "prompt": prompt,
                                 "system": system, "stream": False,
                                 "options": {"temperature": 0.8, "num_predict": 600}}).encode(),
                headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=300) as r:
                return json.loads(r.read())["response"]
        except Exception as e:
            print(f"  [reintento {attempt+1}/{retries}] {e}")
            if attempt == retries - 1:
                raise
    return ""


TEMAS_INSTAGRAM = [
    # Educación / valor
    "Por qué los negocios que no usan IA van a quedarse atrás en 2 años",
    "3 tareas que tu empresa puede automatizar HOY mismo sin invertir miles",
    "Qué es un chatbot de IA y cómo puede triplicar tus ventas sin contratar",
    "El error más caro que cometen las PYMES con el marketing digital",
    "Cómo una clínica redujo 40% sus llamadas con un chatbot (caso real)",
    # Servicios
    "Presentamos NEXIA: la agencia de IA que trabaja mientras tú duermes",
    "Chatbot en WhatsApp: atiende a 100 clientes a la vez sin pagar un empleado",
    "De idea a app real en 3 semanas. Así trabajamos en NEXIA",
    "Gestión de redes con IA: 30 posts al mes sin que toques el móvil",
    "Vídeos personalizados con IA para tu negocio: cómo funciona",
    # Captación
    "Consulta gratuita de 30 min: te decimos gratis qué cambiaría en tu negocio",
    "¿Cuánto cuesta un chatbot profesional? (La respuesta te va a sorprender)",
    "5 preguntas que debes hacer antes de contratar una agencia de IA",
    "Resultados reales de nuestros clientes (con números)",
    "¿Tu competencia ya usa IA? Descúbrelo y actúa antes de que sea tarde",
    # Autoridad / trust
    "Cómo elegimos las herramientas de IA para cada cliente (nuestro proceso)",
    "Por qué somos más baratos que contratar 1 empleado y damos más resultados",
    "El stack tecnológico de NEXIA: Claude, n8n, Supabase y más",
    "Nuestro proceso en 4 pasos: de consulta a sistema funcionando",
    "Garantía de satisfacción 30 días: si no funciona, lo arreglamos gratis",
]

TEMAS_LINKEDIN = [
    "Las 5 áreas de una PYME que se pueden automatizar con IA en 2026",
    "Por qué el chatbot es el mejor ROI en marketing digital actual",
    "Cómo vendemos sistemas de IA a negocios tradicionales: nuestra metodología",
    "El coste oculto de no automatizar: cuánto está perdiendo tu empresa cada mes",
    "Caso de éxito: despacho de abogados reduce 70% el tiempo en documentación",
    "IA para RRHH: cómo automatizar onboarding y reducir errores en contratación",
    "Los 3 errores que cometen las agencias de IA (y cómo los evitamos)",
    "Escalabilidad sin límite: por qué el modelo SaaS de chatbots cambia el juego",
    "Presentación de NEXIA para partners y distribuidores: modelo de colaboración",
    "El futuro de las agencias digitales: IA como infraestructura, no como herramienta",
    "Métricas que importan: cómo medimos el ROI de cada implementación de IA",
    "Automatización de ventas: cómo conseguimos leads B2B sin cold calling",
    "Por qué invertir en IA ahora es 10x más barato que esperar 2 años",
    "NEXIA busca primeros 10 clientes: oferta de lanzamiento exclusiva",
    "Colaboraciones y white-label: oportunidades para agencias y consultoras",
]


def gen_instagram(tema, idx):
    system = f"""Eres el community manager de {AGENCIA['nombre']}, una agencia de IA.
Escribes posts virales para Instagram en español (España/Latino), directos, con gancho.
Incluye emojis, es obligatorio. Tono: cercano pero profesional, con autoridad.
NUNCA uses hashtags genéricos como #marketing. Usa hashtags nicho específicos."""

    prompt = f"""Escribe un post de Instagram sobre: "{tema}"

Para la agencia {AGENCIA['nombre']} — {AGENCIA['tagline']}
Servicios: {', '.join(AGENCIA['servicios'])}
Web: {AGENCIA['web']}

Formato OBLIGATORIO:
- Primera línea: GANCHO que para el scroll (máx 10 palabras, impactante)
- Cuerpo: 3-4 párrafos con valor real (emojis al inicio de cada párrafo)
- CTA claro al final (consulta gratis, link en bio, etc.)
- 5-7 hashtags específicos al final

Máximo 300 palabras total. SOLO escribe el post, nada más."""

    return ollama(prompt, system)


def gen_linkedin(tema, idx):
    system = f"""Eres el Director de {AGENCIA['nombre']}, agencia de IA.
Escribes en LinkedIn con autoridad, datos y experiencia real.
Tono: ejecutivo pero accesible. Sin emojis en exceso (máx 3).
Formato: párrafos cortos, separados. Sin bullets largos."""

    prompt = f"""Escribe un post de LinkedIn sobre: "{tema}"

Para {AGENCIA['nombre']} dirigido a: CEOs de PYME, directores de marketing, emprendedores.
Menciona sutilmente los servicios de NEXIA cuando sea natural.

Formato:
- Primera línea: afirmación o pregunta que genere curiosidad
- 3-4 párrafos de valor / insight real
- Párrafo final: CTA suave + {AGENCIA['web']}

Entre 200-350 palabras. SOLO el post."""

    return ollama(prompt, system)


print("=" * 60)
print(f" NEXIA — Generador de Contenido de Lanzamiento")
print("=" * 60)
print(f" Generando {len(TEMAS_INSTAGRAM)} posts Instagram + {len(TEMAS_LINKEDIN)} LinkedIn")
print(f" Destino: {OUT_DIR}")
print("=" * 60)

# Generate Instagram posts
ig_posts = []
for i, tema in enumerate(TEMAS_INSTAGRAM, 1):
    print(f"\n[Instagram {i}/{len(TEMAS_INSTAGRAM)}] {tema[:50]}...")
    post = gen_instagram(tema, i)
    ig_posts.append({"tema": tema, "plataforma": "instagram", "contenido": post, "orden": i})
    print(f"  ✓ {len(post)} chars")

# Generate LinkedIn posts
li_posts = []
for i, tema in enumerate(TEMAS_LINKEDIN, 1):
    print(f"\n[LinkedIn {i}/{len(TEMAS_LINKEDIN)}] {tema[:50]}...")
    post = gen_linkedin(tema, i)
    li_posts.append({"tema": tema, "plataforma": "linkedin", "contenido": post, "orden": i})
    print(f"  ✓ {len(post)} chars")

# Save all posts
all_posts = ig_posts + li_posts
fecha = datetime.date.today().isoformat()

# JSON completo
json_path = OUT_DIR / f"posts_lanzamiento_{fecha}.json"
json_path.write_text(json.dumps(all_posts, ensure_ascii=False, indent=2), encoding="utf-8")

# Markdown readable
md_lines = ["# NEXIA — Contenido de Lanzamiento\n", f"Generado: {fecha}\n", "---\n"]
md_lines.append("## INSTAGRAM\n")
for p in ig_posts:
    md_lines.append(f"### Post {p['orden']}: {p['tema']}\n")
    md_lines.append(p['contenido'])
    md_lines.append("\n\n---\n")

md_lines.append("\n## LINKEDIN\n")
for p in li_posts:
    md_lines.append(f"### Post {p['orden']}: {p['tema']}\n")
    md_lines.append(p['contenido'])
    md_lines.append("\n\n---\n")

md_path = OUT_DIR / f"posts_lanzamiento_{fecha}.md"
md_path.write_text("".join(md_lines), encoding="utf-8")

print(f"\n{'='*60}")
print(f"[OK] {len(all_posts)} posts guardados:")
print(f"  JSON: {json_path}")
print(f"  MD:   {md_path}")
print(f"{'='*60}")
