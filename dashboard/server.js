// NEXIA — Dashboard del Universo (Node.js puro, sin dependencias)
// Arrancar:  node dashboard/server.js   ->  http://127.0.0.1:3000
// Centro de control de toda la agencia: planetas (mundos), CRM, servicios y acciones.
const http = require("http");
const fs = require("fs");
const path = require("path");
const { spawn } = require("child_process");

const BASE = path.resolve(__dirname, "..");
const PY = "C:\\Program Files\\Python312\\python.exe";
const TOOLS = path.join(BASE, "mundo-ventas", "herramientas");
const LOG = path.join(BASE, "dashboard", "ultima-accion.log");
const PORT = 3000;
const FLASK = "http://127.0.0.1:8080";

// --- helpers ---
function get(url, timeout = 2500) {
  return new Promise((resolve) => {
    const req = http.get(url, { timeout }, (res) => {
      let d = ""; res.on("data", (c) => (d += c));
      res.on("end", () => resolve({ ok: res.statusCode === 200, body: d }));
    });
    req.on("error", () => resolve({ ok: false, body: "" }));
    req.on("timeout", () => { req.destroy(); resolve({ ok: false, body: "" }); });
  });
}

async function status() {
  const [flask, n8n, ollama] = await Promise.all([
    get(FLASK + "/"), get("http://127.0.0.1:5678/healthz"), get("http://localhost:11434/api/tags"),
  ]);
  return { "CRM / API (8080)": flask.ok, "n8n (5678)": n8n.ok, "Ollama (11434)": ollama.ok };
}

function lanzar(script, args) {
  const out = fs.createWriteStream(LOG);
  out.write(`> ${script} ${args.join(" ")}\n`);
  const p = spawn(PY, [path.join(TOOLS, script), ...args], { cwd: TOOLS });
  p.stdout.pipe(out); p.stderr.pipe(out);
  p.on("close", () => fs.appendFileSync(LOG, "\n--- TERMINADO ---\n"));
}

// --- server ---
const server = http.createServer(async (req, res) => {
  const u = new URL(req.url, "http://x");
  const send = (code, body, type = "application/json") => {
    res.writeHead(code, { "Content-Type": type }); res.end(body);
  };

  if (u.pathname === "/") {
    return send(200, fs.readFileSync(path.join(__dirname, "public", "index.html")), "text/html; charset=utf-8");
  }
  if (u.pathname === "/api/status") {
    return send(200, JSON.stringify(await status()));
  }
  if (u.pathname === "/api/leads") {
    // Lee el CRM sqlite directo (no depende de Flask) via python
    const db = path.join(BASE, "mundo-agencia", "crm", "agencia.db");
    const code = `import sqlite3,json
try:
 c=sqlite3.connect(r"${db}");rows=c.execute("SELECT nombre,contacto,estado FROM clientes ORDER BY id DESC LIMIT 100").fetchall();c.close()
 print(json.dumps([{"nombre":a or "","contacto":b or "","estado":d or ""} for a,b,d in rows]))
except Exception as e:
 print("[]")`;
    const p = spawn(PY, ["-c", code]);
    let out = ""; p.stdout.on("data", (c) => (out += c));
    p.on("close", () => send(200, out.trim() || "[]"));
    return;
  }
  if (u.pathname === "/api/estado") {
    const r = await get(FLASK + "/estado", 4000);
    return send(200, r.ok ? r.body : "{}");
  }
  if (u.pathname === "/api/log") {
    let t = ""; try { t = fs.readFileSync(LOG, "utf8").slice(-4000); } catch {}
    return send(200, JSON.stringify({ log: t || "(sin acciones todavia)" }));
  }
  if (u.pathname === "/api/cazar" && req.method === "POST") {
    let b = ""; req.on("data", (c) => (b += c));
    req.on("end", () => {
      let d = {}; try { d = JSON.parse(b); } catch {}
      const nicho = d.nicho || "restaurantes", ciudad = d.ciudad || "Miami", pais = d.pais || "USA";
      lanzar("scraper-leads.py", ["--nicho", nicho, "--ciudad", ciudad, "--pais", pais,
        "--solo-con-web", "--enriquecer", "--clasificar", "--crm", "--limite", "50"]);
      send(200, JSON.stringify({ ok: true }));
    });
    return;
  }
  send(404, JSON.stringify({ error: "no encontrado" }));
});

server.listen(PORT, "127.0.0.1", () =>
  console.log(`NEXIA Universo Dashboard -> http://127.0.0.1:${PORT}`));
