# Estado Actual de la Agencia — NEXIA

**Última actualización:** 2026-06-25

---

## 🆕 SESIÓN 2026-06-25 (rama claude/focused-ride-801h71)

- **Groq integrado en las herramientas de ventas** (con fallback a Ollama):
  nuevo `mundo-ventas/herramientas/llm.py`. Si hay `GROQ_API_KEY` usa Groq
  (rápido, gratis, funciona en cualquier máquina/VPS); si no, cae a Ollama local.
  Refactorizados: buscar-trabajos, diagnostico-web, scraper-leads, campana-leads,
  generar-propuesta. `.env.example` ampliado con `GROQ_*` / `OLLAMA_*`.
- **Guía OpenClaw + Groq**: `mundo-agencia/OPENCLAW-GROQ.md` (pasos para conectar
  Groq en OpenClaw en la PC de EE.UU. + en las herramientas Python).
- **Landing optimizada para conversión** (`web-nexia/src/app/page.tsx`):
  bloque "qué incluye tu diagnóstico", línea de confianza en el hero
  (sin tarjeta / 24h / sin permanencia), botón flotante de WhatsApp (configurable
  con la constante `WHATSAPP`) y barra CTA fija en móvil. Build verificado OK.
- **Limpieza repo**: des-trackeados `web-nexia/.next` y `web-nexia/out` (artefactos
  de build que estaban commiteados por error; Netlify ya hace `npm run build`).
- ⚠️ PENDIENTE de TI: poner número en la constante `WHATSAPP` de la landing;
  crear la `GROQ_API_KEY` en https://console.groq.com/keys y configurarla en
  OpenClaw + en `.env`. La caza de leads/trabajos en vivo se corre en tu PC/VPS
  (la red del entorno cloud de Claude bloquea Freelancer/OSM).

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

### Web & datos (de sesiones previas — verificar al retomar)
- Web NEXIA → https://nexia-ia-com.netlify.app (REVISAR: casos de éxito son inventados)
- Supabase DB → tahzdjevzxppeqiajvnz.supabase.co (migración pospuesta, seguimos en SQLite)
- GitHub → https://github.com/Michel8612/nexia-agencia-ia

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
