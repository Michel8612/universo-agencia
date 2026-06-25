# Conectar Groq — OpenClaw (tu PC) + Herramientas de NEXIA

Guía para enchufar la **API de Groq** (IA rápida y gratis en la nube) en dos sitios:

1. **OpenClaw** en tu PC de EE.UU. (el asistente que orquesta la agencia).
2. **Las herramientas Python de `mundo-ventas`** (ya hecho en el repo).

> ⚠️ Esta sesión de Claude corre en un contenedor cloud aislado y **NO tiene
> acceso a tu PC**. Por eso lo de OpenClaw son instrucciones para que las
> ejecutes tú en tu máquina. Lo de las herramientas Python sí está commiteado.

---

## 0. Conseguir la API key de Groq (gratis)

1. Entra en https://console.groq.com/keys
2. Crea una key. Empieza por `gsk_...`. Cópiala (solo se muestra una vez).
3. Groq es gratis con límites de cuota generosos y muy rápido. Modelos útiles:
   - `llama-3.3-70b-versatile` → calidad (propuestas, análisis) ✅ por defecto
   - `llama-3.1-8b-instant` → velocidad/volumen (clasificar leads en masa)

> El endpoint de Groq es **compatible con OpenAI**:
> `https://api.groq.com/openai/v1`

---

## 1. OpenClaw en tu PC → usar Groq

OpenClaw (https://github.com/openclaw/openclaw) se configura en
`~/.openclaw/openclaw.json` y el modelo se indica como `"<proveedor>/<modelo>"`.

La forma **recomendada y confirmada** de configurarlo es el asistente guiado:

```bash
openclaw onboard --install-daemon
```

En el wizard:
- Elige proveedor **Groq** (o "OpenAI-compatible / custom" si no aparece Groq).
- Pega tu `GROQ_API_KEY` (`gsk_...`).
- Si te pide base URL: `https://api.groq.com/openai/v1`
- Modelo: `llama-3.3-70b-versatile`

> 📌 No memorizo el formato JSON exacto del bloque de proveedores de OpenClaw
> (cambia entre versiones). El wizard escribe el `openclaw.json` correcto por ti.
> Si prefieres editarlo a mano, mira la referencia oficial:
> https://docs.openclaw.ai/concepts/models  (sección de proveedores / model-failover).
> La idea es: definir el proveedor Groq con su `baseURL` + `apiKey`, y poner
> `agent.model` apuntando al modelo de Groq.

Tras configurarlo, prueba con un mensaje cualquiera; si responde rápido, va por Groq.

---

## 2. Herramientas Python de `mundo-ventas` → ya usan Groq (con fallback)

Hecho en el repo: todas las herramientas comparten `herramientas/llm.py`, que usa
**Groq si hay `GROQ_API_KEY`, y si no cae automáticamente a Ollama local**.

Afecta a: `buscar-trabajos.py`, `diagnostico-web.py`, `scraper-leads.py`,
`campana-leads.py`, `generar-propuesta.py`.

### Activarlo en tu PC / VPS

Copia `.env.example` a `.env` y rellena:

```bash
GROQ_API_KEY=gsk_tu_key_real
GROQ_MODEL=llama-3.3-70b-versatile
```

O expórtalo en la sesión antes de correr una herramienta:

**Windows (PowerShell):**
```powershell
$env:GROQ_API_KEY="gsk_tu_key_real"
python buscar-trabajos.py --query chatbot --propuestas
```

**Linux/Mac (VPS):**
```bash
export GROQ_API_KEY=gsk_tu_key_real
python3 buscar-trabajos.py --query chatbot --propuestas
```

### Cómo saber qué backend está usando

- `buscar-trabajos.py --propuestas` imprime `Generando propuestas con groq` (o `ollama`).
- En código: `from llm import backend_activo; print(backend_activo())`.

### Variables disponibles (todas opcionales menos la key)

| Variable        | Defecto                              | Para qué |
|-----------------|--------------------------------------|----------|
| `GROQ_API_KEY`  | (vacío → usa Ollama)                 | Activa Groq |
| `GROQ_MODEL`    | `llama-3.3-70b-versatile`            | Modelo Groq |
| `GROQ_BASE_URL` | `https://api.groq.com/openai/v1`     | Endpoint |
| `OLLAMA_URL`    | `http://localhost:11434/api/generate`| Fallback local |
| `OLLAMA_MODEL`  | `qwen2.5:14b`                        | Modelo Ollama |

---

## 3. Nota sobre "cazar leads/trabajos" desde la nube

El buscador de trabajos (Freelancer) y el scraper (OpenStreetMap) hacen peticiones
HTTP a servicios externos. En **tu PC o en un VPS** funcionan sin problema. En el
entorno cloud de Claude la política de red bloquea esos dominios, así que esa parte
**se ejecuta en tu máquina/VPS**, no en la sesión de Claude.
