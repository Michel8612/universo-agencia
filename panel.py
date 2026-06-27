#!/usr/bin/env python3
"""
NEXIA — Panel de control LOCAL (sin dependencias, sin API de pago)

Un solo archivo. Lo arrancas con:   python panel.py
Luego abre en el navegador:          http://127.0.0.1:8090

Desde el panel puedes:
- Ver los leads del CRM
- Lanzar una caza de leads (nicho + ciudad + pais)
- Ver el estado de los servicios (n8n, Ollama, CRM)
- Ver el log de la ultima caza
Todo local. No gasta tokens de Claude.
"""
import os, sys, json, sqlite3, subprocess, threading, urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

BASE = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable
CRM_DB = os.path.join(BASE, "mundo-agencia", "crm", "agencia.db")
SCRAPER = os.path.join(BASE, "mundo-ventas", "herramientas", "scraper-leads.py")
CAMPANA = os.path.join(BASE, "mundo-ventas", "herramientas", "campana-leads.py")
TOOLS = os.path.join(BASE, "mundo-ventas", "herramientas")
LOG = os.path.join(BASE, "panel-ultima-caza.log")
PORT = 8090

NICHOS = ["restaurantes","cafeterias","bares","hoteles","peluquerias","belleza","spa",
          "gimnasios","dentistas","clinicas","fisioterapia","psicologos","abogados",
          "inmobiliarias","asesorias","talleres","fontaneros","electricistas",
          "fotografos","tiendas-ropa","joyerias","floristerias","veterinarios","opticas"]

def up(url):
    try:
        return urllib.request.urlopen(url, timeout=1.2).status == 200
    except Exception:
        return False

def leer_leads(limite=200):
    try:
        c = sqlite3.connect(CRM_DB)
        rows = c.execute("SELECT id,nombre,contacto,estado,notas FROM clientes ORDER BY id DESC LIMIT ?", (limite,)).fetchall()
        c.close()
        return [{"id":r[0],"nombre":r[1],"contacto":r[2] or "","estado":r[3] or "","notas":(r[4] or "")[:90]} for r in rows]
    except Exception as e:
        return [{"id":0,"nombre":f"(error leyendo CRM: {e})","contacto":"","estado":"","notas":""}]

def lanzar_caza(nicho, ciudad, pais):
    args = [PY, SCRAPER, "--nicho", nicho, "--ciudad", ciudad, "--pais", pais,
            "--solo-con-web", "--enriquecer", "--clasificar", "--crm", "--limite", "50"]
    def run():
        with open(LOG, "w", encoding="utf-8") as f:
            f.write(f"Cazando {nicho} en {ciudad} ({pais})...\n")
            try:
                p = subprocess.Popen(args, cwd=TOOLS, stdout=f, stderr=subprocess.STDOUT, text=True)
                p.wait()
                f.write("\n--- CAZA TERMINADA ---\n")
            except Exception as e:
                f.write(f"\nERROR: {e}\n")
    threading.Thread(target=run, daemon=True).start()

