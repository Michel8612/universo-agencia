# Estado Actual de la Agencia — NEXIA

**Última actualización:** 2026-06-25

---

## 🆕 SESIÓN 2026-06-25 — RESUMEN COMPLETO (todo en `main`)

> Handoff detallado: `mundo-agencia/memoria/CAMBIOS-2026-06-25.md`
> Índice de docs: `mundo-agencia/README.md`

### Hecho y en producción
- **Web NEXIA LIVE** → https://nexia-ia-com.netlify.app (se desbloqueó haciendo el repo
  **público**; el plan gratis de Netlify bloqueaba deploys de repos privados).
  Incluye: botón WhatsApp (+53 5665 9464), botones Telegram → @Jarvistrading2026_bot,
  bloque "qué analizamos", línea de confianza, barra CTA móvil.
- **Next.js 14.2.3 → 14.2.35** (cierra CVE).

### Hecho en el repo (a configurar/usar en la PC)
- **Groq + fallback Ollama**: `mundo-ventas/herramientas/llm.py` usado por las 5
  herramientas. Activar con `GROQ_API_KEY` en `.env`.
- **Slack** avisos de leads: `herramientas/notificar.py` (necesita `SLACK_WEBHOOK_URL`).
- **Sala VIP Telegram** (leads calentados): `herramientas/telegram_sala.py` + guía
  `TELEGRAM-SALA-VIP.md` (necesita `TELEGRAM_BOT_TOKEN` y `TELEGRAM_SALA_CHAT_ID`).
- **MCP de empleos** (`mundo-ventas/mcp-empleos/`): herramientas `buscar_empleos`
  (Freelancer) y `buscar_empleos_remoto` (Remotive) para Claude Desktop.
- **Spec Kit** (SDD): `setup-speckit.sh` + `SPECKIT.md` + constitución NEXIA.
- **Perfil freelance** ES/EN: `mundo-ventas/PERFIL-FREELANCE.md` (Malt/Upwork/Freelancer/Workana).
- **Taíno Labs RESCATADO**: `mundo-saas-factory/tainolabs/` (landing de respuesta de
  leads que solo existía como HTML suelto en Netlify; ahora versionada + plan en su README).
- **Puente de continuidad**: `MCP-PUENTE-PC.md` (MCP filesystem para `D:\Proyectos claude`
  en Claude Desktop + protocolo Git como nexo nube↔PC).

### ⚠️ Pendiente de TI (en la PC)
1. `cp .env.example .env` y rellenar: `GROQ_API_KEY`, `SLACK_WEBHOOK_URL`,
   `TELEGRAM_BOT_TOKEN`, `TELEGRAM_SALA_CHAT_ID`.
2. Configurar los MCP en Claude Desktop (filesystem + empleos) — ver `MCP-PUENTE-PC.md`.
3. Crear el grupo privado Telegram (sala VIP) y conectar el disparador de "lead calentado".
4. `bash mundo-agencia/setup-speckit.sh`.
5. Correr scraper/buscador de empleos (la red de la PC sí llega a Freelancer/OSM; la nube no).
6. Decidir Taíno Labs: modelo (SaaS/servicio), precio, y pasar su deploy a Git.

### Notas de entorno (importante)
- La sesión de Claude en la NUBE no ve el disco de la PC ni el sistema local (n8n/Ollama/bot).
  El nexo es **Git**: push desde la PC → pull en la nube. La memoria (este archivo) viaja en el repo.
- Red de la nube bloquea: Freelancer, OpenStreetMap, Malt, netlify.app → esas se corren en la PC.

---

## ✅ INFRAESTRUCTURA OPERATIVA (verificada funcionando)

### Servicios locales (auto-arranque + watchdog cada 5 min)
- ✅ **n8n** → http://127.0.0.1:5678 (Task Scheduler `n8n-agencia`, se reinicia solo)
- ✅ **Flask API** → http://127.0.0.1:8080 (CRM en SQLite)
- ✅ **Ollama** → http://localhost:11434 (qwen2.5:14b) — toda la IA interna, gratis
- Watchdog: `C:\Users\Romer\AppData\Local\n8n-watchdog.ps1` mantiene ambos vivos

### Funnel de leads — VERIFICADO end-to-end (workflow cKCMyzGZiZLM1zPk)
Webhook → Validar → Guardar CRM → IA analiza (Ollama) → Email prospecto + Email director → Respuesta web.
- Email por SMTP (teamorionglobal@gmail.com + App Password). Cred n8n id b85GBYExeehQdazK.
- Emails salen personalizados y bien formados (probado exec 51).

