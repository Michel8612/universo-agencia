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

## Estado actual (2026-06-28)
- ✅ Web NEXIA LIVE https://nexia-ia-com.netlify.app + **formulario conectado al funnel n8n**
  (doble envío: formsubmit.co + webhook que `CLOUDFLARE-TUNNEL.ps1` autoactualiza).
- ✅ **Dashboard de control local** (`dashboard/`, Node sin deps) → `DASHBOARD.bat` = :3000.
  Lanza campañas, busca freelance, simula/envía tandas, ve estado y CRM.
- ✅ **Emisor de campañas** `enviar-campana.py` (SMTP, dry-run por defecto, tope/throttle/
  dedup/opt-out, lee `.md` y JSON). **7 emails reales enviados** (4 ES + 3 Miami).
- ✅ **Emails en frío más persuasivos** (prompts ES + USA reescritos).
- ✅ **Buscador freelance** con filtrado por relevancia (fit con NEXIA).
- ✅ **Seguridad**: secretos fuera del código (todo en `.env`). GitHub token y API key n8n
  ROTADOS. Ver memoria privada `security-creds-rotar`.
- ✅ **Servidor USA = repo git** (migrado); tiene `campana-usa.py`; **OpenClaw con Groq**.
- ✅ MCP empleos + perfil freelance + Spec Kit + Taíno Labs (`mundo-saas-factory/tainolabs/`).
- CRM local: ~53 leads (`mundo-agencia/crm/agencia.db`). Facturado: 0€.

## Nichos que trabajamos
- **España** (`campana-leads.py`): dentistas, restaurantes, fisioterapia, clínicas,
  peluquerías, belleza, gimnasios, abogados, inmobiliarias, talleres.
- **EE.UU.** (`campana-usa.py`, 98 ciudades de los 50 estados + DC): restaurantes, dentistas,
  abogados, clínicas, fisioterapia, gimnasios, inmobiliarias, talleres, veterinarios,
  peluquerías, belleza, fontaneros, electricistas, reformas, seguros.
- Criterio: negocios locales que necesitan web/chatbot/automatización (alto valor, decisor accesible).

## FleetHub-Laravel-Pro (otro proyecto del usuario, corre en USA :8080)
Plataforma de taller/flota + asistencia en carretera (sistema NFK). **Backend muy completo**:
63 migraciones (tablas), 49 modelos, 38 controladores, auth Sanctum + permisos spatie,
dominio rico (work orders, invoices, dispatch, emergency tickets, payments/webhooks, provider
network, audit logs). **Frontend casi inexistente** (3 vistas blade, 0 Livewire) → es API-first,
le falta la UI (web/app que consuma la API). No es repo git. Última mod: 2026-05-16.

## Plan para MAÑANA (acordado 2026-06-28, usuario aprobó puerto 8090)
1. **Fix CRM USA**: hacer `CRM_URL` configurable (env) + arrancar Flask NEXIA en **:8090**
   en USA (el 8080 lo tiene FleetHub). Sin esto, las campañas USA no guardan leads.
2. **Programar ambos países a las 8am** en USA: `campana-leads.py` (ES, quitar `--sin-email`
   para que prepare emails persuasivos) + `campana-usa.py` (EE.UU.).
3. **Conectar OpenClaw a Slack** (canal Slack del usuario) — pendiente: necesita token/OAuth de Slack.
4. **Workflow de filtrado de leads por IA**: la IA lee la bandeja (IMAP), detecta respuestas,
   clasifica/filtra, y dispara seguimiento (2º/3er email solo a quien NO respondió).
5. **n8n en Docker en la PC local** (más estable que Windows nativo, que se cae seguido).

## Claves que van en .env / llm-config.json (NUNCA a git)
GROQ_API_KEY · SLACK_WEBHOOK_URL · TELEGRAM_BOT_TOKEN · TELEGRAM_SALA_CHAT_ID · N8N_API_KEY · MAIL_PASSWORD

### Mapa de las 3 keys de Groq (valores solo en archivos gitignored, nunca aquí)
1. **Herramientas de ventas** → `mundo-ventas/herramientas/llm-config.json` (`groq_key`).
   La usan las 5 tools vía `llm.py` (buscar-trabajos, diagnostico-web, scraper-leads,
   campana-leads, generar-propuesta). Verificada válida 2026-06-28.
2. **OpenClaw (PC USA)** → ✅ configurada 2026-06-28 en `~\.openclaw\openclaw.json`
   (`models.providers.groq`). Gateway reiniciado. Verificada válida.
3. **Bot de leads Telegram** → `mundo-agencia/herramientas/bot-leads-config.json` (`groq_key`).
   La usa @Jarvistrading2026_bot. Verificada válida 2026-06-28.