HTML = """<!doctype html><html lang=es><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>NEXIA Panel</title>
<style>
*{box-sizing:border-box;font-family:system-ui,Segoe UI,sans-serif}
body{margin:0;background:#08080c;color:#e5e7eb}
.wrap{max-width:1000px;margin:0 auto;padding:20px}
h1{font-size:22px}.b{color:#60a5fa}
.row{display:flex;gap:12px;flex-wrap:wrap;margin:12px 0}
.card{background:#0d1426;border:1px solid #1e293b;border-radius:12px;padding:16px;flex:1;min-width:260px}
.dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px}
input,select,button{padding:9px;border-radius:8px;border:1px solid #334155;background:#0a1120;color:#e5e7eb}
button{background:#2563eb;border:0;cursor:pointer;font-weight:600}
button:hover{background:#3b82f6}
table{width:100%;border-collapse:collapse;font-size:13px;margin-top:8px}
th,td{text-align:left;padding:7px;border-bottom:1px solid #1e293b}
th{color:#94a3b8}
pre{background:#0a1120;border:1px solid #1e293b;border-radius:8px;padding:10px;font-size:12px;max-height:220px;overflow:auto;white-space:pre-wrap}
.muted{color:#64748b;font-size:12px}
</style></head><body><div class=wrap>
<h1>NEX<span class=b>IA</span> · Panel local</h1>
<div class=muted>Todo corre en tu PC. No gasta tokens de Claude.</div>

<div class=row>
  <div class=card>
    <b>Estado</b><div id=estado style=margin-top:8px>Cargando...</div>
  </div>
  <div class=card>
    <b>Cazar leads</b>
    <div class=row style=margin-top:8px>
      <select id=nicho></select>
      <input id=ciudad placeholder="Ciudad (ej: Miami)" value="Miami">
      <input id=pais placeholder="Pais" value="USA" style=max-width:90px>
      <button onclick=cazar()>Cazar</button>
    </div>
    <div id=cazamsg class=muted></div>
  </div>
</div>

<div class=card>
  <b>Log de la ultima caza</b> <button onclick=verlog() style=float:right;padding:4px_10px>Refrescar</button>
  <pre id=log>—</pre>
</div>

<div class=card style=margin-top:12px>
  <b>Leads en el CRM</b> <button onclick=verleads() style=float:right;padding:4px_10px>Refrescar</button>
  <span id=nleads class=muted></span>
  <table><thead><tr><th>Nombre</th><th>Contacto</th><th>Estado</th><th>Notas</th></tr></thead>
  <tbody id=leads></tbody></table>
</div>
</div>
<script>
const NICHOS=__NICHOS__;
nicho.innerHTML=NICHOS.map(n=>`<option>${n}</option>`).join('');
async function j(u,o){const r=await fetch(u,o);return r.json()}
async function verestado(){const s=await j('/api/status');
 estado.innerHTML=Object.entries(s).map(([k,v])=>`<div><span class=dot style=background:${v?'#22c55e':'#ef4444'}></span>${k}</div>`).join('')}
async function verleads(){const d=await j('/api/leads');nleads.textContent=`(${d.length})`;
 leads.innerHTML=d.map(l=>`<tr><td>${l.nombre}</td><td>${l.contacto}</td><td>${l.estado}</td><td class=muted>${l.notas}</td></tr>`).join('')}
async function verlog(){const d=await j('/api/log');log.textContent=d.log||'—'}
async function cazar(){cazamsg.textContent='Lanzando...';
 const r=await j('/api/scraper',{method:'POST',headers:{'Content-Type':'application/json'},
   body:JSON.stringify({nicho:nicho.value,ciudad:ciudad.value,pais:pais.value})});
 cazamsg.textContent=r.ok?'Caza lanzada. Mira el log en unos segundos.':'Error';
 setTimeout(verlog,3000)}
verestado();verleads();verlog();setInterval(verestado,15000)
</script></body></html>"""

class H(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.0"
    def _send(self, code, body, ctype="application/json"):
        b = body.encode("utf-8") if isinstance(body, str) else body
        self.send_response(code); self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(b)))
        self.send_header("Connection", "close"); self.end_headers(); self.wfile.write(b)
    def log_message(self, *a): pass
    def do_GET(self):
        p = urlparse(self.path).path
        if p == "/":
            self._send(200, HTML.replace("__NICHOS__", json.dumps(NICHOS)), "text/html; charset=utf-8")
        elif p == "/api/leads":
            self._send(200, json.dumps(leer_leads()))
        elif p == "/api/status":
            self._send(200, json.dumps({
                "CRM (8080)": up("http://127.0.0.1:8080/"),
                "n8n (5678)": up("http://127.0.0.1:5678/healthz"),
                "Ollama (11434)": up("http://localhost:11434/api/tags"),
            }))
        elif p == "/api/log":
            try: txt = open(LOG, encoding="utf-8").read()[-4000:]
            except Exception: txt = "(sin caza todavia)"
            self._send(200, json.dumps({"log": txt}))
        else:
            self._send(404, json.dumps({"error": "no encontrado"}))
    def do_POST(self):
        if urlparse(self.path).path == "/api/scraper":
            n = int(self.headers.get("Content-Length", 0))
            d = json.loads(self.rfile.read(n) or "{}")
            nicho = d.get("nicho", "restaurantes"); ciudad = d.get("ciudad", "Miami"); pais = d.get("pais", "USA")
            lanzar_caza(nicho, ciudad, pais)
            self._send(200, json.dumps({"ok": True}))
        else:
            self._send(404, json.dumps({"error": "no encontrado"}))

if __name__ == "__main__":
    print(f"NEXIA Panel en http://127.0.0.1:{PORT}  (Ctrl+C para parar)")
    ThreadingHTTPServer(("127.0.0.1", PORT), H).serve_forever()
