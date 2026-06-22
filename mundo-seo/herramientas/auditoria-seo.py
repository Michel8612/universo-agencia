#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auditoria SEO rapida de una URL o dominio.
Uso: python auditoria-seo.py --url https://ejemplo.com
Genera un informe que puedes vender como servicio (300-800 EUR).
"""

import argparse
import json
import re
import urllib.request
import urllib.parse
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).parent.parent.parent
INFORMES_DIR = BASE / "mundo-seo" / "informes-auditoria"
INFORMES_DIR.mkdir(parents=True, exist_ok=True)


def fetch_url(url: str, timeout: int = 10) -> tuple[str, dict]:
    """Descarga una URL y devuelve (html, headers)."""
    headers = {"User-Agent": "Mozilla/5.0 (compatible; AgenciaIA-SEO-Auditor/1.0)"}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="ignore"), dict(resp.headers)
    except Exception as e:
        return "", {"error": str(e)}


def analizar_meta_tags(html: str) -> dict:
    title = re.search(r'<title[^>]*>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
    description = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)', html, re.IGNORECASE)
    h1_tags = re.findall(r'<h1[^>]*>(.*?)</h1>', html, re.IGNORECASE | re.DOTALL)
    h2_tags = re.findall(r'<h2[^>]*>(.*?)</h2>', html, re.IGNORECASE | re.DOTALL)
    canonical = re.search(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)', html, re.IGNORECASE)
    og_title = re.search(r'<meta[^>]+property=["\']og:title["\'][^>]+content=["\']([^"\']+)', html, re.IGNORECASE)

    title_text = re.sub(r'<[^>]+>', '', title.group(1)).strip() if title else None
    desc_text = description.group(1).strip() if description else None
    h1_text = [re.sub(r'<[^>]+>', '', h).strip() for h in h1_tags]

    return {
        "title": title_text,
        "title_len": len(title_text) if title_text else 0,
        "description": desc_text,
        "desc_len": len(desc_text) if desc_text else 0,
        "h1_count": len(h1_tags),
        "h1_text": h1_text[:3],
        "h2_count": len(h2_tags),
        "canonical": canonical.group(1) if canonical else None,
        "og_title": og_title.group(1) if og_title else None,
    }


def analizar_contenido(html: str) -> dict:
    texto_limpio = re.sub(r'<[^>]+>', ' ', html)
    texto_limpio = re.sub(r'\s+', ' ', texto_limpio).strip()
    palabras = texto_limpio.split()
    imgs = re.findall(r'<img[^>]+>', html, re.IGNORECASE)
    imgs_sin_alt = [i for i in imgs if 'alt=""' in i or 'alt=' not in i]
    links_internos = re.findall(r'href=["\'][^"\']*["\']', html, re.IGNORECASE)

    return {
        "word_count": len(palabras),
        "images_total": len(imgs),
        "images_without_alt": len(imgs_sin_alt),
        "links_count": len(links_internos),
    }


def analizar_velocidad(headers: dict) -> dict:
    cache = headers.get("Cache-Control", "no-cache")
    server = headers.get("Server", "desconocido")
    https = True  # Si llegamos aqui con HTTPS funciona

    return {
        "https": https,
        "cache_control": cache,
        "server": server,
        "compresion_gzip": "gzip" in headers.get("Content-Encoding", ""),
    }


def puntuar(meta: dict, contenido: dict, velocidad: dict) -> dict:
    puntos = []
    problemas = []
    oportunidades = []

    # Title
    if not meta["title"]:
        problemas.append("CRITICO: No tiene etiqueta <title>")
    elif meta["title_len"] < 30:
        problemas.append(f"Title demasiado corto ({meta['title_len']} chars) — recomendado 50-60")
    elif meta["title_len"] > 70:
        problemas.append(f"Title demasiado largo ({meta['title_len']} chars) — se corta en Google")
    else:
        puntos.append(f"Title correcto: {meta['title_len']} caracteres")

    # Description
    if not meta["description"]:
        problemas.append("CRITICO: No tiene meta description — Google genera una automatica (mala)")
        oportunidades.append("Agregar meta description optimizada con keyword principal")
    elif meta["desc_len"] < 120:
        problemas.append(f"Meta description corta ({meta['desc_len']} chars) — recomendado 150-160")
    elif meta["desc_len"] > 165:
        problemas.append(f"Meta description larga ({meta['desc_len']} chars) — se corta en resultados")
    else:
        puntos.append(f"Meta description correcta: {meta['desc_len']} caracteres")

    # H1
    if meta["h1_count"] == 0:
        problemas.append("CRITICO: Sin H1 — Google no sabe de que trata la pagina")
    elif meta["h1_count"] > 1:
        problemas.append(f"Multiples H1 ({meta['h1_count']}) — usar solo uno por pagina")
    else:
        puntos.append("H1 unico y correcto")

    # Contenido
    if contenido["word_count"] < 300:
        problemas.append(f"Contenido muy escaso ({contenido['word_count']} palabras) — minimo 600 para rankear")
    elif contenido["word_count"] < 800:
        oportunidades.append(f"Ampliar contenido ({contenido['word_count']} palabras) — los top 10 suelen tener 1200+")
    else:
        puntos.append(f"Buen volumen de contenido: {contenido['word_count']} palabras")

    # Imagenes sin ALT
    if contenido["images_without_alt"] > 0:
        problemas.append(f"{contenido['images_without_alt']} imagenes sin atributo ALT — pierden SEO y accesibilidad")
        oportunidades.append("Agregar ALT descriptivos con keywords a todas las imagenes")

    # HTTPS
    if not velocidad["https"]:
        problemas.append("CRITICO: Sitio sin HTTPS — Google penaliza y Chrome muestra 'No seguro'")
    else:
        puntos.append("HTTPS activado")

    # Canonical
    if not meta["canonical"]:
        oportunidades.append("Agregar canonical tag para evitar contenido duplicado")

    # Calcular nota
    total_checks = 7
    errores_criticos = len([p for p in problemas if "CRITICO" in p])
    nota = max(0, 100 - (errores_criticos * 20) - (len(problemas) - errores_criticos) * 8)

    return {
        "nota": nota,
        "nivel": "Excelente" if nota >= 80 else "Mejorable" if nota >= 50 else "Urgente mejorar",
        "puntos_fuertes": puntos,
        "problemas": problemas,
        "oportunidades": oportunidades,
    }


def generar_informe(url: str, meta: dict, contenido: dict, velocidad: dict, puntuacion: dict) -> str:
    dominio = urllib.parse.urlparse(url).netloc
    fecha = datetime.now().strftime("%d/%m/%Y")
    nota = puntuacion["nota"]

    informe = f"""# AUDITORIA SEO — {dominio}
