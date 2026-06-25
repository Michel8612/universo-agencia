# MCP de Empleos — NEXIA (Freelancer.com)

Servidor MCP para que **Claude (app de escritorio)** busque empleos freelance en vivo
como una herramienta. Usa la API pública de Freelancer.com. Solo busca; **no auto-aplica**.

> Corre en **tu PC** (tiene salida a internet). La nube de Claude bloquea freelancer.com.

## 1. Instalar

```bash
cd mundo-ventas/mcp-empleos
pip install -r requirements.txt      # o: uv pip install -r requirements.txt
```

## 2. Configurar en Claude Desktop

Edita el archivo de config de Claude Desktop:
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`

Añade (ajusta la RUTA absoluta al repo):

```json
{
  "mcpServers": {
    "nexia-empleos": {
      "command": "python",
      "args": ["C:\\ruta\\al\\repo\\mundo-ventas\\mcp-empleos\\server.py"]
    }
  }
}
```

Reinicia Claude Desktop. Tendrás la herramienta **`buscar_empleos`**. Pídeme cosas como:
> "busca empleos de chatbot con presupuesto mínimo 300 y poca competencia"

## 3. Probar el servidor a mano (opcional)

```bash
python server.py        # arranca en modo MCP (stdio); Ctrl+C para salir
```

---

## Correr el scraper y la búsqueda de empleos directamente (sin MCP)

Estas herramientas (en `mundo-ventas/herramientas/`) también se corren sueltas en tu PC:

```bash
cd mundo-ventas/herramientas

# Buscar trabajos en Freelancer + generar propuestas con IA (Groq/Ollama):
python buscar-trabajos.py --query chatbot --min-budget 200 --max-competencia 40 --propuestas

# Cazar leads por nicho+ciudad (OpenStreetMap), clasificar y guardar en CRM:
python scraper-leads.py --nicho restaurantes --ciudad "Valencia, Espana" --enriquecer --clasificar --crm
```

(Recuerda tener `GROQ_API_KEY` en `.env` para que la IA vaya por Groq; si no, usa Ollama local.)
