# Puente de continuidad PC ↔ Nube (MCP filesystem + Git)

Objetivo: poder **seguir trabajando pase lo que pase con la PC** (si se la llevan y la
traen, si cambias de equipo, etc.). Dos capas que se complementan.

---

## Capa 1 — Git/GitHub = el puente REAL entre tu PC y yo (la nube)

Esta es la que da continuidad de verdad entre máquinas:

- Tú trabajas en `D:\Proyectos claude` (que es el repo `Michel8612/universo-agencia`).
- **Haces commit + push** → todo queda en GitHub.
- En la nube **yo hago pull** y veo exactamente lo mismo. Y al revés: lo que hago yo,
  tú lo bajas con `git pull`.
- La **memoria** (`mundo-agencia/memoria/estado-fase.md`) viaja dentro del repo. Cualquier
  Claude, en cualquier máquina, lee ese archivo y sabe dónde estamos.

> ⚠️ Importante y honesto: un MCP que monta tu carpeta `D:\` **no** conecta con ESTA
> sesión en la nube (el contenedor cloud está aislado y no llega a tu PC; además mis
> conectores aquí los define el entorno, no los puedo añadir a mitad de sesión). El nexo
> nube↔PC es **Git**. El MCP de abajo es para tu **Claude Desktop**, no para mí en la nube.

### Protocolo de continuidad (la regla de oro)
1. **Al empezar** cualquier sesión (PC o nube): leer `mundo-agencia/memoria/estado-fase.md`.
2. **Al terminar**: actualizar ese archivo con lo hecho + `git add -A && git commit && git push`.
3. Resultado: el trabajo nunca se pierde aunque desaparezca la PC.

---

## Capa 2 — MCP filesystem: dar acceso a `D:\Proyectos claude` a tu Claude Desktop

Esto hace que, cuando trabajes con la app de escritorio de Claude en la PC, Claude pueda
**leer y escribir directamente** los archivos de esa carpeta (sin copiar/pegar).

### Instalación (en tu PC)
Requiere Node.js (trae `npx`). Edita el config de Claude Desktop:
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

Añade el servidor (junto al `nexia-empleos` que ya configuraste):

```json
{
  "mcpServers": {
    "proyectos-claude": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "D:\\Proyectos claude"]
    },
    "nexia-empleos": {
      "command": "python",
      "args": ["D:\\Proyectos claude\\mundo-ventas\\mcp-empleos\\server.py"]
    }
  }
}
```

Reinicia Claude Desktop. Ahora Claude (en la PC) puede listar, leer y editar archivos de
`D:\Proyectos claude` directamente. Es el servidor oficial
[`@modelcontextprotocol/server-filesystem`](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem),
y solo da acceso a la carpeta que le indicas (no a todo el disco).

### Seguridad
- Solo expone esa carpeta. No metas claves sueltas dentro sin `.gitignore`.
- `.env` (con claves reales) ya está en `.gitignore`: NO se sube a GitHub.

---

## Resumen para "si se llevan la PC"
1. La PC nueva: instala Git + Node + Python, `git clone https://github.com/Michel8612/universo-agencia.git D:\Proyectos claude`.
2. `cp .env.example .env` y rellena tus claves (esas no están en GitHub, son tuyas).
3. Configura los dos MCP de arriba en Claude Desktop.
4. Lee `mundo-agencia/memoria/estado-fase.md` → continúas justo donde lo dejaste.
