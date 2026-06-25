#!/usr/bin/env python3
"""
NEXIA — Cliente LLM unificado: Groq (rapido, gratis, en la nube) con
FALLBACK automatico a Ollama local.

Por que: las herramientas de ventas necesitaban Ollama corriendo en la PC
(localhost:11434). Con esto, si defines GROQ_API_KEY funcionan en CUALQUIER
maquina o VPS sin Ollama. Si Groq falla o no hay key, cae a Ollama local.

Config por variables de entorno (ver .env.example):
  GROQ_API_KEY    -> si esta, se usa Groq primero. Si no, se usa Ollama.
  GROQ_MODEL      -> por defecto "llama-3.3-70b-versatile"
  GROQ_BASE_URL   -> por defecto "https://api.groq.com/openai/v1" (OpenAI-compat)
  OLLAMA_URL      -> por defecto "http://localhost:11434/api/generate"
  OLLAMA_MODEL    -> por defecto "qwen2.5:14b"

Uso:
  from llm import generar
  texto = generar("Escribe un email...", system="Eres comercial de NEXIA")
"""
import os, json, urllib.request

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "").strip()
GROQ_MODEL   = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile").strip()
GROQ_BASE    = os.environ.get("GROQ_BASE_URL", "https://api.groq.com/openai/v1").rstrip("/")
GROQ_URL     = GROQ_BASE + "/chat/completions"

OLLAMA_URL   = os.environ.get("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "qwen2.5:14b")


def backend_activo():
    """Devuelve que backend se usara primero: 'groq' o 'ollama'."""
    return "groq" if GROQ_API_KEY else "ollama"


def _post(url, body, headers, timeout):
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=headers)
    return urllib.request.urlopen(req, timeout=timeout).read().decode("utf-8", "ignore")


def _groq(prompt, system, temperature, max_tokens, timeout):
    msgs = []
    if system:
        msgs.append({"role": "system", "content": system})
    msgs.append({"role": "user", "content": prompt})
    body = {"model": GROQ_MODEL, "messages": msgs, "temperature": temperature, "stream": False}
    if max_tokens:
        body["max_tokens"] = max_tokens
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {GROQ_API_KEY}"}
    data = json.loads(_post(GROQ_URL, body, headers, timeout))
    return data["choices"][0]["message"]["content"].strip()


def _ollama(prompt, system, temperature, max_tokens, timeout):
    full = (system + "\n\n" + prompt) if system else prompt
    opts = {"temperature": temperature}
    if max_tokens:
        opts["num_predict"] = max_tokens
    body = {"model": OLLAMA_MODEL, "prompt": full, "stream": False, "options": opts}
    data = json.loads(_post(OLLAMA_URL, body, {"Content-Type": "application/json"}, timeout))
    return data["response"].strip()


def generar(prompt, system=None, temperature=0.7, max_tokens=None, timeout=120):
    """
    Genera texto. Intenta Groq si hay GROQ_API_KEY; si falla, cae a Ollama local.
    Lanza RuntimeError solo si ambos backends fallan.
    """
    errores = []
    if GROQ_API_KEY:
        try:
            return _groq(prompt, system, temperature, max_tokens, timeout)
        except Exception as e:
            errores.append(f"Groq({GROQ_MODEL}): {e}")
    try:
        return _ollama(prompt, system, temperature, max_tokens, timeout)
    except Exception as e:
        errores.append(f"Ollama({OLLAMA_MODEL}): {e}")
    raise RuntimeError("Ningun backend LLM disponible -> " + " | ".join(errores))
