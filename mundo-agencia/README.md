# 📂 mundo-agencia — Índice

Punto de entrada. Al conectarte desde la PC, empieza por el **HANDOFF**.

## 🟢 Empieza aquí
- **[memoria/CAMBIOS-2026-06-25.md](memoria/CAMBIOS-2026-06-25.md)** — HANDOFF de la última
  sesión: arquitectura, qué se hizo, errores y soluciones, y pendientes. **Léelo primero.**
- [memoria/estado-fase.md](memoria/estado-fase.md) — estado general de la agencia.

## 🛠️ Guías de configuración (lo que toca hacer en la PC)
- **[OPENCLAW-GROQ.md](OPENCLAW-GROQ.md)** — conectar Groq (IA rápida/gratis) en OpenClaw
  y en las herramientas de ventas.
- **[SLACK-TELEGRAM.md](SLACK-TELEGRAM.md)** — avisos de leads en Slack + botón del bot en la web.
- **[TELEGRAM-SALA-VIP.md](TELEGRAM-SALA-VIP.md)** — sala privada de Telegram solo para leads
  calentados (enlaces de un solo uso).
- **[SPECKIT.md](SPECKIT.md)** — Spec Kit (desarrollo guiado por specs) + `setup-speckit.sh`
  y la constitución de NEXIA.

## ✅ Checklist rápido en la PC
1. [ ] Netlify desbloqueado → web live (ver HANDOFF §2).
2. [ ] `cp .env.example .env` y rellenar: `GROQ_API_KEY`, `SLACK_WEBHOOK_URL`,
   `TELEGRAM_BOT_TOKEN`, `TELEGRAM_SALA_CHAT_ID`.
3. [ ] Crear grupo privado Telegram + bot admin (sala VIP).
4. [ ] `bash mundo-agencia/setup-speckit.sh` (activar Spec Kit).
5. [ ] Correr scraper/buscador de leads (la red de la PC sí llega a Freelancer/OSM).
