# NEXIA — Prompt Maestro de la Agencia IA
**Actualizado:** 2026-06-24 | **Estado:** Pre-cliente (0€ facturado, primer cliente en proceso)

> Leer este archivo al inicio de CADA sesión. Contiene todo el contexto necesario para no repetir trabajo ni gastar tokens en redescubrimiento.

## 🎯 ROADMAP ACTUAL (prioridad decidida 2026-06-24) — META: FACTURAR YA
1. **Página de ventas perfecta** — quitar casos falsos, enfoque PROGRAMA FUNDADOR (3 clientes fundadores 50% dto → primeros casos reales), conectar formulario a n8n. Cuando se cumplan fundadores → precios reales.
2. **Buscador de trabajos freelance** — Freelancer.com API (legal) + propuestas con Ollama. NO auto-aplicar (banea), NO crear cuentas (las hace Michel). Fiverr = crear gigs, no aplicar.
3. **Cazar leads pipeline real** — scraper-leads + diagnostico-web sobre nichos/ciudades concretos.
Ver detalle en `mundo-agencia/memoria/estado-fase.md`.

---

## 1. QUIÉN SOY Y QUÉ ESTOY CONSTRUYENDO

Soy Michel, emprendedor cubano construyendo **NEXIA** — una agencia de IA profesional que resuelve problemas reales a empresas. Trabajo desde Windows 10 (Ryzen 7 7730U, 40GB RAM, AMD Radeon 760M, sin GPU dedicada).

**Visión:** Una agencia que usa IA para entregar servicios de desarrollo, automatización, marketing y multimedia — con un equipo de sub-agentes especializados que trabajan en paralelo, cada uno con el modelo correcto para su tarea.

**Situación actual:** Sin facturación activa. Toda la infraestructura está construida y lista. El objetivo inmediato es conseguir el primer cliente (500-2,000€) para activar el stack de pago.

**Regla de modelos HASTA el primer cliente:**
- TODO desarrollo interno → **Ollama local** (gratis, qwen2.5:14b)
- Claude API (Sonnet/Haiku/Opus) → SOLO cuando haya ingreso real
- Esta regla puede cambiarse editando este archivo cuando llegue el primer pago

---

## 2. STACK TÉCNICO — LO QUE ESTÁ INSTALADO Y FUNCIONANDO

### Software base (NO reinstalar, ya existe)
| Herramienta | Versión | Ruta/Puerto |
|-------------|---------|-------------|
| **Node.js** | v22.16.0 | `C:\Program Files\nodejs\node.exe` — **YA INSTALADO, NO REINSTALAR** |
| **n8n** | 2.22.6 | `C:\Users\Romer\AppData\Roaming\npm\node_modules\n8n` — auto-start al boot |
| **Python** | 3.12.9 | en PATH |
| **Ollama** | 0.30.10 | http://localhost:11434 — auto-start al boot |
| **FFmpeg** | master | `C:\ffmpeg\ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe` |
| **Flask** | 3.1.3 | pip — para API agencia |
| **insightface** | 1.0.1 | pip — face swap |
| **onnxruntime-directml** | 1.24.4 | pip — GPU AMD via DirectML |
| **rclone** | 1.68.2 | `C:\Users\Romer\AppData\Local\rclone\` |

### Modelos IA locales (Ollama)
- `qwen2.5:14b` — modelo principal (2.6 t/s CPU)
- `qwen2.5-coder:7b` — código

### Servicios en ejecución (auto-arrancan al boot)
| Servicio | URL | Estado |
|---------|-----|--------|
| n8n | http://127.0.0.1:5678 | ✅ Activo (Task Scheduler + watchdog cada 5 min) |
| API Agencia (Flask) | http://127.0.0.1:8080 | ✅ Activo (VBS en Startup, 20s delay) |
| Ollama | http://localhost:11434 | ✅ Activo |
| Tailscale | IP: 100.99.251.46 | ✅ Activo (acceso remoto VPN) |
| **localtunnel** | ⚠️ TEMPORAL — cambia en cada reinicio | Expone n8n al exterior. Relanzar con `LANZAR-TUNEL.bat` |

### Túnel público actual (TEMPORAL)
> ⚠️ Esta URL cambia cada vez que se reinicia el túnel. Después de relanzar, actualizar `WEBHOOK_URL` en `mundo-ventas/web-nexia/src/app/page.tsx` y reconstruir con `BUILD-NEXIA.bat`.

| Concepto | Valor |
|---------|-------|
| **URL túnel** | `https://mighty-hounds-yell.loca.lt` |
| **Webhook NEXIA** | `https://mighty-hounds-yell.loca.lt/webhook/lead-nexia` |
| **Cómo relanzar** | Doble clic en `D:\Proyectos claude\LANZAR-TUNEL.bat` |
| **URL queda en** | `D:\Proyectos claude\tunnel-url.txt` |
| **Herramienta** | `localtunnel` (npm) — instalado globalmente |

