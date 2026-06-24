# Checklist Legal NEXIA — Acciones del fundador

> Basado en "Los 5 cimientos para publicar tu SaaS legal" (eriktaveras.com).
> ⚠️ NO es asesoría legal. Es un punto de partida; revisa con un abogado antes de cobrar al primer cliente.
> Lo marcado ✅ ya está implementado en la web. Lo marcado ⬜ depende de ti.

---

## Cimiento 1 — Estructura legal (DECISIÓN TUYA)
- ⬜ Definir titular legal que cobra (tú como autónomo / empresa)
- ⬜ Definir residencia fiscal (dónde declaras los ingresos)
- ⬜ Separar cuenta bancaria del negocio desde el día 1
- ⬜ Si vendes global en USD → evaluar US LLC (Firstbase/doola/Stripe Atlas) + EIN + Mercury/Wise
- ⬜ Si abres US LLC → recordatorio anual Form 5472 + 1120 (multa hasta $25.000 por no presentarlo)

**Regla:** puedes empezar como persona física para validar; formaliza antes de ingresos recurrentes o datos sensibles.

## Cimiento 2 — Términos de Uso
- ✅ Página de Términos publicada (`/terminos`) y enlazada en el footer
- ✅ Pagos, reembolsos y cancelaciones definidos
- ✅ Limitación de responsabilidad incluida
- ⬜ Confirmar JURISDICCIÓN aplicable (ahora genérica — poner tu país/estado real)

## Cimiento 3 — Privacidad
- ✅ Política de privacidad publicada (`/privacidad`)
- ✅ Derechos del usuario y cómo ejercerlos
- ✅ Lista de subprocesadores (Netlify, FormSubmit, email, IA)
- ✅ Aviso/banner de cookies + Política de Cookies (`/cookies`)
- ⬜ Firmar/activar los DPA (Data Processing Agreement) de cada subprocesador:
      - Stripe (cuando lo uses), Netlify, Google Workspace, Anthropic/OpenAI (si usas su IA)
      - La mayoría se activan desde el panel de cada proveedor

## Cimiento 4 — Seguridad
- ✅ HTTPS en todo (Netlify lo da automático)
- ✅ Sin API keys en el código (la web es estática, no expone secretos)
- ⬜ En el lado servidor (n8n/Flask/CRM): contraseñas con hashing, backups probados,
     aislamiento entre clientes, rate limiting en logins, 2FA para admin
- ⬜ Mini plan de respuesta a incidentes (contener → evaluar → notificar 72h GDPR → documentar → corregir)

## Cimiento 5 — Pagos y marketing
- ⬜ Usar Stripe / Paddle / Lemon Squeezy — nunca tocar números de tarjeta (te quita PCI-DSS)
- ⬜ Activar Stripe Tax o un Merchant of Record (Paddle/Lemon Squeezy) si vendes global (IVA por país)
- ✅ Política de reembolsos visible (en Términos)
- ⬜ En outreach/email: opt-in claro, enlace de baja real en cada email, identificarte (remitente + dirección)
- ⬜ WhatsApp Business: cumplir políticas de Meta (opt-in, plantillas aprobadas) o banean el número
- ⬜ No comprar listas ni enviar frío masivo sin base legal

## Bonus IA
- ✅ Divulgación de uso de IA en la web (footer + privacidad + términos)
- ✅ Aviso de que los resultados de IA pueden contener errores
- ✅ Subprocesadores de IA mencionados en privacidad
- ⬜ Si usas datos de cliente para entrenar → pedir consentimiento explícito (idealmente, no usarlos)

---

## Herramientas útiles (del checklist original)
| Necesidad | Opciones |
|-----------|----------|
| Generar términos/privacidad | Termly, iubenda, GetTerms, Termsfeed |
| Banner de cookies | Cookiebot, Osano, Termly |
| Pagos | Stripe, PayPal |
| Merchant of Record (impuestos globales) | Paddle, Lemon Squeezy, Polar |
| US LLC remota | Firstbase, doola, Stripe Atlas |
| Banco USD remoto | Mercury, Wise, Relay |
| Email transaccional/marketing | Resend, Postmark, Listmonk |

**Mínimo antes de cobrar al primer cliente:** estructura definida + términos + privacidad + HTTPS + procesador de pago serio.
