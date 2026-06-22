#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de articulos SEO optimizados usando Ollama (gratis) o Claude API.
Uso: python generador-articulos.py --keyword "chatbot para restaurantes" --nicho hosteleria
"""

import argparse
import json
import re
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).parent.parent.parent
ARTICULOS_DIR = BASE / "mundo-seo" / "articulos-generados"
ARTICULOS_DIR.mkdir(parents=True, exist_ok=True)

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "qwen2.5-coder:7b"

PLANTILLAS_NICHO = {
    "hosteleria": {
        "audiencia": "duenos de restaurantes, bares y hoteles en Espana",
        "pain_points": ["poco personal", "reservas perdidas", "atencion al cliente lenta"],
        "keywords_relacionadas": ["restaurante automatizacion", "chatbot para bar", "reservas online restaurante"],
    },
    "salud": {
        "audiencia": "clinicas, consultorios y centros de salud privados",
        "pain_points": ["citas perdidas", "llamadas sin respuesta", "historiales manuales"],
        "keywords_relacionadas": ["chatbot clinica", "citas medicas online", "automatizacion salud"],
    },
    "legal": {
        "audiencia": "despachos de abogados y gestorerias",
        "pain_points": ["tiempo en consultas basicas", "documentacion manual", "clientes sin respuesta rapida"],
        "keywords_relacionadas": ["automatizacion legal", "chatbot abogados", "ia para gestoria"],
    },
    "ecommerce": {
        "audiencia": "tiendas online y negocios de venta por internet",
        "pain_points": ["carritos abandonados", "atencion 24h imposible", "devolucioes sin gestionar"],
        "keywords_relacionadas": ["chatbot tienda online", "automatizacion ecommerce", "ia ventas online"],
    },
    "general": {
        "audiencia": "pymes y negocios en Espana",
        "pain_points": ["poco tiempo", "costes altos de personal", "competencia digital"],
        "keywords_relacionadas": ["ia para empresas", "automatizacion negocios", "chatbot empresas"],
    },
}

ESTRUCTURA_SEO = """
Escribe un articulo SEO completo sobre: "{keyword}"
Audiencia objetivo: {audiencia}
Problemas que resuelve: {pain_points}

ESTRUCTURA OBLIGATORIA (usa exactamente estos encabezados):

# {titulo_h1}

## Introduccion (150 palabras, incluye la keyword en las primeras 100 palabras)

## Por que los {nicho} necesitan esto en 2026

## Como funciona: guia paso a paso

## Casos de exito reales (inventa 2 ejemplos realistas con numeros)

## Cuanto cuesta y como calcularlo

## Preguntas frecuentes (5 preguntas con respuesta)

## Conclusion y llamada a la accion

---
REGLAS:
- Longitud total: 1200-1500 palabras
- Tono: profesional pero cercano, en espanol de Espana
- Incluir la keyword principal al menos 8 veces de forma natural
- Incluir keywords relacionadas: {keywords_relacionadas}
- CTA final dirigido a conseguir una consulta gratuita
- Sin usar emojis excesivos
"""


def llamar_ollama(prompt: str) -> str:
    """Llama a Ollama local para generar contenido gratis."""
    payload = json.dumps({
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.7, "num_predict": 2000}
    }).encode("utf-8")

    req = urllib.request.Request(
        OLLAMA_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("response", "")
    except Exception as e:
        return f"[ERROR Ollama: {e}. Asegurate de que Ollama esta corriendo: ollama serve]"


def generar_titulo(keyword: str, nicho: str) -> str:
    titulos = {
        "hosteleria": f"Chatbot para Restaurantes: Cómo {keyword} puede duplicar tus reservas en 30 días",
        "salud": f"{keyword}: La guía definitiva para clínicas que quieren reducir llamadas un 40%",
        "legal": f"Cómo {keyword} ahorra 10 horas semanales a tu despacho de abogados",
        "ecommerce": f"{keyword}: Recupera el 25% de carritos abandonados con inteligencia artificial",
        "general": f"{keyword}: La guía completa para PYMES españolas en 2026",
    }
    return titulos.get(nicho, f"Guía completa: {keyword} para tu negocio en 2026")


def generar_meta_description(keyword: str, nicho: str) -> str:
    return (
        f"Descubre cómo {keyword} puede transformar tu negocio de {nicho}. "
        f"Guía práctica con casos reales, precios y cómo empezar hoy. "
        f"Consulta gratuita disponible."
    )[:160]


def guardar_articulo(keyword: str, contenido: str, meta: str, titulo: str) -> Path:
    slug = re.sub(r'[^a-z0-9]+', '-', keyword.lower()).strip('-')
    fecha = datetime.now().strftime("%Y%m%d")
    nombre = f"{fecha}-{slug}.md"
    ruta = ARTICULOS_DIR / nombre

    encabezado = f"""---
title: {titulo}
meta_description: {meta}
keyword: {keyword}
fecha: {datetime.now().strftime("%Y-%m-%d")}
estado: borrador
---

"""
    ruta.write_text(encabezado + contenido, encoding="utf-8")
    return ruta


def main():
    parser = argparse.ArgumentParser(description="Generador SEO con Ollama")
    parser.add_argument("--keyword", required=True, help='Keyword principal (ej: "chatbot para restaurantes")')
    parser.add_argument("--nicho", default="general", choices=list(PLANTILLAS_NICHO.keys()))
    parser.add_argument("--modelo", default="ollama", choices=["ollama", "claude"])
    args = parser.parse_args()

    nicho_data = PLANTILLAS_NICHO[args.nicho]
    titulo = generar_titulo(args.keyword, args.nicho)
    meta = generar_meta_description(args.keyword, args.nicho)

    prompt = ESTRUCTURA_SEO.format(
        keyword=args.keyword,
        titulo_h1=titulo,
        nicho=args.nicho,
        audiencia=nicho_data["audiencia"],
        pain_points=", ".join(nicho_data["pain_points"]),
        keywords_relacionadas=", ".join(nicho_data["keywords_relacionadas"]),
    )

    print(f"\nGenerando articulo SEO...")
    print(f"  Keyword: {args.keyword}")
    print(f"  Nicho:   {args.nicho}")
    print(f"  Modelo:  {args.modelo} (Ollama = gratis)\n")

    if args.modelo == "ollama":
        contenido = llamar_ollama(prompt)
    else:
        print("[Claude API no configurada aun. Usando Ollama.]")
        contenido = llamar_ollama(prompt)

    ruta = guardar_articulo(args.keyword, contenido, meta, titulo)

    print(f"Articulo guardado en: {ruta}")
    print(f"\nMeta description ({len(meta)} chars):")
    print(f"  {meta}")
    print(f"\nPrimeras lineas del articulo:")
    print(contenido[:300] + "...")


if __name__ == "__main__":
    main()
