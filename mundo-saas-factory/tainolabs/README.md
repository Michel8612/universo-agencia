# Taíno Labs — análisis y plan para terminar

Producto: **sistema de respuesta y calificación instantánea de leads** ("responde y
califica cada contacto en segundos, 24/7"). Landing de venta bilingüe (EN/ES).

> Estaba **solo como un HTML suelto en Netlify** (subido a mano el 13-jun, sin repo).
> Ahora está versionado aquí. La web vive en https://tainolabs.netlify.app

## Qué es (encaja con la agencia)
Es la **versión productizada del servicio estrella de NEXIA**: chatbot + automatización
+ WhatsApp para que ningún lead se enfríe. Se puede **vender como servicio/SaaS** (prueba
14 días) o **usar como plantilla** para clientes. Mismo WhatsApp que NEXIA (5356659464).

## Estado: ✅ lo que YA está hecho (y está muy bien)
- Diseño profesional, limpio (Inter + Newsreader), responsive.
- **Bilingüe EN/ES** con diccionario completo + autodetección por idioma del navegador + toggle.
- **Calculadora de ROI interactiva**: 6 nichos (solar, HVAC, dental, legal, finanzas,
  hogar) con medias de EE.UU. 2026, sliders y cálculo de pérdida anual/mensual. Gran gancho B2B.
- **Demo animada** del flujo (entra lead → entiende → responde → cierra) con escenarios rotando.
- Sección problema, beneficios, CTA final con headline dinámico (importe a recuperar).
- **Formulario con Netlify Forms** (captura automática) + honeypot anti-spam.
- Botón flotante de WhatsApp + mensaje localizado.

## 🔧 Lo que FALTA para terminarlo (plan priorizado)

### P1 — Cierre del funnel (lo que más convierte)
- [ ] **Página/estado de "gracias"** tras enviar el formulario (ahora muestra la genérica de
  Netlify). Añadir `action="/gracias"` + página `gracias.html`, o éxito por AJAX.
- [ ] **Notificación de lead nuevo** → conectar Netlify Forms a email/Slack/Telegram (igual
  que en NEXIA con `notificar.py`). Que no se quede un lead sin ver.
- [ ] **Precio o "agenda una llamada"** — hoy dice "prueba 14 días" pero no hay precio ni
  enlace a calendario (Cal.com). Decidir modelo y añadirlo.

### P2 — Confianza y legal
- [ ] Páginas **Privacidad / Términos / Cookies** (hay checkbox de consentimiento + captura
  de datos → obligatorio). Reutilizar las de NEXIA.
- [ ] **Favicon** + **imagen OG** (para que se vea bien al compartir el enlace).

### P3 — SEO y medición
- [ ] `robots.txt`, `sitemap.xml`, canonical. (El `<html lang>` ya lo ajusta el JS.)
- [ ] Analítica/medición de conversión (Plausible/GA4) para optimizar.

### P4 — Producto real detrás (lo que se entrega)
- [ ] La landing VENDE el servicio; el **sistema que responde leads** (chatbot+automatización
  WhatsApp/web + agenda) es lo que NEXIA construye al cerrar cliente. Definir el "entregable
  estándar" (plantilla n8n + bot) para montarlo rápido a cada cliente.

### P5 — Despliegue serio
- [ ] **Conectar a Git** (este repo) en vez de drop manual, para que cada cambio se publique
  solo. Decisión: ¿deploy desde este monorepo o repo propio de Taíno Labs?
- [ ] Dominio propio (ej. tainolabs.com) en vez de subdominio netlify.app.

## Decisiones para ti
1. **Modelo de negocio:** ¿SaaS con suscripción, servicio a medida, o las dos?
2. **Precio:** ¿cuánto por la prueba/mensualidad?
3. **Despliegue:** ¿lo movemos a deploy por Git desde este repo (recomendado)?

Dime por dónde empezamos y lo terminamos por fases.
