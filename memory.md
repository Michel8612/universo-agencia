# 🧠 MEMORY — NEXIA (leer al arrancar cualquier sesión)

> Archivo de memoria maestro, versionado en Git. **Protocolo:** al EMPEZAR una sesión
> (PC, servidor o nube) leer esto; al TERMINAR, actualizarlo + `git add -A && git commit && git push`.
> Detalle por sesión en `mundo-agencia/memoria/` (estado-fase.md, SESION-USA-0625.md, CAMBIOS-*).

## Qué somos
Agencia de IA (NEXIA). Rol principal: **auditar la web de un negocio → detectar problemas →
mapear a servicios con precio → pitch**. Vendemos webs, chatbots y automatización.

## Arquitectura / dónde corre todo
- **Servidor 24/7 en USA** (desktop-c1v13sm, Tailscale 100.105.141.108, SSH `~/.ssh/nexia_usa`):
  corre n8n, scraper, bots, campañas. IP USA = sin bloqueos OSM.
- **Bots Telegram 24/7**: @Rebeeka_bot (mando) + @Jarvistrading2026_bot (leads).
- **IA**: Groq (nube, gratis, Llama 3.3 70B) vía `herramientas/llm.py` + `llm-config.json`
  (NO en git). Fallback Ollama. Fix Cloudflare 403 = User-Agent de navegador.
- **Nube (esta sesión de Claude)**: NO ve el disco de la PC ni el sistema local. Nexo = **Git**.
  La red de la nube bloquea Freelancer/OSM/Malt/netlify.app → esas tareas van en el servidor.
- Carpeta física del repo: `D:\Proyectos claude` (= repo Michel8612/universo-agencia).

## Estado actual (2026-06-26)
- ✅ Web NEXIA LIVE: https://nexia-ia-com.netlify.app (repo público para desbloquear Netlify).
- ✅ Taíno Labs (landing respuesta de leads) rescatada → `mundo-saas-factory/tainolabs/`.
- ✅ Herramientas reconciliadas con `llm.py` nuevo (5 importan limpio).
- ✅ Leads reales Miami: 3 emails listos en `mundo-ventas/outreach/miami-outreach-v2.md`
  (OJO: 3 de 6 eran plataformas, no enviar).
- ✅ **Campaña USA** lista: `herramientas/campana-usa.py` (98 ciudades × 15 nichos = 1470
  combos/vuelta, bucle infinito, anti-bloqueo OSM, análisis web completo). Lanzar con
  `mundo-ventas/INICIAR-CAMPANA-USA.bat`. Ver `mundo-ventas/CAMPANA-USA.md`.
- ✅ MCP de empleos (`mundo-ventas/mcp-empleos/`) + perfil freelance + Spec Kit + puente PC.

## Pendiente / próximo
1. Lanzar la campaña USA en el servidor (`INICIAR-CAMPANA-USA.bat`) y dejarla corriendo.
2. Enviar los 3 emails de Miami (poner nombre + dirección postal CAN-SPAM).
3. Buscar y aplicar a trabajos en Freelancer (`buscar-trabajos.py`, ver CAMPANA-USA.md).
4. Taíno Labs P1: página de gracias + aviso de leads + decidir precio/modelo.

## Claves que van en .env / llm-config.json (NUNCA a git)
GROQ_API_KEY · SLACK_WEBHOOK_URL · TELEGRAM_BOT_TOKEN · TELEGRAM_SALA_CHAT_ID
