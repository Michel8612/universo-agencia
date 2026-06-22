import { anthropic } from "@ai-sdk/anthropic";
import { streamText } from "ai";
import { createClient } from "@supabase/supabase-js";
import { NextRequest } from "next/server";

const supabase = createClient(
  process.env.SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_KEY!
);

export async function POST(req: NextRequest) {
  const { messages, businessId } = await req.json();

  // Obtener contexto del negocio (FAQs, productos, info)
  const { data: business } = await supabase
    .from("businesses")
    .select("name, system_prompt, knowledge_base")
    .eq("id", businessId)
    .single();

  if (!business) {
    return new Response("Negocio no encontrado", { status: 404 });
  }

  // Guardar conversación en DB
  await supabase.from("conversations").insert({
    business_id: businessId,
    messages: messages,
    created_at: new Date().toISOString(),
  });

  // Stream respuesta con Haiku (barato para alto volumen)
  const result = await streamText({
    model: anthropic("claude-haiku-4-5-20251001"),
    system: `Eres el asistente virtual de ${business.name}.
${business.system_prompt}

BASE DE CONOCIMIENTO:
${business.knowledge_base}

REGLAS:
- Responde siempre en el idioma del usuario
- Sé amable y profesional
- Si no sabes algo, di "Déjame conectarte con un agente humano"
- Nunca inventes información sobre precios o disponibilidad
- Máximo 3 párrafos por respuesta`,
    messages,
    maxTokens: 500,
  });

  return result.toDataStreamResponse();
}
