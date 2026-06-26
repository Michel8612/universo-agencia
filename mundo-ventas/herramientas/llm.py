#!/usr/bin/env python3
"""
NEXIA — Módulo central de IA.

Una sola función `generar(prompt)` que usan TODAS las herramientas.
Prioriza Groq (nube, gratis, Llama 3.3 70B) y cae a Ollama local si falla.
Así el servidor de 4GB no necesita modelo local: solo una llamada HTTP.

Config en llm-config.json (NO se sube a git):
  { "groq_key": "gsk_...", "groq_model": "llama-3.3-70b-versatile",
    "ollama_model": "qwen2.5:14b" }
"""
import urllib.request, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.join(HERE, "llm-config.json")

def _cfg():
    try:
        return json.load(open(CFG, encoding="utf-8"))
    except Exception:
        return {}

def _groq(cfg, prompt, max_tokens, temperatura):
    body = json.dumps({
        "model": cfg.get("groq_model", "llama-3.3-70b-versatile"),
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens, "temperature": temperatura,
    }).encode()
    req = urllib.request.Request(
        "https://api.groq.com/openai/v1/chat/completions", data=body,
        headers={"Authorization": f"Bearer {cfg['groq_key']}", "Content-Type": "application/json",
                 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) NEXIA/1.0"})
    r = json.loads(urllib.request.urlopen(req, timeout=60).read())
    return r["choices"][0]["message"]["content"].strip()

def _ollama(cfg, prompt):
    body = json.dumps({"model": cfg.get("ollama_model", "qwen2.5:14b"),
                       "prompt": prompt, "stream": False}).encode()
    req = urllib.request.Request("http://localhost:11434/api/generate",
        data=body, headers={"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=120).read())["response"].strip()

def generar(prompt, max_tokens=600, temperatura=0.7):
    """Genera texto. Groq primero (nube), Ollama de respaldo. Nunca lanza excepción."""
    cfg = _cfg()
    if cfg.get("groq_key"):
        try:
            return _groq(cfg, prompt, max_tokens, temperatura)
        except Exception:
            pass
    try:
        return _ollama(cfg, prompt)
    except Exception as e:
        return f"(IA no disponible: {e})"

if __name__ == "__main__":
    print(generar("Di 'hola' en una palabra."))
