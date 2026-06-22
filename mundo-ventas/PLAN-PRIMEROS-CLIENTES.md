# NEXIA — Plan de Acción: Primeros 3 Clientes

**Fecha inicio**: Junio 2026  
**Objetivo**: 3 clientes pagando en 30 días  
**Presupuesto marketing**: 0€ (todo orgánico hasta el primer ingreso)

---

## SEMANA 1 — Cimientos (lo que debes hacer tú)

### Cuentas que tienes que crear manualmente

| Red | Nombre sugerido | URL objetivo | Prioridad |
|-----|----------------|-------------|-----------|
| LinkedIn Company Page | NEXIA — Agencia de IA | linkedin.com/company/nexia-ia | 🔴 MUY ALTA |
| Instagram | @nexia.ia | instagram.com/nexia.ia | 🔴 MUY ALTA |
| TikTok | @nexia_ia | tiktok.com/@nexia_ia | 🟡 ALTA |
| YouTube | @NexiaIA | youtube.com/@nexiaIA | 🟡 ALTA |
| Facebook | NEXIA Agencia IA | - | 🟢 MEDIA |

**Email agencia** (crea cuenta Google para):
- hola@nexia.io (si nexia.io no está disponible: nexia-ia.com o nexiaagencia.com)
- Una vez creado, ejecuta: `mundo-agencia/herramientas/conectar-gdrive.bat`

### Perfil personal LinkedIn (el tuyo, como Director)
Actualiza tu bio a:
> "Director de NEXIA | Ayudo a PYMEs a automatizar procesos con IA | Chatbots, Apps y Sistemas a medida"

---

## SEMANA 1-2 — Outreach Directo (200 contactos mínimo)

### Script de uso rápido

```powershell
# Genera mensaje para cualquier empresa
cd "D:\Proyectos claude\mundo-ventas\herramientas"

# Ejemplos por sector:
python outreach-linkedin.py --empresa "Clínica Dental García" --contacto "Dr. García" --sector "salud" --canal "linkedin"
python outreach-linkedin.py --empresa "Hotel Mediterráneo" --contacto "María López" --sector "hosteleria" --canal "email"
python outreach-linkedin.py --empresa "Despacho Ruiz & Asociados" --contacto "Carlos Ruiz" --sector "legal" --canal "linkedin"
python outreach-linkedin.py --empresa "Inmobiliaria Costa Sol" --contacto "Ana Martínez" --sector "inmobiliaria" --canal "linkedin"
python outreach-linkedin.py --empresa "Centro Wellness Madrid" --contacto "Laura" --sector "clinica_estetica" --canal "email"
```

**Sectores disponibles**: salud, hosteleria, legal, ecommerce, inmobiliaria, restaurante, formacion, logistica, clinica_estetica

### Dónde encontrar contactos (GRATIS)

1. **LinkedIn** — Busca: "dueño clínica [ciudad]", "director hotel [ciudad]", "gerente restaurante"
2. **Google Maps** — Busca negocios locales, busca su web, encuentra el email de contacto
3. **Instagram** — Busca por hashtags del sector + ciudad
4. **Páginas Amarillas** — Directorio de empresas con emails

### Meta diaria (lunes a viernes)
- 20 solicitudes de conexión LinkedIn (con nota personalizada)
- 10 emails fríos
- 5 seguimientos de días anteriores

---

## SEMANA 2-3 — Contenido Social (ya automatizado)

Los 35 posts están siendo generados por IA en:
`D:\Proyectos claude\mundo-social-media\contenido-nexia\`

**Calendario de publicación sugerido**:
- Instagram: 1 post/día + 2 Stories/día
- LinkedIn: 1 post cada 2 días
- TikTok: 1 vídeo/semana (puedes reutilizar reels de Instagram)

**Herramienta gratuita de programación**: Buffer.com (free plan = 3 canales + 10 posts en cola)

---

## SEMANA 3-4 — Propuestas y Cierre

Cuando alguien responda interesado:

1. **Llamada de descubrimiento** (30 min, por Zoom/Meet)
   - ¿Cuál es su mayor problema ahora mismo?
   - ¿Cuánto les cuesta ese problema por mes?
   - ¿Han intentado solucionarlo antes? ¿Cómo?

2. **Genera propuesta en 5 minutos**:
   ```
   Ejecuta la API de la agencia:
   POST http://localhost:8080/ventas/propuesta
   {"empresa": "nombre", "problema": "descripción", "presupuesto": 1497}
   ```

3. **Envía propuesta** y da 48h para decidir

4. **Seguimiento**: si no hay respuesta en 48h, llama/escribe personalmente

---

## Pricing de lanzamiento (primeros 5 clientes)

| Paquete | Precio normal | Precio lanzamiento | Entrega |
|---------|--------------|-------------------|---------|
| Starter | 497€ | 297€ (40% dto) | 5 días |
| Growth | 1,497€ | 997€ (33% dto) | 3 semanas |
| Agency Pro | 4,997€ | 3,497€ (30% dto) | 6 semanas |

**Argumento**: "Somos nuevos y buscamos 5 casos de éxito. A cambio de precio especial, te pido permiso para usar tu caso como referencia."

---

## KPIs semanales

| Métrica | Objetivo semana 1 | Objetivo semana 2 | Objetivo semana 4 |
|---------|-----------------|-----------------|-----------------|
| Conexiones LinkedIn | 100 | 200 | 400 |
| Emails enviados | 50 | 100 | 200 |
| Respuestas recibidas | 5 | 15 | 30 |
| Llamadas agendadas | 1 | 3 | 8 |
| Propuestas enviadas | 0 | 1 | 4 |
| Clientes cerrados | 0 | 0 | 1-2 |

---

## El pitch de 30 segundos (apréndetelo)

> "Hola [nombre], soy de NEXIA. Ayudamos a negocios como [empresa] a automatizar la atención al cliente con IA — el tipo de cosas que normalmente requieren 2 empleados, nosotros las hacemos con un chatbot por 497€. ¿Tienes 20 minutos esta semana para ver si encaja?"

---

## Acciones de hoy (prioridad máxima)

- [ ] Crear cuenta LinkedIn Company Page para NEXIA
- [ ] Crear Instagram @nexia.ia
- [ ] Crear email de agencia (Google Workspace o Gmail)
- [ ] Actualizar bio de LinkedIn personal
- [ ] Enviar primeras 20 solicitudes de conexión (sector: salud o hostelería)
- [ ] Crear cuenta en cal.com/nexia para reuniones
- [ ] Revisar y publicar primer post en Instagram (está en contenido-nexia/)
