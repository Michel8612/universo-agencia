# Sala VIP de Telegram — solo para leads CALENTADOS

Objetivo: un espacio privado donde **solo entran leads ya cualificados** (calentados),
para ofrecerles el servicio sin ruido ni curiosos.

## Cómo funciona (diseño)

```
Web → botón Telegram → el lead abre chat con @Jarvistrading2026_bot
        ↓
El bot conversa y CALIENTA el lead (preguntas, diagnóstico, interés)
        ↓
Cuando el lead está "calentado" (regla tuya: respondió, pidió precio, score alto…)
        ↓
El bot genera un ENLACE DE INVITACIÓN ÚNICO (1 uso, caduca) y se lo envía
        ↓
El lead entra a la SALA VIP privada → ahí se le ofrece el servicio
```

La sala es **privada y sin enlace público**: nadie entra por su cuenta. Solo se entra
con un enlace de un solo uso que el bot da a los leads aprobados. Control total.

## Setup (en la PC donde corre el bot)

1. **Crea el grupo privado** en Telegram (ej. *"NEXIA · Clientes VIP"*).
2. **Añade tu bot** `@Jarvistrading2026_bot` como **administrador** con el permiso
   *"Invitar usuarios mediante enlace"* activado.
3. **Consigue el chat_id** del grupo (número negativo, ej. `-1001234567890`):
   - Truco rápido: añade `@RawDataBot` al grupo unos segundos y te lo muestra; luego lo quitas.
   - O por API: `getUpdates` tras escribir algo en el grupo.
4. **Pon en `.env`:**
   ```
   TELEGRAM_BOT_TOKEN=123456:ABC...        # de @BotFather
   TELEGRAM_SALA_CHAT_ID=-1001234567890
   ```

## Uso

Script: `mundo-ventas/herramientas/telegram_sala.py`

```bash
# Enviar invitación a un lead concreto (debe haber escrito antes al bot):
python telegram_sala.py --invitar 123456789 --nombre "Carlos"

# Solo generar un enlace de un solo uso (para pruebas):
python telegram_sala.py --link
```

Desde el código del bot (cuando detectes que el lead está calentado):
```python
from telegram_sala import invitar_lead
invitar_lead(user_id, nombre="Carlos")   # crea enlace único + se lo manda
```

## Definir "lead calentado" (regla a decidir)

Elige tu disparador (uno o varios):
- Respondió ≥ N mensajes al bot, o
- Pidió precio / dijo "me interesa", o
- Score IA ≥ 7 (la función `clasificar_lead` del scraper ya puntúa 1-10), o
- Rellenó el formulario de la web y luego abrió el bot.

Cuando se cumpla, el bot llama a `invitar_lead(...)`. Pendiente: conectar este
disparador dentro de la lógica del bot (que vive en tu PC).

## Notas / límites

- Telegram **no deja** al bot escribir a un usuario que no haya iniciado chat con él
  primero. Por eso el flujo entra por el botón de la web → el lead abre el bot.
- Los enlaces caducan (por defecto 120 min) y son de 1 uso → no se reenvían ni filtran.
- Si prefieres, se puede cambiar a modo "solicitud de unión con aprobación" del bot
  (`creates_join_request=True` en `crear_invitacion`) — dímelo y lo ajusto.
