# Campaña de leads USA + búsqueda de empleos (servidor)

Todo esto corre en el **servidor USA** (tiene salida a internet). La nube de Claude bloquea
OSM/Freelancer, así que aquí solo se construye y se prueba en seco; el run real va allá.

## 1. Campaña de leads en TODO USA (24/7)

Motor: `herramientas/campana-usa.py` — 98 ciudades (50 estados) × 15 nichos de alto valor.
Por cada negocio con web: **diagnóstico web completo** (velocidad, móvil, SSL, SEO, chat,
formulario, analytics, redes) → servicios del catálogo con precio → email frío con IA →
guarda en el CRM. Sin duplicados (estado en `campana-usa-estado.json`), reanuda solo.

### Anti-bloqueo ("no quemar la cuenta")
- Nominatim: 1.2s por ciudad (límite oficial) + `--pausa-combo` (def. 4s) entre combos.
- Overpass: mirrors con fallback + User-Agent de navegador (ya en scraper-leads).
- `--pausa-vuelta` (def. 3600s) entre vueltas completas → no martillea OSM.
- **No envía emails** (solo los prepara) → imposible quemar el correo. El envío se hace
  aparte, en tandas de 20-40/día, con opt-out (CAN-SPAM).

### Cómo dejarlo corriendo
- **Fácil:** doble clic en `mundo-ventas/INICIAR-CAMPANA-USA.bat` (se auto-reinicia si peta).
  Deja la ventana abierta o prográmalo en Task Scheduler al inicio de sesión.
- **Manual / prueba en vivo (1 vuelta):**
  ```bat
  cd mundo-ventas\herramientas
  python campana-usa.py --once --por-combo 4
  ```
- **Prueba offline (0 red, valida config):**
  ```bat
  python campana-usa.py --solo-listar
  ```
- Salida: leads en el CRM + ficheros `mundo-ventas/campanas/usa-*.md` + log
  `mundo-ventas/campana-usa.log`.

### Opciones útiles
| Flag | Para qué | Defecto |
|------|----------|---------|
| `--por-combo N` | leads con web por combinación | 6 |
| `--pausa-combo S` | segundos entre combos (subir si OSM se queja) | 4 |
| `--pausa-vuelta S` | segundos entre vueltas completas | 3600 |
| `--sin-email` | solo encontrar+diagnosticar (sin gastar IA) | off |
| `--once` | una sola vuelta | off |

> Si algún mirror de OSM da 429/406, sube `--pausa-combo` a 8-10s. El script nunca se
> cae por un error de red: lo registra y sigue.

## 2. Buscar empleos en Freelancer (para aplicar manual)

Herramienta: `herramientas/buscar-trabajos.py` (API pública de Freelancer, sin login).
Trae proyectos activos por skill, filtra por presupuesto/competencia y **redacta la
propuesta con IA en el idioma del proyecto**. TÚ revisas y aplicas manual (auto-aplicar
viola los ToS y banea la cuenta).

```bat
cd mundo-ventas\herramientas

REM Buscar en una skill concreta con propuestas:
python buscar-trabajos.py --query chatbot --min-budget 250 --max-competencia 35 --propuestas

REM Barrido por todas las skills de NEXIA (web, wordpress, automation, n8n, react...):
python buscar-trabajos.py --min-budget 200 --max-competencia 40 --propuestas
```
Salida: `mundo-ventas/trabajos-encontrados/trabajos-*.md` (legible, con la propuesta lista
para copiar) y `.csv`. Revisa, ajusta y aplica desde tu cuenta de Freelancer.

> Alternativa: el **MCP de empleos** (`mundo-ventas/mcp-empleos/`) te deja pedírmelo en
> lenguaje natural desde Claude Desktop ("busca trabajos de chatbot con buen presupuesto").
