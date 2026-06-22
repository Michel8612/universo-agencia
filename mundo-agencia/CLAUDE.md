# MUNDO AGENCIA — CRM + Orquestador Central

El cerebro operativo de la agencia. Gestiona clientes, propuestas, proyectos activos y facturación.

## API Central (Puerto 8080)

Archivo: `mundo-agencia/api/agencia-api.py`
Arranque manual: `INICIAR-API.bat` | Auto-start: VBS en Startup folder (20s delay)
Log: `C:\Users\Romer\AppData\Local\agencia-api.log`

### Endpoints clave

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/` | GET | Health check — lista los 14 mundos |
| `/estado` | GET | CRM stats + estado Ollama |
| `/contenido/generar` | POST | Posts, emails, propuestas con Ollama |
| `/crm/cliente` | POST | Añade cliente a SQLite |
| `/crm/clientes` | GET | Lista todos los clientes |
| `/multimedia/video` | POST | Genera vídeo con FFmpeg |
| `/ventas/propuesta` | POST | Propuesta comercial completa (MD) |
| `/tarea` | POST | Ejecuta script Python de cualquier mundo |

Tipos de contenido: `post_linkedin`, `post_instagram`, `email_prospecto`, `propuesta`, `seo_meta`, `idea_contenido`

## CRM SQLite

Archivo: `mundo-agencia/crm/agencia.db`
- Tabla `clientes`: nombre, contacto, mundo, estado, presupuesto, notas
- Tabla `tareas`: log automático de todas las ejecuciones

## Hub n8n (importar JSON)

Archivo: `mundo-agencia/api/hub-workflow.json`
Webhook en: `http://localhost:5678/webhook/agencia`
```json
{"tipo": "contenido", "subtipo": "post_linkedin", "tema": "IA para pymes"}
```

## Clientes activos (CRM)

| Cliente | Estado | Presupuesto | Notas |
|---------|--------|-------------|-------|
| Maikel Alimentos | activo | 3,500€ | Fase 2 pendiente |
| Cliente Bot Fondeo | prospecto | 8,000€ | Bot + frontend + VPS + Meta Ads |

## Funciones Principales
- CRM de clientes (historial, contactos, estado)
- Generación de propuestas comerciales
- Seguimiento de proyectos activos
- Control de facturación y pagos
- Onboarding de nuevos clientes

## Protocolo de Nuevo Cliente

### 1. Primer Contacto
Al recibir un lead, crear automáticamente:
- Ficha en `memoria/clientes.md`
- Carpeta en `mundo-dev-clientes/proyectos/`
- Propuesta base en `memoria/propuestas/`

### 2. Propuesta Comercial
Template adaptable que incluye:
- Resumen ejecutivo del problema
- Solución propuesta (con arquitectura simplificada)
- Timeline (por fases/sprints)
- Precios por paquete (Basic/Pro/Enterprise)
- Garantías y soporte post-entrega

### 3. Onboarding (cliente aceptado)
- Crear canal de comunicación dedicado
- Definir KPIs de éxito del proyecto
- Establecer reuniones de seguimiento (checkpoint semanal)
- Accesos y credenciales necesarias

## Catálogo de Servicios de la Agencia

| Servicio | Precio Referencia | Tiempo |
|---------|------------------|--------|
| Landing Page + IA | 500-1.500€ | 1 semana |
| App web completa | 3.000-15.000€ | 1-3 meses |
| Sistema de automatización | 1.000-5.000€ | 2-4 semanas |
| Gestión redes sociales | 500-2.000€/mes | Recurrente |
| Chatbot IA personalizado | 2.000-8.000€ | 3-6 semanas |
| Consultoría IA | 150-300€/hora | - |

## Estructura de Memoria
```
mundo-agencia/
└── memoria/
    ├── clientes.md          ← CRM principal
    ├── propuestas/          ← propuestas por cliente
    ├── proyectos_activos.md ← estado de todos los proyectos
    └── facturacion.md       ← registro de ingresos
```

## Reporte Semanal Automático
Cada lunes genera un resumen de:
- Proyectos activos y su % de avance
- Ingresos de la semana
- Leads nuevos
- Tareas pendientes urgentes
