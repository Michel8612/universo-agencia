# Sesión 2026-06-25 — Migración a servidor USA + leads reales

## Logros clave
- **Servidor 24/7 montado en USA** (desktop-c1v13sm, Tailscale 100.105.141.108, user owner, SSH con llave `C:\Users\Romer\.ssh\nexia_usa`). Ver [[us-server-access]].
- **Bots vivos 24/7 en USA**: @Rebeeka_bot (mando) + @Jarvistrading2026_bot (leads, conversacional comercial con guardrails). Watchdog cada 5 min + campaña diaria 08:00.
- **Groq en la nube** (3 keys repartidas: herramientas / OpenClaw / bot-leads). Fix Cloudflare 403 = mandar User-Agent de navegador. El servidor de 4GB solo hace llamada HTTP (no corre LLM local).
- **Scraper arreglado para USA**: 406 de Overpass = UA de navegador + mirrors reordenados. Bug de enriquecimiento (rutas con `\` rotas) arreglado → 6x más emails. Filtro anti-plataformas (menufy/getbento/atom...).
- **Leads reales de Miami**: 19 restaurantes, 3 con email real + mensajes de outreach listos (`mundo-ventas/outreach/miami-emails.json`): Giardino (info@giardinosalads.com), Fritz & Franz (Miamibierhaus@aol.com), Joey's (events@joeyswynwood.com).
- **Conectores Claude Desktop restaurados**: filesystem, memory, sequential-thinking, nexia-empleos + n8n. Reiniciar Claude Desktop para activar.

## Modelo operativo (decidido)
- **Todo corre en el servidor USA** (IP USA, conexión buena, sin bloqueos OSM). Cuba = solo control vía SSH/Telegram.
- **Vendemos a USA primero** (luego Europa), por huso horario y mercado.
- Continuidad PC↔nube↔móvil = **Git** (no MCP). Regla: leer estado-fase al empezar, commit+push al terminar.

## Actualización — sesión nube 2026-06-26
- ✅ **Repo reconciliado**: el merge dejó imports rotos en las herramientas
  (`buscar-trabajos` importaba `backend_activo`, ya inexistente; `generar-propuesta`
  llamaba con kwargs viejos). Alineadas las 5 a `llm.generar(prompt, max_tokens=...)`.
  Verificado que importan limpio. (`llm-config.json` confirmado fuera de git.)
- ✅ **Outreach Miami v2** listo: `mundo-ventas/outreach/miami-outreach-v2.md`. OJO: de los
  6, solo 3 emails son del negocio real (Giardino, Fritz & Franz, Joey's). Los otros 3 van
  a plataformas (menufy/getbento/atom) → NO enviar. Mensajes reescritos + opt-out CAN-SPAM.

## Pendiente / próximo
- Enviar los 3 emails de Miami. Cazar más ciudades USA (Orlando, Tampa) para juntar 20-30 leads con email.
- Reconciliar repo: origin/main tiene trabajo de la sesión nube (WhatsApp btn +53 5665 9464, Next.js 14.2.35 seguridad, MCP empleos, perfiles freelance, Spec Kit). Su llm.py NO tiene el fix User-Agent (daría 403).
- Spec Kit (github/spec-kit v0.11.8, CLI `specify`): instalar en PC con `bash mundo-agencia/setup-speckit.sh`.
- OpenClaw (key #2 Groq) cuando se monte.
