# NEXIA — Inicio Rápido

> **Leer esto primero.** Todo lo que está listo y todo lo que debes hacer tú.

---

## LO QUE TIENES LISTO AHORA MISMO

### Herramientas que puedes usar HOY

| Herramienta | Uso | Comando |
|-------------|-----|---------|
| **Outreach LinkedIn/Email** | Genera mensajes personalizados por sector | `cd mundo-ventas/herramientas && python outreach-linkedin.py --empresa "X" --sector "salud" --canal "linkedin"` |
| **Propuesta comercial** | Genera propuesta completa en PDF/MD | `cd mundo-ventas/herramientas && python generar-propuesta.py --empresa "X" --sector "salud" --presupuesto 1497` |
| **Demo Chatbot** | Muestra a clientes cómo funciona | `cd mundo-chatbots/herramientas && python demo-chatbot-local.py --sector salud --nombre "Clínica García"` |
| **API Central** | Orquesta todos los servicios | Está corriendo en `http://localhost:8080` |
| **Contenido social** | 35 posts generados por IA | En `mundo-social-media/contenido-nexia/` (cuando termine el face-swap) |
| **Landing NEXIA** | Web lista para publicar | `mundo-ventas/web-nexia/out/` — arrastra a netlify.com/drop |

### Sectores del outreach (10 disponibles)
`salud` · `hosteleria` · `legal` · `ecommerce` · `inmobiliaria` · `restaurante` · `formacion` · `logistica` · `clinica_estetica` + más

---

## PROCESOS CORRIENDO AHORA (no los toques)

| Proceso | ETA | Resultado |
|---------|-----|---------|
| Face-swap Video 1 (trigueño + abuelo) | ~3h desde las 2AM | `mundo-multimedia/proyectos/face-swap/video1_trigueño_abuelo.mp4` |
| Face-swap Video 2 (naranja + gorra roja) | ~6h desde las 2AM | `mundo-multimedia/proyectos/face-swap/video2_naranja_gorraroja.mp4` |
| Generador de contenido (35 posts) | Auto tras face-swap | `mundo-social-media/contenido-nexia/posts_lanzamiento_FECHA.md` |

---

## LO QUE TÚ TIENES QUE HACER (no puedo hacerlo por ti)

### HOY — Alta prioridad

- [ ] **Ir a [app.netlify.com/drop](https://app.netlify.com/drop)** y arrastrar la carpeta `mundo-ventas/web-nexia/out/` → tu web estará en nexia-ia.netlify.app
- [ ] **Crear Company Page NEXIA en LinkedIn** (necesitas estar logueado en tu cuenta personal)
- [ ] **Crear cuenta Instagram** @nexia.ia (o @nexia_ia si está ocupado)
- [ ] **Crear cuenta Google para NEXIA** (para el email de agencia) → luego ejecuta `mundo-agencia/herramientas/conectar-gdrive.bat`

### MAÑANA — Para conseguir clientes

- [ ] **Crear cuenta en [cal.com](https://cal.com)** → configura agenda → URL: cal.com/nexia
- [ ] **Enviar 20 solicitudes de conexión LinkedIn** con el outreach generado
- [ ] **Enviar 10 emails fríos** a empresas locales de tu ciudad
- [ ] **Publicar primer post** en Instagram y LinkedIn (usar el contenido generado)

---

## FLUJO DE PRIMER CLIENTE

```
1. Encuentras una empresa interesante
   ↓
2. Generas el mensaje: python outreach-linkedin.py --empresa "..." --sector "..."
   ↓
3. Lo mandas manualmente en LinkedIn/email
   ↓
4. Responden interesados
   ↓
5. Haces llamada de 20 min (Zoom/Meet)
   ↓
6. Generas propuesta: python generar-propuesta.py --empresa "..."
   ↓
7. Envías propuesta, cierras, cobras 50% por adelantado
   ↓
8. Desarrollas con la agencia
   ↓
9. Entregas → cobras otro 50%
```

---

## ARQUITECTURA DE LA AGENCIA

```
D:\Proyectos claude\
├── mundo-ventas/          ← outreach, propuestas, landing NEXIA
├── mundo-chatbots/        ← demos + chatbot SaaS (futuro)
├── mundo-agencia/         ← API central (puerto 8080) + CRM
├── mundo-multimedia/      ← face-swap, vídeos IA
├── mundo-social-media/    ← contenido y publicación
├── mundo-dev-clientes/    ← proyectos de clientes
└── mundo-seo/             ← SEO (por construir)
```

---

## PRECIOS DE REFERENCIA (ya en los scripts)

| Servicio | Precio | Cuándo usarlo |
|---------|--------|--------------|
| Starter | 497€ | PYMEs pequeñas, primer contacto |
| Growth | 1,497€ | Empresa mediana con presupuesto |
| Agency Pro | 4,997€ | Empresas grandes, proyecto complejo |
| Mantenimiento | desde 49€/mes | Todos los clientes después de entrega |

---

*Actualizado: Junio 2026 | nexia.io | hola@nexia.io*