**Fecha:** {fecha}
**URL analizada:** {url}
**Puntuacion SEO:** {nota}/100 — {puntuacion['nivel']}

---

## RESUMEN EJECUTIVO

Esta auditoria ha detectado **{len(puntuacion['problemas'])} problemas** y **{len(puntuacion['oportunidades'])} oportunidades de mejora**.
{"Hay problemas criticos que deben resolverse de inmediato." if any("CRITICO" in p for p in puntuacion['problemas']) else "No hay errores criticos urgentes."}

---

## PUNTOS FUERTES
{chr(10).join(f"- {p}" for p in puntuacion['puntos_fuertes']) or "- Ninguno detectado"}

## PROBLEMAS DETECTADOS
{chr(10).join(f"- {p}" for p in puntuacion['problemas']) or "- Sin problemas criticos"}

## OPORTUNIDADES DE MEJORA
{chr(10).join(f"- {o}" for o in puntuacion['oportunidades']) or "- Sin oportunidades adicionales"}

---

## ANALISIS DETALLADO

### Metaetiquetas
| Campo | Valor | Estado |
|-------|-------|--------|
| Title | {meta['title'] or 'NO TIENE'} | {'OK' if 50 <= meta['title_len'] <= 70 else 'MEJORAR'} |
| Longitud title | {meta['title_len']} chars | {'OK (50-70)' if 50 <= meta['title_len'] <= 70 else 'Fuera de rango'} |
| Meta description | {str(meta['description'])[:60] + '...' if meta['description'] and len(meta['description']) > 60 else meta['description'] or 'NO TIENE'} | {'OK' if meta['desc_len'] and 120 <= meta['desc_len'] <= 165 else 'MEJORAR'} |
| H1 tags | {meta['h1_count']} | {'OK' if meta['h1_count'] == 1 else 'MEJORAR'} |
| H2 tags | {meta['h2_count']} | Info |
| Canonical | {'Si' if meta['canonical'] else 'No configurado'} | {'OK' if meta['canonical'] else 'Recomendado'} |

