#!/usr/bin/env node
/**
 * MCP Server — n8n Bridge
 * Permite a Claude Code activar workflows de n8n directamente
 */

const http = require("http");

const N8N_BASE_URL = process.env.N8N_BASE_URL || "http://localhost:5678";
const N8N_API_KEY = process.env.N8N_API_KEY || "";

// MCP protocol over stdio
process.stdin.setEncoding("utf8");

function send(obj) {
  process.stdout.write(JSON.stringify(obj) + "\n");
}

async function callN8n(path, method = "GET", body = null) {
  return new Promise((resolve, reject) => {
    const url = new URL(N8N_BASE_URL + path);
    const options = {
      hostname: url.hostname,
      port: url.port || 5678,
      path: url.pathname + url.search,
      method,
      headers: {
        "Content-Type": "application/json",
        "X-N8N-API-KEY": N8N_API_KEY,
      },
    };
    const req = http.request(options, (res) => {
      let data = "";
      res.on("data", (chunk) => (data += chunk));
      res.on("end", () => {
        try { resolve(JSON.parse(data)); }
        catch { resolve({ raw: data }); }
      });
    });
    req.on("error", reject);
    if (body) req.write(JSON.stringify(body));
    req.end();
  });
}

const TOOLS = [
  {
    name: "n8n_list_workflows",
    description: "Lista todos los workflows de n8n disponibles",
    inputSchema: { type: "object", properties: {} },
  },
  {
    name: "n8n_trigger_workflow",
    description: "Activa un workflow de n8n por webhook o ID",
    inputSchema: {
      type: "object",
      required: ["webhook_url"],
      properties: {
        webhook_url: { type: "string", description: "URL del webhook del workflow" },
        data: { type: "object", description: "Datos a enviar al workflow" },
      },
    },
  },
  {
    name: "n8n_get_executions",
    description: "Ver las últimas ejecuciones de un workflow",
    inputSchema: {
      type: "object",
      properties: {
        workflow_id: { type: "string", description: "ID del workflow" },
        limit: { type: "number", description: "Cuántas ejecuciones mostrar (default 10)" },
      },
    },
  },
  {
    name: "n8n_publish_social",
    description: "Publica contenido en redes sociales vía n8n",
    inputSchema: {
      type: "object",
      required: ["content", "platforms"],
      properties: {
        content: { type: "string", description: "Texto del post" },
        platforms: {
          type: "array",
          items: { type: "string", enum: ["instagram", "tiktok", "twitter", "linkedin", "facebook"] },
          description: "Plataformas donde publicar",
        },
        image_url: { type: "string", description: "URL de imagen opcional" },
        schedule_at: { type: "string", description: "ISO datetime para programar (opcional)" },
      },
    },
  },
];

let buffer = "";
process.stdin.on("data", async (chunk) => {
  buffer += chunk;
  const lines = buffer.split("\n");
  buffer = lines.pop();

  for (const line of lines) {
    if (!line.trim()) continue;
    let msg;
    try { msg = JSON.parse(line); } catch { continue; }

    if (msg.method === "initialize") {
      send({
        jsonrpc: "2.0", id: msg.id,
        result: {
          protocolVersion: "2024-11-05",
          capabilities: { tools: {} },
          serverInfo: { name: "n8n-mcp", version: "1.0.0" },
        },
      });
    } else if (msg.method === "tools/list") {
      send({ jsonrpc: "2.0", id: msg.id, result: { tools: TOOLS } });

    } else if (msg.method === "tools/call") {
      const { name, arguments: args } = msg.params;
      let result;

      try {
        if (name === "n8n_list_workflows") {
          const data = await callN8n("/api/v1/workflows");
          result = { workflows: data.data?.map(w => ({ id: w.id, name: w.name, active: w.active })) };

        } else if (name === "n8n_trigger_workflow") {
          const res = await fetch(args.webhook_url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(args.data || {}),
          });
          result = { status: res.status, ok: res.ok };

        } else if (name === "n8n_get_executions") {
          const data = await callN8n(`/api/v1/executions?workflowId=${args.workflow_id || ""}&limit=${args.limit || 10}`);
          result = { executions: data.data };

        } else if (name === "n8n_publish_social") {
          // Llama al webhook del workflow de publicación social
          const webhookUrl = process.env.N8N_SOCIAL_WEBHOOK || `${N8N_BASE_URL}/webhook/publish-social`;
          const res = await fetch(webhookUrl, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(args),
          });
          result = { status: res.status, message: "Post enviado a n8n para publicar", platforms: args.platforms };
        }
      } catch (e) {
        result = { error: e.message };
      }

      send({
        jsonrpc: "2.0", id: msg.id,
        result: { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] },
      });
    }
  }
});

process.on("uncaughtException", () => {});