---

## 3. N8N — INSTALACIÓN Y USO

### Cómo está instalado
```
npm install -g n8n   (instalado globalmente, versión 2.22.6)
```
n8n arranca automáticamente al encender el PC via un archivo `.vbs` en la carpeta Startup de Windows con 20 segundos de delay.

**IMPORTANTE para n8n:** Node.js v22 ya está instalado en `C:\Program Files\nodejs\`. Si algún agente de Cowork intenta instalar Node.js nuevamente, debe parar — usar el existente.

### Acceso
- **UI:** http://localhost:5678
- **API REST:** http://localhost:5678/api/v1/
- **Webhook agencia:** http://localhost:5678/webhook/agencia
- **Webhook social:** http://localhost:5678/webhook/publish-social

### Workflows activos en n8n
1. `Social Media - Post cada 20 min (Ollama)` — publica contenido automático en redes
2. `SEO - Generador Artículos Semanal` — artículos SEO semanales
3. `UNIVERSO HUB — Orquestador Central` — webhook que recibe tareas y las distribuye
4. `NEXIA — Lead Automático Completo` [id:cKCMyzGZiZLM1zPk] — ✅ ACTIVO y verificado. Webhook local: `http://127.0.0.1:5678/webhook/lead-nexia`. Webhook público (túnel): `https://mighty-hounds-yell.loca.lt/webhook/lead-nexia`. E2E confirmado: ejecución ID 44, status success, 2026-06-23.

### Cómo llamar al hub n8n
```json
POST http://localhost:5678/webhook/agencia
{"tipo": "contenido", "subtipo": "post_linkedin", "tema": "IA para pymes"}
```

### Lecciones críticas de n8n (ya aprendidas, no repetir errores)
- n8n resuelve `localhost` como IPv6 `::1` — usar siempre `127.0.0.1` en HTTP nodes de n8n
- **Webhook envuelve el payload en `body`** → dentro del workflow usar `$json.body.Campo` (NO `$json.Campo`). El validador IF, el nodo CRM y el parser deben leer `.body.X`
- **bodyParameters solo evalúan expresiones si el valor empieza con `=`** → un `{{ }}` sin `=` delante se manda como TEXTO LITERAL. El prompt de IA y todos los campos con `{{ }}` DEBEN empezar con `=`
- n8n agrega wrapper `{body: {...}}` al payload → en Flask: `data = raw.get("body", raw)`
- Switch node v3 de n8n es buggy → usar siempre v1
- `n8n-nodes-base.sqlite` NO existe en n8n v2.22.6 → usar `httpRequest` a Flask API (127.0.0.1:8080) para guardar datos
- **Email: usar nodo `emailSend` (SMTP), NO `gmail` (OAuth2)**. Credencial SMTP "Gmail SMTP - Nexia" (id b85GBYExeehQdazK): smtp.gmail.com:465 SSL, teamorionglobal@gmail.com + App Password
- **Endpoint CRM correcto: `http://127.0.0.1:8080/crm/cliente`** (campos: nombre, contacto, mundo, estado, presupuesto, notas). NO existe `/api/leads`
- VBS Startup: usar rutas absolutas de node.exe, no depender del PATH
- **DOS Python instalados**: el bueno es `C:\Program Files\Python312\python.exe` (tiene Flask). El stub `WindowsApps\python.exe` NO tiene nada. SIEMPRE usar ruta completa al lanzar Flask
- **Watchdog NEXIA**: Task Scheduler `n8n-agencia` corre cada 5 min + al logon. Script: `C:\Users\Romer\AppData\Local\n8n-watchdog.ps1` — mantiene vivos n8n (5678) Y Flask (8080). Si cualquiera cae, se reinicia solo en ≤5 min
- **Funnel de leads VERIFICADO funcionando** (exec 49): Webhook→Validar→CRM→IA(Ollama)→Parser→Email prospecto+director→Respuesta. Email con valores reales personalizados

