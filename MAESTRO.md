# NEXIA — Archivo Maestro de la Agencia
**Actualizado:** 2026-06-21 | **Estado:** Pre-cliente (sin facturación activa)

---

## STACK TÉCNICO LOCAL (todo gratis)

| Herramienta | URL/Puerto | Estado |
|-------------|-----------|--------|
| **n8n** (automatización) | http://localhost:5678 | ✅ Activo |
| **Ollama** (IA local) | http://localhost:11434 | ✅ Activo |
| **Agencia API** | http://localhost:8080 | ⚠️ Verificar |
| **CRM SQLite** | mundo-agencia/crm/agencia.db | ✅ Existe |

**Modelos Ollama disponibles:**
- `qwen2.5:14b` — 2.6 t/s (principal)
- `qwen2.5-coder:7b` — código

---

## PLUGINS Y CAPACIDADES CONECTADAS

### MCP Servers (Claude Desktop config)
| Servidor | Función | Config |
|---------|---------|--------|
| `n8n-agencia` | Workflows n8n, publicar redes sociales | localhost:5678 |
| `filesystem` | Acceso directo a D:\Proyectos claude + Downloads | ✅ Activo |
| `memory` | Memoria persistente entre conversaciones | ✅ Activo |
| `sequential-thinking` | Razonamiento paso a paso complejo | ✅ Activo |

### Skills de Anthropic (slash commands)
| Skill | Para qué usarla |
|-------|----------------|
| `anthropic-skills:pdf` | Generar PDFs de propuestas/reportes |
| `anthropic-skills:pptx` | Presentaciones PowerPoint |
| `anthropic-skills:xlsx` | Hojas de cálculo / presupuestos |
| `anthropic-skills:canvas-design` | Diseño visual en canvas |
| `anthropic-skills:web-artifacts-builder` | Construir apps web interactivas |
| `anthropic-skills:consolidate-memory` | Consolidar memorias largas |
| `anthropic-skills:schedule` | Programar tareas automáticas |
| `update-config` | Configurar hooks y permisos de Claude Code |
| `code-review` | Revisión de código |
| `deep-research` | Investigación multi-fuente con verificación |

### Brightdata (web scraping / inteligencia)
| Skill | Para qué usarla |
|-------|----------------|
| `brightdata-plugin:search` | Búsqueda web avanzada |
| `brightdata-plugin:scrape` | Scraping de cualquier web |
| `brightdata-plugin:competitive-intel` | Inteligencia competitiva de empresas |
| `brightdata-plugin:seo-audit` | Auditoría SEO de webs |
| `brightdata-plugin:brand-listening` | Monitoreo de marca en redes |
| `brightdata-plugin:price-comparison` | Comparación de precios |
| `brightdata-plugin:live-research` | Investigación en tiempo real |

### Marketing (contenido y campañas)
| Skill | Para qué usarla |
|-------|----------------|
| `marketing:content-creation` | Crear contenido para redes/blog |
| `marketing:email-sequence` | Secuencias de email marketing |
| `marketing:campaign-plan` | Plan de campaña completo |
| `marketing:seo-audit` | Auditoría SEO |
| `marketing:competitive-brief` | Brief competitivo |
| `marketing:performance-report` | Reporte de resultados |
| `marketing:brand-review` | Revisión de marca |
| `vpai:vibe-prospecting` | Outreach y prospección de ventas |

### Bigdata.com (análisis financiero/empresarial)
| Skill | Para qué usarla |
|-------|----------------|
| `bigdata-com:company-brief` | Brief rápido de empresa |
| `bigdata-com:investment-memo` | Memo de inversión |
| `bigdata-com:risk-assessment` | Evaluación de riesgos |
| `bigdata-com:sector-analysis` | Análisis de sector/industria |
| `bigdata-com:thematic-research` | Investigación temática |
| `bigdata-com:valuation-snapshot` | Snapshot de valoración |

