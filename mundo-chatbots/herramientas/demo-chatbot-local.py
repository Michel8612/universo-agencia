"""
NEXIA — Demo Chatbot Local (usa Ollama, sin API keys)
Crea un chatbot configurable por sector para demos a clientes

Uso:
  python demo-chatbot-local.py --sector salud --nombre "Clínica García"
  python demo-chatbot-local.py --sector hosteleria --nombre "Hotel Mediterráneo"

Abre http://localhost:7860 en el navegador
"""
import argparse, json, urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler

OLLAMA = "http://localhost:11434/api/generate"
PORT = 7860

SECTORES = {
    "salud": {
        "icono": "🏥",
        "color": "#3b82f6",
        "sistema": """Eres el asistente virtual de {nombre}. Ayudas a los pacientes con:
- Información sobre servicios y especialidades
- Cómo pedir cita (deben llamar al número o usar el formulario web)
- Horarios de atención
- Preguntas frecuentes sobre tratamientos
- Orientación sobre qué especialista necesitan

Siempre sé empático, claro y profesional. Si es urgencia médica, deriva al 112.""",
        "faq": "Citas, horarios, especialidades, precios orientativos, ubicación",
    },
    "hosteleria": {
        "icono": "🏨",
        "color": "#10b981",
        "sistema": """Eres el concierge virtual de {nombre}. Asistes a los huéspedes con:
- Información sobre habitaciones y servicios
- Proceso de reserva y check-in/out
- Actividades y atracciones locales
- Servicios del hotel (spa, restaurante, parking)
- Solicitudes especiales durante la estancia

Tono: cálido, hospitalario y servicial.""",
        "faq": "Reservas, precios, servicios, ubicación, políticas de cancelación",
    },
    "restaurante": {
        "icono": "🍽️",
        "color": "#f59e0b",
        "sistema": """Eres el asistente virtual de {nombre}. Ayudas con:
- Información sobre el menú y platos especiales
- Reservas de mesa (recoge nombre, día, hora, número de personas)
- Alérgenos e información dietética
- Horarios y ubicación
- Opciones para llevar y delivery

Sé amable y apetitoso al describir los platos.""",
        "faq": "Menú, alérgenos, reservas, horarios, delivery",
    },
    "legal": {
        "icono": "⚖️",
        "color": "#6366f1",
        "sistema": """Eres el asistente de {nombre}, despacho de abogados. Orientas a potenciales clientes sobre:
- Áreas de práctica del despacho
- Cómo funciona la primera consulta (y si es gratuita)
- Documentación que necesitan aportar
- Proceso general de cada tipo de caso
- Costes orientativos y formas de pago

IMPORTANTE: No das consejo legal concreto. Siempre recomienda una consulta con el abogado.""",
        "faq": "Consulta inicial, especialidades, costes, proceso",
    },
    "ecommerce": {
        "icono": "🛒",
        "color": "#ec4899",
        "sistema": """Eres el asistente de ventas de {nombre}. Ayudas a los clientes con:
- Información sobre productos y disponibilidad
- Estado de pedidos y envíos
- Política de devoluciones y garantías
- Métodos de pago aceptados
- Descuentos y promociones actuales
- Recomendaciones personalizadas

Objetivo: convertir visitas en ventas de forma natural.""",
        "faq": "Productos, pedidos, envíos, devoluciones, pagos",
    },
    "inmobiliaria": {
        "icono": "🏠",
        "color": "#8b5cf6",
        "sistema": """Eres el asistente de {nombre}, agencia inmobiliaria. Ayudas con:
- Información sobre propiedades disponibles
- Proceso de compra, venta o alquiler
- Documentación necesaria para cada operación
- Financiación y pasos con el banco
- Agenda visitas (recoge nombre, contacto, propiedad de interés y disponibilidad)

Cualifica amablemente: ¿compra o alquila?, ¿tiene financiación?, ¿cuándo busca?""",
        "faq": "Propiedades, proceso compraventa, visitas, financiación",
    },
}

