# NEXIA — Docker (n8n estable, sin depender del arranque de Windows)

Objetivo: que **n8n** (y opcionalmente Ollama) corran 24/7 en Docker con `restart:
unless-stopped`, en vez del arranque automático + watchdog de la PC que no levanta bien.

## Arrancar
```bash
cd docker
docker compose up -d          # n8n en http://localhost:5678
docker compose logs -f n8n    # ver que arranca
```
Con Ollama local también:
```bash
docker compose --profile ollama up -d
docker exec -it nexia-ollama ollama pull qwen2.5:14b   # 1ª vez, baja el modelo
```

## Migrar lo que ya tienes
1. **Quitar el arranque automático viejo de n8n** (Task Scheduler `n8n-agencia` +
   watchdog `n8n-watchdog.ps1`) para que no choque con el de Docker.
2. n8n en Docker guarda sus datos en el volumen `n8n_data` (persisten entre reinicios).
   Para traer tus workflows: en el n8n viejo, *Export* del workflow → en el nuevo, *Import*.
   (Los JSON del repo están montados en `/workflows` dentro del contenedor, solo lectura.)
3. **API Flask + campañas**: siguen en el host por ahora (usan rutas de Windows y
   `D:\Proyectos claude`). n8n las llama con `http://host.docker.internal:8080`
   (variable `NEXIA_API` ya inyectada en el contenedor).

## Webhook
Si usas el webhook de n8n desde fuera de la máquina, define `WEBHOOK_URL` antes de subir:
```bash
WEBHOOK_URL=https://tu-dominio-o-tailscale:5678/ docker compose up -d
```

## Por hacer (fase siguiente)
- Dockerizar también la **API Flask** (requiere hacer `BASE` configurable por env y, para
  el endpoint de vídeo, ffmpeg+fuentes en la imagen). Lo vemos cuando definamos el panel.
- Conectar todo al **panel/frontend** de la agencia.
