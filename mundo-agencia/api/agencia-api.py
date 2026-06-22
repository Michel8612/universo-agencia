"""
UNIVERSO AGENCIA — API Central
Puerto 8080 | Conecta n8n con todos los mundos
"""

import os, json, subprocess, datetime, sqlite3
from pathlib import Path
from flask import Flask, request, jsonify
import urllib.request

BASE = Path(r"D:\Proyectos claude")
OLLAMA = "http://localhost:11434/api/generate"
FFMPEG = r"C:\ffmpeg\ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe"
DB_PATH = BASE / "mundo-agencia" / "crm" / "agencia.db"

app = Flask(__name__)

# ─── Base de datos CRM ligera ─────────────────────────────────
def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT, contacto TEXT, mundo TEXT,
            estado TEXT DEFAULT 'prospecto',
            presupuesto REAL, notas TEXT,
            fecha TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mundo TEXT, herramienta TEXT, params TEXT,
            estado TEXT DEFAULT 'pendiente',
            resultado TEXT, fecha TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def log_tarea(mundo, herramienta, params, estado, resultado=""):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO tareas (mundo, herramienta, params, estado, resultado) VALUES (?,?,?,?,?)",
        (mundo, herramienta, json.dumps(params), estado, str(resultado)[:500])
    )
    conn.commit()
    conn.close()

# ─── Ollama helper ────────────────────────────────────────────
def ollama_ask(prompt, model="qwen2.5:14b", system="Eres un asistente profesional."):
    payload = json.dumps({
        "model": model,
        "prompt": prompt,
        "system": system,
        "stream": False,
        "options": {"temperature": 0.7, "num_predict": 800}
    }).encode()
    req = urllib.request.Request(OLLAMA, data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())["response"]

# ═══════════════════════════════════════════════════════════════
# ENDPOINTS
# ═══════════════════════════════════════════════════════════════

@app.route("/echo", methods=["POST", "GET"])
def echo():
    """Debug: muestra exactamente lo que recibe"""
    return jsonify({
        "method": request.method,
        "content_type": request.content_type,
        "body_raw": request.get_data(as_text=True)[:500],
        "json": request.json,
        "ok": True
    })

@app.route("/", methods=["GET"])
def health():
    return jsonify({
        "estado": "online",
        "agencia": "NEXIA",
        "hora": datetime.datetime.now().isoformat(),
        "mundos": [d.name for d in BASE.iterdir() if d.is_dir() and d.name.startswith("mundo-")]
    })

@app.route("/estado", methods=["GET"])
def estado():
    """Resumen rápido de la agencia"""
    conn = sqlite3.connect(DB_PATH)
    clientes = conn.execute("SELECT COUNT(*) FROM clientes").fetchone()[0]
    tareas_hoy = conn.execute(
        "SELECT COUNT(*) FROM tareas WHERE fecha >= date('now')"
    ).fetchone()[0]
    conn.close()

    mundos_info = {}
    for m in BASE.iterdir():
        if m.is_dir() and m.name.startswith("mundo-"):
            mundos_info[m.name] = {
                "herramientas": len(list((m / "herramientas").glob("*.py"))) if (m / "herramientas").exists() else 0,
                "proyectos": len(list((m / "proyectos").iterdir())) if (m / "proyectos").exists() else 0
            }

    return jsonify({
        "clientes_total": clientes,
        "tareas_hoy": tareas_hoy,
        "mundos": mundos_info,
        "ollama": _check_ollama()
    })

@app.route("/contenido/generar", methods=["POST"])
def generar_contenido():
    """Genera contenido con Ollama — mundo-contenido / mundo-social-media"""
    data = request.json or {}
    tipo = data.get("tipo", "post_linkedin")  # post_linkedin | email | seo | propuesta
    tema = data.get("tema", "inteligencia artificial para negocios")
    cliente = data.get("cliente", "generico")

    prompts = {
        "post_linkedin": f"Escribe un post de LinkedIn sobre: {tema}. Máximo 500 caracteres. Tono profesional y cercano. 3 hashtags al final. SOLO el texto, sin comentarios.",
        "post_instagram": f"Escribe un caption de Instagram sobre: {tema}. Máximo 300 caracteres. Incluye emojis y 5 hashtags. SOLO el texto.",
        "email_prospecto": f"Escribe un email de prospección B2B ofreciendo servicios de IA y automatización para el sector: {tema}. Asunto incluido. Máximo 200 palabras.",
        "propuesta": f"Genera una propuesta profesional de servicios de IA para un cliente en el sector: {tema}. Incluye: problema, solución, precio estimado (500-5000€), timeline. Formato markdown.",
        "seo_meta": f"Genera un title tag SEO (60 chars) y meta description (155 chars) para una agencia de IA especializada en: {tema}.",
        "idea_contenido": f"Dame 5 ideas de contenido viral para redes sociales sobre: {tema}. Para una agencia de automatización con IA. Lista numerada."
    }

    system = "Eres un copywriter experto en marketing digital y tecnología. Escribes en español de España, claro y persuasivo."
    prompt = prompts.get(tipo, prompts["post_linkedin"])

    try:
        resultado = ollama_ask(prompt, system=system)
        log_tarea("mundo-contenido", tipo, data, "completado", resultado)
        return jsonify({"ok": True, "tipo": tipo, "tema": tema, "contenido": resultado})
    except Exception as e:
        log_tarea("mundo-contenido", tipo, data, "error", str(e))
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route("/crm/cliente", methods=["POST"])
def add_cliente():
    """Añade o actualiza cliente en el CRM"""
    data = request.json or {}
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO clientes (nombre, contacto, mundo, estado, presupuesto, notas) VALUES (?,?,?,?,?,?)",
        (data.get("nombre"), data.get("contacto"), data.get("mundo", "mundo-dev-clientes"),
         data.get("estado", "prospecto"), data.get("presupuesto", 0), data.get("notas", ""))
    )
    conn.commit()
    conn.close()
    return jsonify({"ok": True, "mensaje": f"Cliente {data.get('nombre')} registrado"})