---

## 4. MCP SERVERS Y PLUGINS CONECTADOS A CLAUDE

### MCP Servers (en `C:\Users\Romer\AppData\Roaming\Claude\claude_desktop_config.json`)
| Servidor | Función |
|---------|---------|
| `n8n-agencia` | Disparar workflows n8n, publicar en redes |
| `filesystem` | Acceso directo a `D:\Proyectos claude\` y `Downloads` |
| `memory` | Memoria persistente entre conversaciones |
| `sequential-thinking` | Razonamiento estructurado paso a paso |

### Skills disponibles (usar con Skill tool o como /comando)
**Anthropic built-in:**
- `anthropic-skills:pdf` → propuestas en PDF
- `anthropic-skills:pptx` → presentaciones
- `anthropic-skills:xlsx` → presupuestos/hojas de cálculo
- `anthropic-skills:canvas-design` → diseño visual
- `anthropic-skills:web-artifacts-builder` → apps web interactivas
- `anthropic-skills:schedule` → programar tareas cloud
- `deep-research` → investigación multi-fuente verificada
- `code-review` → revisión de código
- `update-config` → configurar hooks/permisos Claude Code

**Brightdata (web intelligence):**
- `brightdata-plugin:search` → búsqueda web avanzada
- `brightdata-plugin:scrape` → scraping de cualquier web
- `brightdata-plugin:competitive-intel` → inteligencia competitiva
- `brightdata-plugin:seo-audit` → auditoría SEO
- `brightdata-plugin:brand-listening` → monitoreo de marca
- `brightdata-plugin:live-research` → investigación en tiempo real

**Marketing:**
- `marketing:content-creation` → contenido redes/blog
- `marketing:email-sequence` → secuencias email
- `marketing:campaign-plan` → plan de campaña
- `marketing:seo-audit` → auditoría SEO
- `vpai:vibe-prospecting` → outreach y prospección

**Bigdata.com (análisis empresarial):**
- `bigdata-com:company-brief` → brief de empresa
- `bigdata-com:risk-assessment` → evaluación riesgos
- `bigdata-com:sector-analysis` → análisis de sector
- `bigdata-com:investment-memo` → memo de inversión

**Legal:**
- `legal:review-contract` → revisar contratos
- `legal:triage-nda` → clasificar NDAs
- `legal:compliance-check` → verificar cumplimiento
- `legal:legal-risk-assessment` → evaluar riesgos legales

**Carta (cap table para clientes startup):**
- `carta-crm:search-companies`, `carta-cap-table:carta-round-history`

---

## 5. ESTRUCTURA DE CARPETAS — LOS "MUNDOS"

Ruta base: `D:\Proyectos claude\`

```
mundo-dev-clientes/     → apps, sistemas, APIs (500-15,000€)
  └── equipo/           → sub-agentes: frontend, backend, db, devops, qa
mundo-social-media/     → gestión redes (500-2,000€/mes)
mundo-ciberseguridad/   → auditorías, pen testing (800-5,000€)
mundo-chatbots/         → asistentes IA (500-3,000€)
  └── herramientas/demo-chatbot-local.py  (UI web, 6 sectores, usa Ollama)
mundo-ecommerce/        → tiendas online (1,000-8,000€)
mundo-saas-factory/     → SaaS propios (recurrente)
mundo-ventas/           → funnel y outreach
  └── web-nexia/        → Landing NEXIA en Next.js (build en /out/)
  └── herramientas/scraper-leads.py  (SCRAPER de leads OSM gratis — ver abajo)
  └── herramientas/outreach-linkedin.py  (10 sectores, 3 mensajes/sector)
  └── herramientas/generar-propuesta.py  (propuesta MD con Ollama)
  └── leads-scrapeados/  (CSVs de leads encontrados por el scraper)
  └── perfiles-freelancer/  (Upwork, Fiverr, etc.)

