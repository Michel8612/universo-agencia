# MUNDO SAAS FACTORY — Fábrica de Productos Propios

El mundo más importante a largo plazo. Aquí construyes herramientas que cobran solas.
Un SaaS con 100 clientes a 49€/mes = 4,900€ recurrentes SIN hacer nada.

## Modelo
- Arquitectura del producto: **Opus** (decisión de por vida)
- Desarrollo: **Sonnet**
- Copy/marketing del SaaS: **Haiku**

## Ideas de SaaS para construir (ordenadas por potencial)

### 🥇 SaaS #1 — Agente de Atención al Cliente con IA (mayor demanda)
- Chatbot entrenado con los datos del negocio del cliente
- Se integra en su web con un snippet de código
- Responde preguntas, toma pedidos, agenda citas
- Precio: 49-299€/mes según volumen
- Stack: Next.js + Supabase + Claude API + widget JS

### 🥈 SaaS #2 — Generador de Contenido para PYMES
- El negocio conecta sus redes → IA genera y publica sola
- Dashboard simple para aprobar/rechazar posts
- Precio: 29-99€/mes
- Stack: Next.js + n8n + Supabase

### 🥉 SaaS #3 — Facturación y Presupuestos con IA
- El cliente describe el trabajo → IA genera presupuesto PDF
- Envío automático, seguimiento, recordatorios
- Precio: 19-49€/mes
- Stack: Next.js + Supabase + Stripe + PDF generation

### Otros candidatos
- Monitor de reputación online (alertas cuando mencionan la marca)
- Analizador de competencia automático
- CRM simplificado con IA para PYMES

## Proceso de construcción de cada SaaS
1. **Validar antes de construir** — 5 clientes que paguen por adelantado
2. **MVP en 2 semanas** — lo mínimo que resuelva el problema
3. **Beta privada** — 10 usuarios, feedback constante
4. **Launch** — Product Hunt + LinkedIn + YouTube
5. **Iterar** — retención > adquisición

## Stack estándar de SaaS
```
Frontend:  Next.js 14 + Tailwind + shadcn/ui
Auth:      Supabase Auth
DB:        Supabase PostgreSQL
Pagos:     Stripe (subscriptions + webhooks)
Email:     Resend
Deploy:    Vercel (gratis hasta escalar)
Analytics: Plausible (privacy-friendly)
```

## Regla de oro del SaaS
**No construyas features. Resuelve dolores.**
Habla con 10 dueños de negocio antes de escribir una línea de código.