@app.route("/crm/clientes", methods=["GET"])
def list_clientes():
    """Lista todos los clientes del CRM"""
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("SELECT * FROM clientes ORDER BY fecha DESC").fetchall()
    conn.close()
    cols = ["id", "nombre", "contacto", "mundo", "estado", "presupuesto", "notas", "fecha"]
    return jsonify([dict(zip(cols, r)) for r in rows])

@app.route("/multimedia/video", methods=["POST"])
def gen_video():
    """Genera vídeo con FFmpeg para redes sociales"""
    data = request.json or {}
    titulo = data.get("titulo", "Universo Agencia IA")
    mensaje = data.get("mensaje", "Automatiza tu negocio con inteligencia artificial")
    cliente = data.get("cliente", "agencia")
    duracion = int(data.get("duracion", 15))

    salida = BASE / "mundo-multimedia" / "proyectos" / f"video_{cliente}_{datetime.date.today()}.mp4"
    os.makedirs(salida.parent, exist_ok=True)

    msg_ffmpeg = mensaje.replace("'", " ").replace(":", " ")
    tit_ffmpeg = titulo.replace("'", " ").replace(":", " ")

    cmd = [
        FFMPEG, "-y",
        "-f", "lavfi", "-i", f"color=c=0x0d1117:size=1080x1920:rate=30",
        "-f", "lavfi", "-i", f"color=c=0x58a6ff:size=1080x1920:rate=30",
        "-filter_complex", (
            "[0][1]overlay=0:0:enable='between(t,0,0.1)'[bg];"
            "[bg]"
            f"drawbox=x=60:y=280:w=960:h=3:color=0x58a6ff:t=fill,"
            f"drawbox=x=60:y=1580:w=960:h=3:color=0x58a6ff:t=fill,"
            f"drawtext=text='{tit_ffmpeg}':fontsize=88:fontcolor=0x58a6ff:"
            f"x=(w-text_w)/2:y=340:fontfile='C\\:/Windows/Fonts/arialbd.ttf':"
            f"alpha='if(lt(t,0.5),t*2,1)',"
            f"drawtext=text='{msg_ffmpeg}':fontsize=46:fontcolor=white:"
            f"x=(w-text_w)/2:y=500:fontfile='C\\:/Windows/Fonts/arial.ttf':"
            f"alpha='if(lt(t,1),max(0,t-0.3)*3,1)',"
            f"drawtext=text='universo-ia.com':fontsize=38:fontcolor=0x58a6ff:"
            f"x=(w-text_w)/2:y=1620:fontfile='C\\:/Windows/Fonts/ariali.ttf',"
            f"fade=t=in:st=0:d=0.5,fade=t=out:st={duracion-1}:d=1"
        ),
        "-t", str(duracion), "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-pix_fmt", "yuv420p", str(salida)
    ]

    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode == 0:
        size = os.path.getsize(salida) / 1024 / 1024
        log_tarea("mundo-multimedia", "gen_video", data, "completado", str(salida))
        return jsonify({"ok": True, "archivo": str(salida), "mb": round(size, 2)})
    else:
        return jsonify({"ok": False, "error": r.stderr[-300:]}), 500

