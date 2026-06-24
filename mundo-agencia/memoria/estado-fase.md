# Estado Actual de la Agencia — NEXIA

**Última actualización:** 2026-06-24

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

## FASE: PRE-CLIENTE (0€ facturado)

**Regla de modelos:** TODO con Ollama local (gratis). Claude API de pago SOLO cuando haya primer ingreso real.

## Registro de Ingresos
| Fecha | Cliente | Servicio | Monto | Estado |
|-------|---------|---------|-------|--------|
| - | - | - | 0€ | - |

**Objetivo:** primer proyecto pagado (cualquier monto) para validar el sistema.
