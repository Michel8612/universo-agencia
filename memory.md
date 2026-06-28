# 🧠 MEMORY — NEXIA (leer al arrancar cualquier sesión)

> Archivo de memoria maestro, versionado en Git. **Protocolo:** al EMPEZAR una sesión
> (PC, servidor o nube) leer esto; al TERMINAR, actualizarlo + `git add -A && git commit && git push`.
> Detalle por sesión en `mundo-agencia/memoria/` (estado-fase.md, SESION-USA-0625.md, CAMBIOS-*).

## Qué somos
Agencia de IA (NEXIA). Rol principal: **auditar la web de un negocio → detectar problemas →
mapear a servicios con precio → pitch**. Vendemos webs, chatbots y automatización.

## Arquitectura / dónde corre todo
- **Servidor 24/7 en USA** (desktop-c1v13sm, Tailscale 100.105.141.108, user `owner`,
  SSH `~/.ssh/nexia_usa`, shell remoto = PowerShell): corre **bots Telegram, Ollama,
  scraper y campañas**. IP USA = sin bloqueos OSM. **NO corre n8n.**
- **n8n corre SOLO en la PC local** (localhost:5678), no en USA. El funnel y el túnel
  Cloudflare (`CLOUDFLARE-TUNNEL.ps1`) trabajan contra la PC local.
- **USA `C:\nexia` ya es repo git** (2026-06-28): se migró de copia manual a clon
  (`git reset --hard origin/main`, conserva configs/`agencia.db` no rastreados).
  A futuro: `git pull` en USA sincroniza. Ya tiene `campana-usa.py`. OpenClaw usa Groq.
- ⚠️ **Conflicto de puerto en USA**: el 8080 lo ocupa otro proyecto (FleetHub-Laravel),
  así que el Flask CRM de NEXIA NO corre allí → las campañas USA aún no guardan leads.
  Pendiente: CRM_URL configurable + arrancar Flask NEXIA en puerto libre (p.ej. 8090).
- **Bots Telegram 24/7** (en USA): @Rebeeka_bot (mando) + @Jarvistrading2026_bot (leads).
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
GROQ_API_KEY · SLACK_WEBHOOK_URL · TELEGRAM_BOT_TOKEN · TELEGRAM_SALA_CHAT_ID · N8N_API_KEY · MAIL_PASSWORD

### Mapa de las 3 keys de Groq (valores solo en archivos gitignored, nunca aquí)
1. **Herramientas de ventas** → `mundo-ventas/herramientas/llm-config.json` (`groq_key`).
   La usan las 5 tools vía `llm.py` (buscar-trabajos, diagnostico-web, scraper-leads,
   campana-leads, generar-propuesta). Verificada válida 2026-06-28.
2. **OpenClaw (PC USA)** → pendiente de montar; aún sin colocar en archivo.
3. **Bot de leads Telegram** → `mundo-agencia/herramientas/bot-leads-config.json` (`groq_key`).
   La usa @Jarvistrading2026_bot. Verificada válida 2026-06-28.