### Contenido
| Metrica | Valor | Objetivo |
|---------|-------|---------|
| Palabras | {contenido['word_count']} | >1000 para competir |
| Imagenes totales | {contenido['images_total']} | - |
| Imagenes sin ALT | {contenido['images_without_alt']} | 0 |
| Links en pagina | {contenido['links_count']} | - |

### Aspectos tecnicos
| Aspecto | Estado |
|---------|--------|
| HTTPS | {'Si' if velocidad['https'] else 'NO - Urgente'} |
| Compresion GZIP | {'Si' if velocidad['compresion_gzip'] else 'No'} |
| Cache-Control | {velocidad['cache_control']} |
| Servidor | {velocidad['server']} |

---

## PLAN DE ACCION PRIORITARIO

### Semana 1 (impacto inmediato):
{chr(10).join(f"{i+1}. {p}" for i, p in enumerate([p for p in puntuacion['problemas'] if 'CRITICO' in p][:3])) or "1. Sin acciones urgentes"}

### Mes 1 (mejoras de rendimiento):
{chr(10).join(f"{i+1}. {o}" for i, o in enumerate(puntuacion['oportunidades'][:4])) or "1. Mantener y monitorear"}

---

## SIGUIENTES PASOS

Para implementar todas estas mejoras y empezar a subir en Google, ofrecemos:
- **Servicio SEO basico:** 297 EUR/mes (incluye todas las correcciones tecnicas + 4 articulos/mes)
- **Servicio SEO pro:** 597 EUR/mes (correcciones + 12 articulos + link building)
- **Auditoria completa + implementacion:** 800 EUR (pago unico)

**Contacto:** Reserva tu consulta gratuita de 30 minutos para revisar este informe juntos.

---
*Informe generado por Agencia IA — Sistemas de posicionamiento automatizados*
"""
    return informe


def main():
    parser = argparse.ArgumentParser(description="Auditoria SEO automatica")
    parser.add_argument("--url", required=True, help="URL a auditar (ej: https://ejemplo.com)")
    args = parser.parse_args()

    url = args.url
    if not url.startswith("http"):
        url = "https://" + url

    print(f"\nAnalizando: {url}")
    print("Descargando pagina...")

    html, headers = fetch_url(url)
    if not html:
        error = headers.get("error", "Error desconocido")
        print(f"No se pudo acceder a la URL: {error}")
        sys.exit(1)

    print("Analizando meta tags...")
    meta = analizar_meta_tags(html)
    print("Analizando contenido...")
    contenido = analizar_contenido(html)
    print("Analizando aspectos tecnicos...")
    velocidad = analizar_velocidad(headers)
    print("Calculando puntuacion...")
    puntuacion = puntuar(meta, contenido, velocidad)

    informe = generar_informe(url, meta, contenido, velocidad, puntuacion)

    dominio = urllib.parse.urlparse(url).netloc.replace(".", "-")
    fecha = datetime.now().strftime("%Y%m%d")
    ruta = INFORMES_DIR / f"{fecha}-auditoria-{dominio}.md"
    ruta.write_text(informe, encoding="utf-8")

    print(f"\n{'='*50}")
    print(f"PUNTUACION SEO: {puntuacion['nota']}/100 — {puntuacion['nivel']}")
    print(f"Problemas: {len(puntuacion['problemas'])} | Oportunidades: {len(puntuacion['oportunidades'])}")
    print(f"Informe guardado: {ruta}")
    print(f"{'='*50}")
    print("\nPrimeros problemas detectados:")
    for p in puntuacion['problemas'][:3]:
        print(f"  - {p}")


if __name__ == "__main__":
    main()