### Scraper de Leads (mundo-ventas/herramientas/scraper-leads.py)
Encuentra negocios por nicho+ciudad usando OpenStreetMap (Nominatim+Overpass). 100% gratis, sin API key, legal. Enriquece email visitando la web, clasifica con Ollama, guarda en CRM, exporta CSV.
```
python scraper-leads.py --listar-nichos
python scraper-leads.py --nicho restaurantes --ciudad "Valencia" --solo-con-web --enriquecer
python scraper-leads.py --nicho dentistas --ciudad "Madrid" --enriquecer --clasificar --crm
```
Flags: --subnicho (vegano/italiano/japones...), --pais (default Spain), --limite, --solo-con-web, --enriquecer (email desde web), --clasificar (score IA), --crm (guardar en CRM).
Usar SIEMPRE `C:\Program Files\Python312\python.exe`. Probado: 60 restaurantes Valencia -> 12 con web -> 6 emails reales.
Upgrade futuro (con presupuesto): brightdata-plugin para Google Maps con datos mas ricos.

### Diagnostico Web + Catalogo de servicios (venta por auditoria)
`mundo-ventas/herramientas/diagnostico-web.py` — audita la web de un negocio (SSL, velocidad, responsive, formulario, Analytics, WordPress, SEO, chatbot), detecta problemas REALES y los mapea a servicios del catalogo con precio. Genera pitch personalizado con Ollama.
`mundo-ventas/catalogo-servicios.json` — 35 servicios freelance (precios Workana, USD) con `trigger` = senal del diagnostico que recomienda cada uno.
```
python diagnostico-web.py --url restaurante.com --negocio "X" --pitch
python diagnostico-web.py --csv ../leads-scrapeados/XXXX.csv --pitch --limite 10
```
Flujo de venta completo: scraper-leads (encuentra) -> diagnostico-web (audita+pitch) -> CRM -> funnel email. Probado: unsushi.es -> 5 problemas reales -> $280-950 en servicios -> email listo para enviar.

### Buscador de trabajos freelance (mundo-ventas/herramientas/buscar-trabajos.py)
Trae proyectos reales de la API pública de Freelancer.com (sin login), filtra por skills NEXIA + presupuesto USD + competencia (nº pujas), y genera una propuesta personalizada con Ollama para cada uno. Salida: CSV + Markdown legible en `trabajos-encontrados/`. TÚ revisas y aplicas manual (NUNCA auto-aplicar: banea la cuenta).
```
python buscar-trabajos.py --min-budget 200 --max-competencia 40 --propuestas
python buscar-trabajos.py --query chatbot --propuestas --top 5
```
Probado: encuentra proyectos reales ($250-6350), normaliza monedas a USD, propuestas que referencian la necesidad concreta del cliente.
mundo-multimedia/       → vídeo, imagen, audio
  └── herramientas/face_swap_video.py   (insightface face swap)
  └── herramientas/dia-padre-CALIDAD.bat (video Día del Padre, full res)
mundo-seo/              → posicionamiento orgánico
mundo-ads/              → publicidad de pago
mundo-email-marketing/  → newsletters
mundo-agencia/          → CRM, propuestas, facturación
  └── api/agencia-api.py  (Flask API puerto 8080)
  └── crm/agencia.db      (SQLite CRM)
  └── memoria/            (estado, clientes, facturación)
