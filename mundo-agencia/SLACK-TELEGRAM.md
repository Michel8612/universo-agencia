# Slack (avisos de leads) + Telegram (bot en la web)

## Telegram — botón directo a tu bot

Ya está montado en la web. Solo falta poner el @username de tu bot.

1. Abre `mundo-ventas/web-nexia/src/app/page.tsx`.
2. Arriba, pon tu bot en la constante (sin la "@"):
   ```ts
   const TELEGRAM_BOT = "TuBotUsername";
   ```
3. Listo. Aparecen automáticamente:
   - Un **botón flotante azul de Telegram** (encima del de WhatsApp).
   - Un botón **"Habla con nuestro asistente en Telegram"** en la sección de contacto.
   - Ambos abren `https://t.me/TuBotUsername` → chat 1-a-1 directo con tu bot.

> Si `TELEGRAM_BOT` queda vacío, los botones no se muestran (no rompe nada).
> El bot tiene que estar ya creado en @BotFather y configurado (tú dijiste que lo está).

## Slack — avisos internos cuando entra un lead

Montado en las herramientas Python (best-effort: si no hay webhook, no pasa nada).

1. Crea un **Incoming Webhook** en https://api.slack.com/messaging/webhooks
   (elige el canal donde quieres los avisos, ej. `#leads`).
2. Copia la URL (`https://hooks.slack.com/services/...`) a tu `.env`:
   ```
   SLACK_WEBHOOK_URL=https://hooks.slack.com/services/xxx/yyy/zzz
   ```
3. A partir de ahí, cuando el scraper guarde un lead en el CRM, te llega un aviso a Slack:
   `🎯 Nuevo lead: Pizzeria Bella ⭐⭐⭐⭐ · Servicio: Landing+Chatbot · score:9/10`

**Helper reutilizable:** `mundo-ventas/herramientas/notificar.py`
```python
from notificar import slack, aviso_lead
slack("mensaje libre")
aviso_lead("Negocio X", score=8, servicio="Chatbot", extra="Madrid, web antigua")
```

### Conectar Slack también al funnel de n8n (web → lead)
El formulario de la web entra por n8n. Para avisar a Slack desde ahí:
- En el workflow del funnel, añade un nodo **HTTP Request** (POST) a tu `SLACK_WEBHOOK_URL`
  con body JSON `{"text": "🎯 Nuevo lead web: {{nombre}} - {{email}}"}`.
- O usa el nodo nativo **Slack** de n8n con el webhook/credencial.

> Nota: NO metas el webhook de Slack en el código de la web (es estático y publicaría
> la URL). Los avisos van por el lado servidor: n8n o las herramientas Python.
