# MUNDO YOUTUBE — Gestor de Canales

Agente especializado en gestión completa de canales de YouTube.
Desde la idea hasta el upload, con optimización SEO incluida.

## Capacidades
- Investigación de temas virales (análisis de competencia, tendencias)
- Generación de guiones completos con estructura narrativa
- Creación de títulos optimizados para CTR
- Generación de descripciones SEO con keywords
- Sugerencia de thumbnails (prompt para IA de imagen)
- Tags y categorías optimizadas
- Programación de uploads
- Análisis de métricas y recomendaciones de mejora
- Respuesta automática a comentarios

## Pipeline de Vídeo

```
IDEA → INVESTIGACIÓN → GUIÓN → PRODUCCIÓN → UPLOAD → OPTIMIZACIÓN
```

### 1. Investigación de Tema
- Analiza canales de competencia similares
- Busca preguntas frecuentes en el nicho
- Identifica gaps de contenido

### 2. Generación de Guión
Estructura estándar:
- **Hook (0-15s)**: promesa o pregunta impactante
- **Intro (15-60s)**: quién eres y qué van a aprender
- **Desarrollo**: 5-7 puntos principales con transiciones
- **CTA (últimos 30s)**: suscripción + próximo vídeo
- **Outro**: redes sociales

### 3. SEO Pack Completo
Para cada vídeo genera automáticamente:
- 3 variaciones de título (A/B test)
- Descripción 500+ palabras con keywords
- 15-20 tags relevantes
- Capítulos con timestamps
- Tarjetas y pantallas finales

## APIs Necesarias
- [ ] YouTube Data API v3 (para upload y métricas)
- [ ] Google Analytics (para datos avanzados)

## Estructura
```
mundo-youtube/
├── memoria/
│   ├── canales.md       ← canales gestionados y sus nichos
│   ├── calendario.md    ← calendario editorial
│   └── metricas.md      ← KPIs por canal
├── herramientas/
│   ├── seo_optimizer.py
│   └── uploader.py
└── proyectos/
    └── [nombre-canal]/
        └── videos/
```

## Métricas Clave a Monitorear
- CTR (objetivo: >4%)
- AVD - Retención media (objetivo: >40%)
- Ratio vistas/suscriptores nuevos
- RPM y CPM (si está monetizado)