### Máquina de ventas por auditoría (NUEVO 2026-06-24)
- `mundo-ventas/herramientas/scraper-leads.py` — 49 nichos, multi-país, OSM gratis
- `mundo-ventas/herramientas/diagnostico-web.py` — audita web → problemas → servicios+precio → pitch IA
- `mundo-ventas/catalogo-servicios.json` — 50 servicios con precios y triggers de diagnóstico

### Web & datos
- Web NEXIA → https://nexia-ia-com.netlify.app (rediseñada: programa fundador, mockups, animaciones, legal completo)
- **Auto-deploy Netlify↔GitHub ACTIVO**: cada push a `main` (repo Michel8612/universo-agencia) se publica solo. Build: base=mundo-ventas/web-nexia, command=npm run build, publish=out. NO hace falta deploy manual.
- **Google Search Console VERIFICADO** (cuenta teamorionglobal@gmail.com, etiqueta HTML en layout.tsx) + sitemap.xml enviado
- Supabase DB → tahzdjevzxppeqiajvnz.supabase.co (migración pospuesta, seguimos en SQLite)
- GitHub repo real → https://github.com/Michel8612/universo-agencia

### Máquinas de captación activas
- `buscar-trabajos.py` — proyectos de Freelancer.com + propuestas IA (en idioma del proyecto)
- `campana-leads.py` — motor multi-nicho/ciudad → CRM (21 leads ya, 10+ con email)
- Task Scheduler `nexia-campana-leads` → corre cada día 08:00, llena el CRM solo
- PENDIENTE de Michel: enviar primeros emails en tandas 20-40/día (ver CHECKLIST-LEGAL.md)

---

## 🎯 ROADMAP — ORDEN DE PRIORIDAD (decidido por Michel 2026-06-24)

**META GLOBAL: EMPEZAR A FACTURAR YA. Dinero que entre, dinero que hagamos.**

### P1 — Página de ventas perfecta
- Quitar casos de éxito inventados (Clínica Dental, Tienda Moda, etc. — son falsos)
- Enfoque **PROGRAMA FUNDADOR**: "Buscamos 3 clientes fundadores con 50% dto a cambio de ser nuestros primeros casos de éxito"
- Cuando se cumplan los fundadores → pasar a trabajos reales con precios reales
- Conectar el formulario al funnel de n8n (requiere túnel público — pendiente)
- Precios coherentes (alinear con catalogo-servicios.json)

### P2 — Buscador de trabajos freelance
- Freelancer.com tiene API oficial pública (legal) → traer trabajos por skills
- Redactor de propuestas con Ollama → usuario revisa y envía manual
- NO auto-aplicar (viola ToS, banea cuentas). NO crear cuentas (las hace Michel)
- Fiverr: no se aplica, se crean gigs optimizados

### P3 — Cazar leads (pipeline real)
- Correr scraper + diagnóstico sobre nichos/ciudades concretos
- Generar emails y enviarlos por el funnel

---

## 🔭 VISIÓN FASE 2 — al llegar el PRIMER LEAD/CLIENTE (decidido por Michel 2026-06-24)

Cuando entre el primer ingreso, migramos TODO a un VPS y automatizamos de punta a punta:
- **VPS** con todo corriendo 24/7 sin descanso (n8n, Flask, scrapers, campañas, Ollama o API)
- **Auto-gestión total**: encuentra leads, diagnostica, redacta, envía, responde y hace seguimiento solo
- **API de pago activada** (Claude/OpenRouter) para calidad y velocidad superiores a Ollama local
- **Hermes Agent** en el VPS: un agente que orquesta y gestiona toda la operación literalmente
- **Chatbot propio de NEXIA** (para la web y atención interna)
- **Ampliar nichos y sub-nichos** + campañas mucho más amplias (multi-país)
- **Aplicar a trabajos freelance vía API en TODAS las plataformas que lo permitan** (donde exista API key / oportunidad legal). Nota honesta: la mayoría permiten BUSCAR vía API pero NO auto-aplicar (viola ToS, banea). Evaluar caso por caso; algunas con plan de pago/partner podrían permitir pujar programático.

Regla de idioma (ya implementada en buscar-trabajos.py): aunque trabajemos en español, cada propuesta se escribe 100% en el idioma del proyecto (detección automática + imposición a la IA), sin mezclas.

## FASE: PRE-CLIENTE (0€ facturado)

**Regla de modelos:** TODO con Ollama local (gratis). Claude API de pago SOLO cuando haya primer ingreso real.

## Registro de Ingresos
| Fecha | Cliente | Servicio | Monto | Estado |
|-------|---------|---------|-------|--------|
| - | - | - | 0€ | - |

**Objetivo:** primer proyecto pagado (cualquier monto) para validar el sistema.