mundo-dev-clientes/nexia-backend/  (Laravel backend — EN CONSTRUCCIÓN)
```

---

## 6. PRODUCTOS/SERVICIOS Y PRECIOS DE NEXIA

| Paquete | Precio | Tiempo | Descripción |
|---------|--------|--------|-------------|
| Starter | 497€ | 5 días | Landing + chatbot básico |
| Growth | 1,497€ | 3 semanas | App web + dashboard |
| Agency Pro | 4,997€ | 6 semanas | Sistema a medida |
| Mantenimiento | 49-997€/mes | Recurrente | Hosting + soporte |
| Gestión RRSS | 500-2,000€/mes | Recurrente | Contenido + publicación |
| Chatbot IA | 2,000-8,000€ | 3-6 sem | Asistente personalizado |
| Consultoría IA | 150-300€/hora | - | Estrategia + implementación |

---

## 7. PROYECTOS EN CURSO

| Proyecto | Estado | Próximo paso |
|---------|--------|-------------|
| **Bot Fondeo** (prospecto, 8,000€) | Propuesta pendiente | Enviar propuesta detallada |
| **Maikel Alimentos** (activo, 3,500€) | Fase 2 pendiente | Definir scope Fase 2 |
| **Web NEXIA** | Build ✅, formulario→webhook ✅ | Pendiente: deploy a Netlify (drag `/out/`) y actualizar URL túnel tras reinicio |
| **Backend Laravel** | En construcción | Instalar Laravel, correr migrations en Supabase |
| **Video Día del Padre** | En proceso | Correr `dia-padre-CALIDAD.bat` con fotos nuevas |

---

## 8. LO QUE EXISTE vs LO QUE FALTA

### ✅ YA EXISTE Y FUNCIONA
- n8n corriendo con 4 workflows activos (incluyendo NEXIA Lead — E2E verificado)
- Ollama con qwen2.5:14b (2.6 t/s)
- API agencia Flask (puerto 8080)
- Landing NEXIA (Next.js, lista para deploy)
- CRM SQLite básico
- Scripts outreach LinkedIn/email
- Demo chatbot (6 sectores)
- Face-swap pipeline (insightface)
- MCP servers: filesystem, memory, sequential-thinking, n8n
- Todos los plugins: Brightdata, Marketing, Legal, Carta, Bigdata
- GitHub: github.com/michelmiranda683/universo-agencia

### ⚠️ CONSTRUIDO PERO PENDIENTE ACCIÓN MANUAL DEL USUARIO
- Deploy web NEXIA en Netlify (solo hay que arrastrar la carpeta `/out/`)
  - ⚠️ Antes de deploy: relanzar túnel (`LANZAR-TUNEL.bat`), actualizar `WEBHOOK_URL` en `page.tsx`, reconstruir (`BUILD-NEXIA.bat`)
- ~~Importar workflow n8n lead automático~~ ✅ HECHO — workflow NEXIA activo y E2E verificado
- Crear cuenta Supabase y copiar credenciales al .env
- Crear Gmail de empresa (nexia.agencia@gmail.com o similar)
- Crear LinkedIn Company Page NEXIA
- Crear Instagram @nexia.ia
- Registrar perfiles en Upwork/Fiverr (perfiles ya redactados)

### ❌ FALTA CONSTRUIR
- **Backend Laravel** — controladores, migrations, API endpoints
- ~~**Formulario web conectado al backend**~~ ✅ HECHO — formulario Next.js llama al webhook n8n vía localtunnel
- **Base de datos Supabase** (schema PostgreSQL ya existe, falta ejecutar)
- **CRM real** (el actual es SQLite básico — falta migrar a Supabase)
- **Sistema de pagos** (Stripe para cobrar a clientes)
- **Panel de control** para el usuario (ver estado de todos los mundos)
- **Automatización outreach** real (actualmente es manual)
- **FaceFusion** (herramienta pro de face swap — descarga manual desde GitHub)
- **Primer cliente real** — todo lo demás depende de esto

---

## 9. REGLAS PARA AGENTES DE COWORK

> Esto es crítico. Cuando Cowork lanza sub-agentes, estos no conocen el contexto. Deben seguir estas reglas:

1. **Node.js v22.16.0 YA ESTÁ INSTALADO** en `C:\Program Files\nodejs\` — NO instalar de nuevo
2. **n8n YA ESTÁ INSTALADO** en npm global — NO instalar de nuevo
3. **Python 3.12.9 YA ESTÁ EN EL PATH** — NO instalar
4. **Usar siempre PowerShell** — el usuario tiene permiso total, sin confirmaciones
5. **Ruta base del proyecto:** `D:\Proyectos claude\`
6. **Para IA:** usar Ollama en http://localhost:11434, modelo qwen2.5:14b
7. **Para n8n:** usar 127.0.0.1:5678, NO localhost:5678 (IPv6 conflict)
8. **NO crear archivos de documentación** (.md) a menos que se pida explícitamente
9. **NO agregar comentarios** al código salvo que el WHY sea no obvio

---

## 10. PROBLEMA CONOCIDO: COWORK REINSTALA NODE.JS

**Síntoma:** Cuando se usa Cowork (multi-agente), los sub-agentes intentan instalar Node.js desde cero porque no saben que ya existe.

**Causa:** Los agentes de Cowork arrancan sin contexto del sistema. Ven que n8n necesita Node.js y asumen que hay que instalarlo.

**Solución:** Siempre iniciar los sub-agentes de Cowork con este contexto:
```
Node.js v22.16.0 está instalado en C:\Program Files\nodejs\node.exe
n8n v2.22.6 está instalado globalmente en npm
NO instalar ninguna de estas herramientas — solo usarlas
```
Alternativamente, ejecutar `node --version` al inicio de cualquier tarea para verificar antes de instalar.

---

## 11. ACCESO REMOTO (TAILSCALE)

- **IP Tailscale:** `100.99.251.46`
- **n8n desde móvil/remoto:** `http://100.99.251.46:5678` (con Tailscale activo en el dispositivo)
- **API Agencia remota:** `http://100.99.251.46:8080`
- **Remote Desktop:** deshabilitado (habilitar si se necesita: Settings → Remote Desktop)

