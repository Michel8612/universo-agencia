#!/usr/bin/env python3
"""
NEXIA — Bot de leads en Telegram (cara al cliente)

Atiende a posibles clientes con IA (Groq), responde dudas sobre NEXIA,
capta el lead al CRM y avisa al dueño. Corre 24/7 en el servidor de USA.
Self-contained: solo necesita bot-leads-config.json (token, groq_key, owner_chat_id).
"""
import urllib.request, urllib.parse, json, time, os, sys

# Salida segura (evita crash por encoding/console nula al correr oculto)
class _Null:
    def write(self, *a, **k): pass
    def flush(self): pass
try:
    if sys.stdout is None: sys.stdout = _Null()
    else: sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    sys.stdout = _Null()

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.join(HERE, "bot-leads-config.json")
CRM_URL = "http://127.0.0.1:8080/crm/cliente"

SISTEMA = """Eres el asistente COMERCIAL de NEXIA, agencia de IA, desarrollo web y automatizacion para pymes. Tu UNICO objetivo es convertir a quien escribe en cliente.

QUE HACE NEXIA (precios orientativos):
- Webs y landing pages: desde 250 EUR (tienda online desde 800 EUR)
- Chatbots con IA: desde 400 EUR
- Automatizacion de procesos: desde 200 EUR
- SEO y marketing: desde 150 EUR
- Asistente IA a medida: desde 900 EUR
La web de NEXIA es nexia-ia-com.netlify.app

GANCHO: diagnostico web GRATIS en 24h (el equipo analiza la web del CLIENTE y le dice que falla y cuanto cuesta arreglarlo).
PROGRAMA FUNDADOR: los 3 primeros clientes tienen 50% de descuento.
PAGO (solo lo mencionas cuando el cliente ya quiere contratar): PayPal y criptomonedas.

COMO ACTUAS (estricto):
1. BREVE: maximo 2-3 frases por respuesta. Nunca parrafos largos.
2. Responde SIEMPRE en el idioma del cliente (detecta su idioma y mantente en el).
3. Habla SOLO de NEXIA y del problema del cliente. Si intenta charlar de otra cosa (politica, vida, temas random, bromas), redirige en UNA frase amable: que estas para ayudarle con su web o negocio.
4. VENDE en cada mensaje: detecta su necesidad, muestra como NEXIA la resuelve, y pide sus datos (nombre, su web o negocio, email) para el diagnostico gratis. Cuando haya interes real, propon empezar y explica el pago (PayPal/cripto).
5. NO inventes datos ni plazos exactos. Si te piden diagnosticar una web, pide la URL de SU web (tu no navegas en vivo; el equipo le envia el diagnostico en 24h).
6. Tu representas a NEXIA. Si te piden "diagnostica tu web", entiende que se refieren a la web del cliente; nunca digas que no tienes web.
7. No te repitas ni te enrolles. Cada respuesta debe acercar la venta o capturar un dato."""

conversaciones = {}   # chat_id -> [ {role, content}, ... ]
leads_vistos = set()

def cfg_load():
    try: return json.load(open(CFG, encoding="utf-8"))
    except Exception: return {}

def groq(cfg, messages, max_tokens=220):
    body = json.dumps({"model": cfg.get("groq_model", "llama-3.3-70b-versatile"),
                       "messages": messages, "max_tokens": max_tokens, "temperature": 0.6}).encode()
    req = urllib.request.Request("https://api.groq.com/openai/v1/chat/completions", data=body,
        headers={"Authorization": f"Bearer {cfg['groq_key']}", "Content-Type": "application/json",
                 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) NEXIA/1.0"})
    return json.loads(urllib.request.urlopen(req, timeout=60).read())["choices"][0]["message"]["content"].strip()

def tg(token, method, params):
    data = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(f"https://api.telegram.org/bot{token}/{method}", data=data)
    return json.loads(urllib.request.urlopen(req, timeout=70).read())

def guardar_lead(nombre, contacto, nota):
    try:
        payload = json.dumps({"nombre": nombre, "contacto": contacto, "mundo": "mundo-ventas",
                              "estado": "lead_chatbot", "presupuesto": 0, "notas": nota}).encode()
        urllib.request.urlopen(urllib.request.Request(CRM_URL, data=payload,
            headers={"Content-Type": "application/json"}), timeout=8)
    except Exception:
        pass

def main():
    cfg = cfg_load()
    if not cfg.get("token") or not cfg.get("groq_key"):
        print("Falta token o groq_key en bot-leads-config.json"); return
    token = cfg["token"]
    owner = cfg.get("owner_chat_id")
    print("Bot de leads NEXIA en marcha")
    offset = 0
    while True:
        try:
            r = tg(token, "getUpdates", {"offset": offset, "timeout": 50})
            for upd in r.get("result", []):
                offset = upd["update_id"] + 1
                msg = upd.get("message")
                if not msg or "text" not in msg:
                    continue
                chat_id = msg["chat"]["id"]
                text = msg["text"].strip()[:500]  # limita entradas largas (anti-quema de API)
                nombre = (msg["from"].get("first_name", "") + " " + msg["from"].get("last_name", "")).strip() or "Lead Telegram"
                usuario = msg["from"].get("username")
                contacto = (f"@{usuario}" if usuario else f"tg:{chat_id}")

                # Lead nuevo -> guardar en CRM + avisar al duenno
                if chat_id not in leads_vistos:
                    leads_vistos.add(chat_id)
                    guardar_lead(nombre, contacto, f"Lead via chatbot Telegram. Primer mensaje: {text[:120]}")
                    if owner:
                        try:
                            tg(token, "sendMessage", {"chat_id": owner,
                                "text": f"🔔 Nuevo lead en el chatbot: {nombre} ({contacto})\nDijo: {text[:150]}"})
                        except Exception: pass

                # Conversacion con memoria
                hist = conversaciones.setdefault(chat_id, [])
                hist.append({"role": "user", "content": text})
                messages = [{"role": "system", "content": SISTEMA}] + hist[-8:]
                try:
                    resp = groq(cfg, messages)
                except Exception:
                    resp = "Disculpa, tuve un problema tecnico. ¿Puedes repetirlo en un momento?"
                hist.append({"role": "assistant", "content": resp})
                tg(token, "sendMessage", {"chat_id": chat_id, "text": resp})
        except Exception as e:
            print("loop error:", e); time.sleep(5)

if __name__ == "__main__":
    main()