@app.route("/ventas/propuesta", methods=["POST"])
def gen_propuesta():
    """Genera una propuesta comercial completa"""
    data = request.json or {}
    cliente = data.get("cliente", "Cliente")
    sector = data.get("sector", "e-commerce")
    necesidad = data.get("necesidad", "automatizar procesos con IA")
    presupuesto = data.get("presupuesto", "por determinar")

    prompt = f"""Genera una propuesta comercial profesional de NEXIA (Agencia de Inteligencia Artificial) para:
- Cliente: {cliente}
- Sector: {sector}
- Necesidad: {necesidad}
- Presupuesto: {presupuesto}€

Incluye:
1. Resumen ejecutivo (3 líneas)
2. Diagnóstico del problema
3. Solución propuesta con tecnologías específicas
4. Fases de implementación con duración
5. Inversión desglosada
6. ROI estimado
7. Próximos pasos

Formato: Markdown profesional. Idioma: Español."""

    try:
        propuesta = ollama_ask(prompt, system="Eres el director comercial de NEXIA, agencia de IA. Tus propuestas son claras, concretas y convincentes. Siempre incluye resultados esperados con números.")

        path = BASE / "mundo-ventas" / "propuestas" / f"propuesta_{cliente.lower().replace(' ','_')}_{datetime.date.today()}.md"
        os.makedirs(path.parent, exist_ok=True)
        path.write_text(propuesta, encoding="utf-8")

        log_tarea("mundo-ventas", "propuesta", data, "completado", str(path))
        return jsonify({"ok": True, "propuesta": propuesta, "archivo": str(path)})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route("/tarea", methods=["POST"])
def ejecutar_tarea():
    """Endpoint genérico — ejecuta script Python de cualquier mundo"""
    data = request.json or {}
    mundo = data.get("mundo")
    script = data.get("script")
    args = data.get("args", {})

    if not mundo or not script:
        return jsonify({"ok": False, "error": "Falta mundo o script"}), 400

    script_path = BASE / mundo / "herramientas" / script
    if not script_path.exists():
        return jsonify({"ok": False, "error": f"No existe: {script_path}"}), 404

    env = os.environ.copy()
    env.update({k: str(v) for k, v in args.items()})
    r = subprocess.run(["python", str(script_path)], capture_output=True, text=True, env=env, timeout=300)

    log_tarea(mundo, script, args, "completado" if r.returncode == 0 else "error", r.stdout or r.stderr)
    return jsonify({
        "ok": r.returncode == 0,
        "stdout": r.stdout[-1000:],
        "stderr": r.stderr[-300:] if r.returncode != 0 else ""
    })

@app.route("/dispatch", methods=["POST"])
def dispatch():
    """Endpoint único para n8n — recibe tipo y delega al handler correcto"""
    raw = request.json or {}
    # n8n envuelve el body bajo 'body' key; aceptamos ambos formatos
    data = raw.get("body", raw) if isinstance(raw.get("body"), dict) else raw
    tipo = data.get("tipo", "")

    if tipo == "contenido":
        data_inner = {
            "tipo": data.get("subtipo", "post_linkedin"),
            "tema": data.get("tema", "inteligencia artificial"),
            "cliente": data.get("cliente", "agencia")
        }
        with app.test_request_context(json=data_inner):
            from flask import request as req_inner
            req_inner._cached_json = (data_inner, data_inner)
        # Llamar directamente la función
        import urllib.request as ur
        payload = json.dumps(data_inner).encode()
        r = ur.Request("http://localhost:8080/contenido/generar", data=payload, headers={"Content-Type": "application/json"})
        with ur.urlopen(r, timeout=120) as resp:
            return jsonify(json.loads(resp.read()))

    elif tipo == "crm":
        data_inner = {k: v for k, v in data.items() if k != "tipo"}
        payload = json.dumps(data_inner).encode()
        r = urllib.request.Request("http://localhost:8080/crm/cliente", data=payload, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(r, timeout=10) as resp:
            return jsonify(json.loads(resp.read()))

    elif tipo == "video":
        data_inner = {k: v for k, v in data.items() if k != "tipo"}
        payload = json.dumps(data_inner).encode()
        r = urllib.request.Request("http://localhost:8080/multimedia/video", data=payload, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(r, timeout=60) as resp:
            return jsonify(json.loads(resp.read()))

    elif tipo == "propuesta":
        data_inner = {k: v for k, v in data.items() if k != "tipo"}
        payload = json.dumps(data_inner).encode()
        r = urllib.request.Request("http://localhost:8080/ventas/propuesta", data=payload, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(r, timeout=120) as resp:
            return jsonify(json.loads(resp.read()))

    else:
        return jsonify({"ok": False, "error": f"Tipo desconocido: {tipo}. Usa: contenido, crm, video, propuesta"}), 400

# ─── Helpers ──────────────────────────────────────────────────
def _check_ollama():
    try:
        with urllib.request.urlopen("http://localhost:11434/api/tags", timeout=3) as r:
            models = json.loads(r.read()).get("models", [])
            return {"online": True, "modelos": [m["name"] for m in models]}
    except:
        return {"online": False}

# ─── Arranque ─────────────────────────────────────────────────
if __name__ == "__main__":
    init_db()
    print("=" * 50)
    print(" NEXIA — API Central | Puerto 8080")
    print("=" * 50)
    print(f" CRM: {DB_PATH}")
    print(f" Ollama: {_check_ollama()}")
    print("=" * 50)
    app.run(host="0.0.0.0", port=8080, debug=False)