HTML = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{nombre} — Asistente IA</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:#f0f2f5;height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center}}
.chat-container{{width:420px;height:680px;background:#fff;border-radius:20px;box-shadow:0 20px 60px rgba(0,0,0,.15);display:flex;flex-direction:column;overflow:hidden}}
.chat-header{{background:{color};color:#fff;padding:20px;display:flex;align-items:center;gap:12px}}
.chat-header .avatar{{font-size:28px;background:rgba(255,255,255,.2);border-radius:50%;width:48px;height:48px;display:flex;align-items:center;justify-content:center}}
.chat-header h2{{font-size:16px;font-weight:600}}
.chat-header p{{font-size:12px;opacity:.85;margin-top:2px}}
.online-dot{{width:8px;height:8px;background:#4ade80;border-radius:50%;display:inline-block;margin-right:4px}}
.messages{{flex:1;overflow-y:auto;padding:16px;display:flex;flex-direction:column;gap:12px}}
.msg{{max-width:80%;padding:10px 14px;border-radius:16px;font-size:14px;line-height:1.5}}
.msg.bot{{background:#f3f4f6;color:#1f2937;border-bottom-left-radius:4px;align-self:flex-start}}
.msg.user{{background:{color};color:#fff;border-bottom-right-radius:4px;align-self:flex-end}}
.msg.typing{{color:#9ca3af;font-style:italic}}
.input-area{{padding:16px;border-top:1px solid #e5e7eb;display:flex;gap:8px}}
.input-area input{{flex:1;border:1px solid #e5e7eb;border-radius:24px;padding:10px 16px;font-size:14px;outline:none;transition:border .2s}}
.input-area input:focus{{border-color:{color}}}
.input-area button{{background:{color};color:#fff;border:none;border-radius:50%;width:40px;height:40px;cursor:pointer;font-size:18px;transition:opacity .2s}}
.input-area button:hover{{opacity:.85}}
.branding{{font-size:11px;color:#9ca3af;text-align:center;padding:8px 0 12px;background:#fff}}
.branding a{{color:{color};text-decoration:none;font-weight:500}}
</style>
</head>
<body>
<div class="chat-container">
  <div class="chat-header">
    <div class="avatar">{icono}</div>
    <div>
      <h2>{nombre}</h2>
      <p><span class="online-dot"></span>Asistente IA — disponible 24/7</p>
    </div>
  </div>
  <div class="messages" id="msgs">
    <div class="msg bot">¡Hola! 👋 Soy el asistente virtual de <strong>{nombre}</strong>. ¿En qué puedo ayudarte hoy?</div>
  </div>
  <div class="input-area">
    <input id="inp" type="text" placeholder="Escribe tu pregunta..." onkeydown="if(event.key==='Enter')send()">
    <button onclick="send()">➤</button>
  </div>
  <div class="branding">Impulsado por IA · <a href="http://nexia.io" target="_blank">NEXIA</a></div>
</div>
<script>
const history = [];
async function send() {{
  const inp = document.getElementById('inp');
  const txt = inp.value.trim();
  if (!txt) return;
  inp.value = '';
  addMsg(txt, 'user');
  history.push({{role:'user', content:txt}});
  const typing = addMsg('...', 'bot typing');
  try {{
    const r = await fetch('/chat', {{method:'POST', headers:{{'Content-Type':'application/json'}}, body:JSON.stringify({{messages:history}})}});
    const d = await r.json();
    typing.remove();
    addMsg(d.reply, 'bot');
    history.push({{role:'assistant', content:d.reply}});
  }} catch(e) {{ typing.remove(); addMsg('Error de conexión. Inténtalo de nuevo.', 'bot'); }}
}}
function addMsg(txt, cls) {{
  const d = document.createElement('div');
  d.className = 'msg ' + cls;
  d.textContent = txt;
  const msgs = document.getElementById('msgs');
  msgs.appendChild(d);
  msgs.scrollTop = msgs.scrollHeight;
  return d;
}}
</script>
</body>
</html>"""

class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args): pass

    def do_GET(self):
        content = HTML.format(
            nombre=self.server.nombre,
            icono=self.server.icono,
            color=self.server.color,
        ).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", len(content))
        self.end_headers()
        self.wfile.write(content)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length))
        messages = body.get("messages", [])

        prompt_parts = []
        for m in messages[-6:]:  # last 6 messages for context
            role = "Usuario" if m["role"] == "user" else "Asistente"
            prompt_parts.append(f"{role}: {m['content']}")
        prompt = "\n".join(prompt_parts) + "\nAsistente:"

        try:
            req = urllib.request.Request(OLLAMA,
                data=json.dumps({
                    "model": "qwen2.5:14b",
                    "system": self.server.sistema,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature": 0.7, "num_predict": 300}
                }).encode(),
                headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=120) as r:
                reply = json.loads(r.read())["response"].strip()
        except Exception as e:
            reply = "Lo siento, estoy teniendo dificultades técnicas. Por favor inténtalo en un momento."

        response = json.dumps({"reply": reply}).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", len(response))
        self.end_headers()
        self.wfile.write(response)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sector", default="ecommerce", choices=list(SECTORES.keys()),
                        help=f"Sector: {', '.join(SECTORES.keys())}")
    parser.add_argument("--nombre", default="Mi Negocio", help="Nombre del negocio")
    parser.add_argument("--puerto", type=int, default=PORT)
    args = parser.parse_args()

    cfg = SECTORES[args.sector]
    server = HTTPServer(("0.0.0.0", args.puerto), Handler)
    server.nombre = args.nombre
    server.icono = cfg["icono"]
    server.color = cfg["color"]
    server.sistema = cfg["sistema"].format(nombre=args.nombre)

    print(f"\n{'='*55}")
    print(f"  NEXIA — Demo Chatbot: {args.nombre}")
    print(f"  Sector: {args.sector} {cfg['icono']}")
    print(f"  URL: http://localhost:{args.puerto}")
    print(f"{'='*55}")
    print(f"  Presiona Ctrl+C para parar")
    print(f"{'='*55}\n")
    server.serve_forever()

if __name__ == "__main__":
    main()