### Carta (cap table / inversores)
> Diseñado para startups con equity. Útil si un cliente tiene cap table.
| Skill | Para qué usarla |
|-------|----------------|
| `carta-crm:search-companies` | Buscar empresas en Carta |
| `carta-cap-table:carta-round-history` | Historial de rondas |
| `carta-investors:carta-soi` | Schedule of Investments |

---

## PROYECTOS ACTIVOS

| Proyecto | Cliente | Estado | Próximo paso |
|---------|---------|--------|-------------|
| Bot Fondeo | Cliente Bot | Prospecto | Propuesta pendiente 8,000€ |
| Maikel Alimentos | Maikel | Activo | Fase 2 pendiente |
| Video Día del Padre | Personal | En proceso | Rehacerlo calidad completa |
| Web Nexia | Interno | Pendiente deploy | Arrastrar /out a Netlify |

---

## MUNDOS Y SERVICIOS

```
mundo-dev-clientes/     → apps, sistemas, APIs (500-15,000€)
mundo-social-media/     → gestión redes (500-2,000€/mes)
mundo-ciberseguridad/   → auditorías, pen testing (800-5,000€)
mundo-chatbots/         → asistentes IA (500-3,000€)
mundo-ecommerce/        → tiendas online (1,000-8,000€)
mundo-saas-factory/     → SaaS propios (recurrente)
mundo-ventas/           → funnel y outreach
mundo-multimedia/       → vídeo, imagen, audio
mundo-seo/              → posicionamiento
mundo-ads/              → publicidad de pago
mundo-email-marketing/  → newsletters
mundo-agencia/          → CRM, propuestas, facturación
```

---

## N8N — WORKFLOWS DISPONIBLES

**URL del servidor:** `http://localhost:5678`
**Webhook social:** `http://localhost:5678/webhook/publish-social`
**Webhook agencia:** `http://localhost:5678/webhook/agencia`

Para el plugin de n8n en herramientas externas, usar:
- **URL base:** `http://localhost:5678`
- **API Key:** (configurada en n8n Settings → API)

---

## CLIENTES Y FACTURACIÓN

**Facturación actual:** 0€ (fase pre-cliente)
**Objetivo primer cliente:** 500-2,000€

Ver detalles: `mundo-agencia/memoria/clientes.md`

---

## HERRAMIENTAS MULTIMEDIA

| Script | Función | Ruta |
|--------|---------|------|
| `face_swap_video.py` | Swap de caras en vídeo | mundo-multimedia/herramientas/ |
| `dia-padre-CALIDAD.bat` | Video Día del Padre calidad completa | mundo-multimedia/herramientas/ |
| `face_swap_rapido.py` | Procesado paralelo (chunks) | mundo-multimedia/herramientas/ |

**Fotos Día del Padre (fuentes):**
- `padre_nuevo.jpg` — padre, frontal, 45KB ✅ NUEVA CALIDAD
- `hijo_nuevo.jpg` — hijo, 72KB ✅ NUEVA CALIDAD
- `v2_hijo_naranja.jpg` — pelado naranja, 17KB

---

## REGLAS DE AHORRO DE TOKENS

1. **Leer este archivo al inicio** de cada conversación para contexto
2. Usar **Ollama local** para cualquier tarea interna (gratis)
3. Usar **Haiku** para posts, emails, tareas repetitivas
4. Guardar **decisiones arquitectónicas** en CLAUDE.md del mundo correspondiente
5. No repetir en memoria lo que ya está en el código

---

## PENDIENTES CRÍTICOS

- [ ] Deploy web Nexia en Netlify (arrastra /out a app.netlify.com/drop)
- [ ] Primer cliente → activar stack de pago
- [ ] FaceFusion: descargar ZIP de github.com/facefusion/facefusion
- [ ] Redes sociales: crear LinkedIn Company + Instagram @nexia.ia
- [ ] Reiniciar Claude Desktop para activar nuevos MCP servers
