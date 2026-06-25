#!/usr/bin/env python3
"""
NEXIA — MCP de Empleos (Freelancer.com, API pública)

Servidor MCP para usar desde la app de escritorio de Claude. Expone herramientas
para buscar proyectos freelance en vivo (sin login, API pública y legal).

IMPORTANTE: solo BUSCA y muestra empleos. NO auto-aplica (eso viola los ToS y
banea la cuenta). Tú revisas y aplicas manual.

Requiere correr en una máquina con salida a internet (tu PC), NO en la nube de
Claude (su red bloquea freelancer.com).

Instalar y usar: ver mundo-ventas/mcp-empleos/README.md
"""
import json
import urllib.parse
import urllib.request

from mcp.server.fastmcp import FastMCP

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) NEXIA-EmpleosMCP/1.0"
FL_API = "https://www.freelancer.com/api/projects/0.1/projects/active/"
FL_PROJECT = "https://www.freelancer.com/projects/"

# Conversión aproximada a USD para comparar presupuestos
USD = {"USD": 1, "EUR": 1.08, "GBP": 1.27, "AUD": 0.66, "CAD": 0.73, "NZD": 0.61,
       "INR": 0.012, "PKR": 0.0036, "PHP": 0.017, "BRL": 0.18, "MXN": 0.05,
       "ZAR": 0.055, "AED": 0.27, "SGD": 0.74}

mcp = FastMCP("nexia-empleos")


def _get(url, timeout=25):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    return urllib.request.urlopen(req, timeout=timeout).read().decode("utf-8", "ignore")


def _normalizar(p):
    b = p.get("budget", {}) or {}
    bs = p.get("bid_stats", {}) or {}
    moneda = (p.get("currency") or {}).get("code", "USD")
    minimo = b.get("minimum") or 0
    return {
        "titulo": p.get("title", ""),
        "descripcion": (p.get("preview_description") or "")[:300],
        "presupuesto": f"{minimo}-{b.get('maximum') or 0} {moneda}",
        "usd_min": round(minimo * USD.get(moneda, 0.5)),
        "pujas": bs.get("bid_count") or 0,
        "skills": [j.get("name") for j in (p.get("jobs") or [])][:6],
        "url": FL_PROJECT + p.get("seo_url", ""),
    }


@mcp.tool()
def buscar_empleos(query: str, min_budget_usd: int = 100, max_competencia: int = 60,
                   limite: int = 20) -> str:
    """
    Busca proyectos freelance activos en Freelancer.com por término.

    Args:
        query: término de búsqueda (ej. "chatbot", "next.js", "automation").
        min_budget_usd: presupuesto mínimo en USD (filtra proyectos pequeños).
        max_competencia: máximo de pujas (menos pujas = más opciones de ganar).
        limite: número de proyectos a traer de la API antes de filtrar.

    Devuelve los empleos relevantes ordenados por menos competencia y mayor presupuesto.
    """
    params = urllib.parse.urlencode({
        "query": query, "limit": limite, "full_description": "true",
        "job_details": "true", "sort_field": "time_updated",
    })
    try:
        data = json.loads(_get(f"{FL_API}?{params}"))
    except Exception as e:
        return f"Error consultando Freelancer.com (¿hay salida a internet en esta máquina?): {e}"

    proyectos = data.get("result", {}).get("projects", [])
    out = []
    for p in proyectos:
        t = _normalizar(p)
        if t["usd_min"] < min_budget_usd or t["pujas"] > max_competencia:
            continue
        out.append(t)
    out.sort(key=lambda x: (x["pujas"], -x["usd_min"]))

    if not out:
        return f"Sin resultados para '{query}' con min ${min_budget_usd} y <{max_competencia} pujas."

    lineas = [f"{len(out)} empleos para '{query}':\n"]
    for t in out:
        lineas.append(
            f"• {t['titulo']}\n  💰 {t['presupuesto']} (~${t['usd_min']}) | 🧑‍💻 {t['pujas']} pujas | "
            f"{', '.join(t['skills'])}\n  🔗 {t['url']}"
        )
    return "\n".join(lineas)


if __name__ == "__main__":
    mcp.run()