---

## 12. PENDIENTES DEL USUARIO (solo tú puedes hacerlos)

- [ ] Gmail empresa: crear en accounts.google.com
- [ ] Supabase: crear cuenta en supabase.com → copiar URL y anon key al `.env`
- [ ] Netlify deploy: arrastrar `mundo-ventas/web-nexia/out/` a app.netlify.com/drop
- [x] ~~n8n workflow: importar `mundo-agencia/api/workflow-lead-automatico.json`~~ ✅ HECHO — workflow NEXIA activo, E2E verificado
- [ ] LinkedIn Company Page NEXIA
- [ ] Instagram @nexia.ia
- [ ] FaceFusion: descargar ZIP desde github.com/facefusion/facefusion → extraer en `mundo-multimedia/herramientas/facefusion`
- [ ] Reiniciar Claude Desktop para activar nuevos MCP servers (filesystem, memory, sequential-thinking)

---

## 13. TÚNEL PÚBLICO — FLUJO COMPLETO NEXIA

> El túnel expone n8n al exterior para que el formulario web reciba leads. Es temporal — la URL cambia en cada reinicio.

### Componentes del flujo
```
[Visitante web] → [Formulario Next.js] → [localtunnel] → [n8n webhook] → [email + CRM]
```

### Archivos clave
| Archivo | Función |
|---------|---------|
| `LANZAR-TUNEL.bat` | Lanza localtunnel en background, espera 25s, guarda URL |
| `lt-tunnel.bat` | Proceso localtunnel (lo lanza LANZAR-TUNEL.bat) |
| `tunnel-url.txt` | URL actual del túnel |
| `tunnel-output.log` | Log de localtunnel |
| `BUILD-NEXIA.bat` | Reconstruye el sitio Next.js (`npm run build`) |
| `TEST-LOCAL.bat` | Test E2E directo a localhost:5678 |
| `VERIFY-EXEC.bat` | Verifica ejecuciones en n8n API |

### Procedimiento después de reiniciar el PC
1. n8n arranca solo (Task Scheduler) — verificar en http://localhost:5678
2. Doble clic en `LANZAR-TUNEL.bat` — esperar 25s
3. Leer `tunnel-url.txt` → copiar la nueva URL
4. Editar `mundo-ventas/web-nexia/src/app/page.tsx` → línea `WEBHOOK_URL`
5. Doble clic en `BUILD-NEXIA.bat` → esperar build
6. Hacer deploy a Netlify (o usar localmente con `npm run dev`)

### Lecciones clave (no repetir errores)
- `cloudflared` NO se puede instalar desde CMD/PowerShell (VPN bloquea github.com DNS)
- `localtunnel` SÍ funciona via npm (npm tiene acceso a internet aunque CMD no)
- n8n escucha en IPv6 `::1` — desde Windows funciona `localhost:5678`, desde bash sandbox SOLO `[::1]:5678`
- localtunnel puede dar 408 timeout en primeras peticiones — el webhook sí funciona, es lag del relay
- El sandbox de Cowork usa proxy `localhost:3128` que bloquea `*.loca.lt` — usar Node.js scripts Windows para tests externos

---

## 14. FACTURACIÓN Y ESTADO FINANCIERO

| Concepto | Valor |
|---------|-------|
| Facturación actual | 0€ |
| Objetivo primer cliente | 500-2,000€ |
| Presupuesto en pipeline | 11,500€ (Bot Fondeo 8k + Maikel 3.5k) |
| Inversión en APIs (hasta ahora) | 0€ — todo gratis/local |
