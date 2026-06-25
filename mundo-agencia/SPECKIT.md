# Spec Kit (GitHub) — Skill de Desarrollo Guiado por Especificaciones

**Qué es:** [github/spec-kit](https://github.com/github/spec-kit) es un toolkit para
*Spec-Driven Development (SDD)*. En vez de tirar código a lo loco, primero defines QUÉ
quieres (spec), luego el plan técnico, luego las tareas, y solo entonces se implementa.
Funciona con Claude Code (la app de escritorio) mediante comandos `/speckit.*`.

> ⚠️ **No se pudo instalar desde la nube** (la red de este entorno bloquea clonar repos de
> GitHub que no sean este). Se instala y se usa **en tu PC**, en la app de escritorio de
> Claude, donde la red está abierta. Abajo tienes el comando único.

---

## Instalación + activación en este repo (en tu PC)

Requiere `uv` (gestor de Python). Si no lo tienes: https://docs.astral.sh/uv/getting-started/installation/

**Opción rápida — usa el script que dejé** (Linux/Mac/Git-Bash):
```bash
bash mundo-agencia/setup-speckit.sh
```

**O a mano:**
```bash
# 1) Instalar el CLI specify (una vez)
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@v0.11.8

# 2) Activarlo en este repo para Claude (desde la raíz del repo)
specify init --here --integration claude --script sh --force
#   Windows PowerShell: usa  --script ps   en vez de  --script sh
```

Flags (verificados en v0.11.8):
- `--here` → inicializa en el directorio actual (no crea uno nuevo).
- `--integration claude` → genera los comandos para Claude Code.
- `--script sh|ps` → scripts en bash (Linux/Mac) o PowerShell (Windows).
- `--force` → fusiona aunque la carpeta no esté vacía (nuestro caso).

## Qué crea

- `.specify/memory/constitution.md` → principios del proyecto.
- `.specify/templates/` → `spec-template.md`, `plan-template.md`, `tasks-template.md`.
- `.specify/scripts/bash/` → scripts auxiliares (crear feature, setup plan/tasks).
- `.claude/commands/speckit.*.md` → los comandos slash para Claude Code.
- `specs/` → aquí viven las specs de cada feature.

## Flujo de trabajo (comandos en Claude Code)

1. `/speckit.constitution` → fija los principios (usa el borrador de abajo).
2. `/speckit.specify` → describes la feature en lenguaje natural → genera la spec.
3. `/speckit.plan` → plan técnico (stack, arquitectura, decisiones).
4. `/speckit.tasks` → lista de tareas accionables.
5. `/speckit.implement` → ejecuta la implementación tarea a tarea.

(Versiones recientes añaden también `/speckit.clarify`, `/speckit.analyze` y
`/speckit.checklist` para afinar specs antes de implementar.)

**Regla de oro NEXIA:** nada de código de cliente sin pasar por specify → plan → tasks.
Para tareas internas pequeñas no hace falta; para proyectos de cliente, SIEMPRE.

---

## Borrador de constitución para NEXIA

Pega esto cuando uses `/speckit.constitution` (o directo en `.specify/memory/constitution.md`):

```markdown
# Constitución de NEXIA

## Principios
1. ROUTER DE MODELOS: usar el modelo más barato que resuelva bien la tarea.
   Opus solo para arquitectura, DB y ciberseguridad crítica. Ver CLAUDE.md.
2. HONESTIDAD: nunca inventar casos de éxito, métricas ni experiencia. Si somos
   nuevos, se dice claro (Programa Fundador).
3. DB PRIMERO: el diseño de base de datos lo valida el rol Arquitecto (Opus) antes
   de construir nada encima.
4. SPEC ANTES QUE CÓDIGO: todo proyecto de cliente pasa por spec → plan → tasks.
5. QA OBLIGATORIO: checklist completo antes de entregar; URL de producción funcional.
6. COSTE: preferir herramientas gratis (Ollama, Groq free, OSM) hasta facturar.
7. SEGURIDAD: nunca commitear secretos; .env siempre en .gitignore.

## Restricciones
- No auto-aplicar a plataformas freelance (viola ToS). Buscar sí, aplicar manual.
- No cold email masivo desde Gmail crudo (baneo). Tandas controladas + enlace de baja.

## Calidad
- Código que lea como el de alrededor (mismo estilo y convenciones).
- Entregas por fases con visto bueno del cliente en cada paso.
```

---

## Por qué te sirve con la app de escritorio

Cuando trabajes conmigo en la app de escritorio de Claude dentro de este repo, los
comandos `/speckit.*` ya estarán disponibles (porque `specify init` deja los archivos en
`.claude/commands/`). Así estructuramos cada proyecto de cliente igual y con calidad,
tanto desde la nube como desde tu PC.
