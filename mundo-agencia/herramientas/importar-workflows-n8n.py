#!/usr/bin/env python3
"""Importa los workflows JSON a n8n via API."""
import json
import os
import sys
import urllib.request

# API key fuera del código: se lee de D:\Proyectos claude\.env (gitignored)
def _cargar_env():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    envp = os.path.join(root, ".env")
    if os.path.exists(envp):
        for line in open(envp, encoding="utf-8"):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
_cargar_env()
KEY = os.environ.get("N8N_API_KEY", "")
if not KEY:
    print("[x] Falta N8N_API_KEY en .env (D:\\Proyectos claude\\.env)")
    sys.exit(1)
BASE = "http://localhost:5678/api/v1"

WORKFLOWS = [
    r"D:\Proyectos claude\mundo-seo\herramientas\wf-seo-import.json",
    r"D:\Proyectos claude\mundo-social-media\herramientas\wf-social-import.json",
]

for path in WORKFLOWS:
    data = open(path, "rb").read()
    req = urllib.request.Request(BASE + "/workflows", data=data, method="POST")
    req.add_header("X-N8N-API-KEY", KEY)
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as r:
            resp = json.loads(r.read())
            print("Creado:", resp["name"], "- ID:", resp["id"])
    except Exception as e:
        print("Error:", e)

print("Verificando workflows en n8n...")
req2 = urllib.request.Request(BASE + "/workflows")
req2.add_header("X-N8N-API-KEY", KEY)
with urllib.request.urlopen(req2) as r:
    lista = json.loads(r.read())
    for wf in lista.get("data", []):
        print(" -", wf["name"], "| activo:", wf["active"])
