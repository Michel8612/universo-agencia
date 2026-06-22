# MUNDO CHATBOTS IA — Asistentes para Negocios

Producto más vendible a PYMES. Todo negocio quiere atención 24/7 sin pagar empleados.

## Modelo
- Diseño de flujos complejos: **Sonnet**
- Respuestas, variaciones de texto: **Haiku**

## Tipos de Chatbot que construyes

### 1. Chatbot de Atención al Cliente
- Responde FAQs entrenado con los datos del negocio
- Deriva a humano cuando no sabe
- Canales: web, WhatsApp, Telegram, Instagram DMs
- Precio: 500-2,000€ setup + 49-199€/mes hosting

### 2. Chatbot de Ventas / Cualificación de Leads
- Conversa con el visitante, entiende su necesidad
- Cualifica si es buen cliente
- Agenda reunión automáticamente
- Precio: 800-3,000€ setup + mantenimiento

### 3. Asistente Interno para Equipos
- Responde dudas sobre procedimientos internos
- Accede a documentación de la empresa
- Para RRHH, soporte interno, onboarding de empleados
- Precio: 1,500-5,000€

### 4. Chatbot de Reservas/Citas
- Hoteles, clínicas, restaurantes, peluquerías
- Conecta con Google Calendar o sistema propio
- Precio: 600-1,500€ + 29-79€/mes

## Stack técnico
```
Motor IA:     Claude API (Haiku para respuestas = barato)
Framework:    Vercel AI SDK o LangChain
Widget web:   React embeddable (<script> tag)
WhatsApp:     Twilio o Meta Cloud API
Telegram:     Bot API (gratis)
Instagram:    Meta Graph API
Base de datos: Supabase (historial de conversaciones)
Embeddings:   Supabase pgvector (para entrenar con docs)
```

## Proceso de implementación
1. Recopilar documentación del negocio (FAQs, catálogo, precios)
2. Procesar y vectorizar con embeddings
3. Configurar personalidad y límites del bot
4. Integrar en los canales del cliente
5. Periodo de prueba 1 semana
6. Ajustes y entrega final
7. Formación al equipo para gestionar el panel

## Ventaja competitiva
- **Haiku** cuesta ~$0.001 por conversación → margen brutal
- 1,000 conversaciones/mes = $1 de coste → cobras 49€/mes
- El cliente percibe valor enorme (atención 24/7)
