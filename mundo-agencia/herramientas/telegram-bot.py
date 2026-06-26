#!/usr/bin/env python3
"""
NEXIA — Bot de Telegram (centro de mando)

Centro de control de la agencia desde el móvil, incluso con mala conexión.
- Te avisa de leads nuevos
- Consultas estado del sistema y leads desde el chat
- Lanzas campañas y búsqueda de trabajos con un comando

Sin dependencias externas (usa la API de Telegram vía urllib).

Config: telegram-bot-config.json (token + owner_chat_id).
El PRIMER usuario que escriba /start se queda como dueño (seguridad).

Uso:
  python telegram-bot.py            # arranca el bot (long polling)
  python telegram-bot.py --notificar "mensaje"   # envía aviso al dueño y sale
"""
import urllib.request, urllib.parse, json, time, os, sys, subprocess, sqlite3

# Salida segura: evita crash por encoding/console nula al correr oculto
class _Null:
    def write(self, *a, **k): pass
    def flush(self): pass
try:
    if sys.stdout is None:
        sys.stdout = _Null()
    else:
        sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    sys.stdout = _Null()

HERE = os.path.dirname(__file__)
CFG = os.path.join(HERE, "telegram-bot-config.json")
CRM_DB = r"D:\Proyectos claude\mundo-agencia\crm\agencia.db"
PY = r"C:\Program Files\Python312\python.exe"
TOOLS = r"D:\Proyectos claude\mundo-ventas\herramientas"

def cfg_load():
    if os.path.exists(CFG):
        return json.load(open(CFG, encoding="utf-8"))
    return {"token": "", "owner_chat_id": None}

def cfg_save(c):
    json.dump(c, open(CFG, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

def api(token, method, params=None):
    url = f"https://api.telegram.org/bot{token}/{method}"
    data = urllib.parse.urlencode(params or {}).encode()
    req = urllib.request.Request(url, data=data)
    return json.loads(urllib.request.urlopen(req, timeout=70).read())

def send(token, chat_id, text):
    try:
        api(token, "sendMessage", {"chat_id": chat_id, "text": text, "parse_mode": "HTML",
                                   "disable_web_page_preview": "true"})
    except Exception as e:
        print("send error:", e)

# ── Acciones de los comandos ────────────────────────────────
def estado():
    def up(url):
        try:
            return urllib.request.urlopen(url, timeout=4).status == 200
        except Exception:
            return False
    n8n = "🟢" if up("http://127.0.0.1:5678/healthz") else "🔴"
    flask = "🟢" if up("http://127.0.0.1:8080/") else "🔴"
    ollama = "🟢" if up("http://localhost:11434/api/tags") else "🔴"
    n_leads = 0
    try:
        c = sqlite3.connect(CRM_DB); n_leads = c.execute("SELECT COUNT(*) FROM clientes").fetchone()[0]; c.close()
    except Exception:
        pass
    return (f"<b>Estado NEXIA</b>\n"
            f"{n8n} n8n (5678)\n{flask} API/CRM (8080)\n{ollama} Ollama (11434)\n"
            f"📋 Leads en CRM: <b>{n_leads}</b>")

def ultimos_leads(n=8):
    try:
        c = sqlite3.connect(CRM_DB)
        rows = c.execute("SELECT nombre, contacto, estado FROM clientes ORDER BY id DESC LIMIT ?", (n,)).fetchall()
        c.close()
    except Exception as e:
        return f"Error leyendo CRM: {e}"
    if not rows:
        return "Sin leads aún."
    out = ["<b>Últimos leads</b>"]
    for nombre, contacto, estado in rows:
        out.append(f"• {nombre} — {contacto or 's/contacto'} [{estado}]")
    return "\n".join(out)

def lanzar(script, args=""):
    try:
        subprocess.Popen(f'"{PY}" "{os.path.join(TOOLS, script)}" {args}',
                         cwd=TOOLS, shell=True,
                         creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        return True
    except Exception as e:
        print("lanzar error:", e); return False

MENU = (
    "<b>NEXIA — Centro de mando</b>\n\n"
    "/estado — estado del sistema y nº de leads\n"
    "/leads — últimos leads del CRM\n"
    "/campana — lanzar campaña de leads (12 líneas)\n"
    "/trabajos — buscar trabajos en Freelancer.com\n"
    "/ayuda — este menú"
)

def manejar(token, cfg, msg):
    chat_id = msg["chat"]["id"]
    text = (msg.get("text") or "").strip()

    # Seguridad: el primer /start fija al dueño
    if cfg["owner_chat_id"] is None and text.startswith("/start"):
        cfg["owner_chat_id"] = chat_id; cfg_save(cfg)
        send(token, chat_id, "✅ Eres el dueño de este bot.\n\n" + MENU)
        return
    if cfg["owner_chat_id"] != chat_id:
        send(token, chat_id, "⛔ Este bot es privado.")
        return

    if text.startswith(("/start", "/ayuda", "/help")):
        send(token, chat_id, MENU)
    elif text.startswith("/estado"):
        send(token, chat_id, estado())
    elif text.startswith("/leads"):
        send(token, chat_id, ultimos_leads())
    elif text.startswith("/campana"):
        ok = lanzar("campana-leads.py", "--combos 12 --por-combo 4 --sin-email")
        send(token, chat_id, "🚀 Campaña lanzada. Llenando el CRM…" if ok else "❌ No se pudo lanzar.")
    elif text.startswith("/trabajos"):
        ok = lanzar("buscar-trabajos.py", "--min-budget 200 --max-competencia 40 --propuestas")
        send(token, chat_id, "🔎 Buscando trabajos + propuestas… (tarda)" if ok else "❌ No se pudo lanzar.")
    else:
        send(token, chat_id, "No entendí. " + MENU)

def main():
    cfg = cfg_load()
    if not cfg.get("token"):
        print("Falta el token en telegram-bot-config.json"); return

    # Modo notificación puntual
    if len(sys.argv) >= 3 and sys.argv[1] == "--notificar":
        if cfg.get("owner_chat_id"):
            send(cfg["token"], cfg["owner_chat_id"], sys.argv[2])
            print("Notificación enviada.")
        else:
            print("Aún no hay dueño (escribe /start al bot primero).")
        return

    print("Bot NEXIA en marcha (Ctrl+C para parar)…")
    offset = 0
    while True:
        try:
            r = api(cfg["token"], "getUpdates", {"offset": offset, "timeout": 50})
            for upd in r.get("result", []):
                offset = upd["update_id"] + 1
                if "message" in upd:
                    cfg = cfg_load()  # recargar por si cambió el dueño
                    manejar(cfg["token"], cfg, upd["message"])
        except Exception as e:
            print("loop error:", e); time.sleep(5)

if __name__ == "__main__":
    main()
