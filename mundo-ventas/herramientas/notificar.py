#!/usr/bin/env python3
"""
NEXIA — Notificaciones (Slack) para avisos internos de leads.

Best-effort: si no hay SLACK_WEBHOOK_URL configurado, no hace nada y no rompe.
Crea el webhook en: https://api.slack.com/messaging/webhooks  (Incoming Webhook)
y pega la URL en .env como SLACK_WEBHOOK_URL.

Uso:
  from notificar import slack, aviso_lead
  slack("Texto libre a tu canal")
  aviso_lead("Pizzeria Bella", score=9, servicio="Landing+Chatbot", extra="Valencia, sin web")
"""
import os, json, urllib.request

SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL", "").strip()


def slack(texto):
    """Envia un mensaje al canal de Slack. Devuelve True/False. Nunca lanza."""
    if not SLACK_WEBHOOK_URL:
        return False
    try:
        body = json.dumps({"text": texto}).encode()
        req = urllib.request.Request(
            SLACK_WEBHOOK_URL, data=body, headers={"Content-Type": "application/json"}
        )
        urllib.request.urlopen(req, timeout=8)
        return True
    except Exception:
        return False


def aviso_lead(nombre, score=None, servicio="", extra=""):
    """Aviso formateado de lead nuevo para el canal interno."""
    estrellas = ""
    if isinstance(score, (int, float)):
        estrellas = " " + "⭐" * int(round(min(max(score, 0), 10) / 2))
    partes = [f"🎯 *Nuevo lead:* {nombre}{estrellas}"]
    if servicio:
        partes.append(f"Servicio sugerido: {servicio}")
    if score is not None:
        partes.append(f"Score: {score}/10")
    if extra:
        partes.append(extra)
    return slack("\n".join(partes))
