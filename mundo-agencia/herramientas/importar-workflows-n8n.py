#!/usr/bin/env python3
"""Importa los workflows JSON a n8n via API."""
import json
import urllib.request

KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI5ODY5YTRjNS01NDAxLTRmMTUtOGE3Yy01NTdiMThjNjQwN2UiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwianRpIjoiMmNkYzBmMTktYzI1My00OWUwLWExN2QtMWRlMzM2ZWE1OWRkIiwiaWF0IjoxNzgxODUzMTkyfQ.G3qbvysA5veWZyllFdCMLvJyQAKBOysMJqAf8Csw0Oo"
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
