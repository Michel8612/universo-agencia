#!/usr/bin/env python3
"""
NEXIA — Sala VIP de Telegram para leads CALENTADOS.

Idea: un grupo/canal PRIVADO al que NO se entra con un enlace publico. El bot
(@Jarvistrading2026_bot) genera un enlace de invitacion de UN SOLO USO y con
caducidad, y solo se lo envia a un lead cuando ya esta calentado (cualificado).
Asi solo entran los que tu sistema ha aprobado.

Requisitos (en la PC donde corre el bot):
  1. Crea un grupo privado de Telegram (ej. "NEXIA · Clientes VIP").
  2. Anade tu bot como ADMINISTRADOR con permiso "Invitar usuarios mediante enlace".
  3. Saca el chat_id del grupo (negativo, ej. -1001234567890). Truco: anade
     @RawDataBot al grupo un momento, o usa getUpdates.
  4. Pon en .env:
       TELEGRAM_BOT_TOKEN=123456:ABC...        (token de @BotFather)
       TELEGRAM_SALA_CHAT_ID=-1001234567890

Flujo recomendado:
  Web -> boton Telegram -> el lead abre chat con el bot -> el bot lo cualifica
  (conversacion) -> cuando esta CALENTADO, el bot llama a invitar_lead(user_id)
  -> recibe un enlace unico para entrar a la sala VIP.

Uso manual / pruebas:
  python telegram_sala.py --invitar 123456789      # envia invitacion a ese user_id
  python telegram_sala.py --link                    # solo genera un enlace de 1 uso
"""
import os, json, time, argparse, urllib.request

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
SALA  = os.environ.get("TELEGRAM_SALA_CHAT_ID", "").strip()
API   = f"https://api.telegram.org/bot{TOKEN}"


def _post(metodo, params, timeout=15):
    if not TOKEN:
        raise RuntimeError("Falta TELEGRAM_BOT_TOKEN en el entorno (.env)")
    data = json.dumps(params).encode()
    req = urllib.request.Request(f"{API}/{metodo}", data=data,
                                 headers={"Content-Type": "application/json"})
    r = json.loads(urllib.request.urlopen(req, timeout=timeout).read())
    if not r.get("ok"):
        raise RuntimeError(f"Telegram API error en {metodo}: {r}")
    return r["result"]


def crear_invitacion(expira_min=120, usos=1, titulo="Lead calentado"):
    """Crea un enlace de invitacion de un solo uso (por defecto) a la sala VIP."""
    if not SALA:
        raise RuntimeError("Falta TELEGRAM_SALA_CHAT_ID en el entorno (.env)")
    res = _post("createChatInviteLink", {
        "chat_id": SALA,
        "name": titulo[:32],
        "expire_date": int(time.time()) + expira_min * 60,
        "member_limit": usos,
        "creates_join_request": False,
    })
    return res["invite_link"]


def enviar(user_id, texto):
    """Envia un mensaje del bot a un usuario (debe haber iniciado chat con el bot)."""
    return _post("sendMessage", {"chat_id": user_id, "text": texto,
                                 "parse_mode": "HTML", "disable_web_page_preview": True})


def invitar_lead(user_id, nombre="", expira_min=120):
    """Genera un enlace unico y se lo envia al lead con el pitch de la sala VIP."""
    link = crear_invitacion(expira_min=expira_min, titulo=f"VIP {nombre}".strip())
    saludo = f"Hola{(' ' + nombre) if nombre else ''} 👋"
    texto = (
        f"{saludo}\n\n"
        f"Te damos acceso a nuestra <b>sala privada de clientes NEXIA</b>, donde "
        f"compartimos propuestas, casos y ofertas solo para negocios seleccionados.\n\n"
        f"👉 Entra aquí (enlace personal, válido {expira_min} min y de un solo uso):\n{link}"
    )
    enviar(user_id, texto)
    return link


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--invitar", help="user_id de Telegram al que enviar la invitacion")
    ap.add_argument("--nombre", default="", help="nombre del lead (opcional)")
    ap.add_argument("--link", action="store_true", help="solo imprime un enlace de 1 uso")
    ap.add_argument("--expira", type=int, default=120, help="minutos de validez del enlace")
    args = ap.parse_args()

    if args.link:
        print(crear_invitacion(expira_min=args.expira))
    elif args.invitar:
        link = invitar_lead(args.invitar, nombre=args.nombre, expira_min=args.expira)
        print(f"Invitacion enviada a {args.invitar}: {link}")
    else:
        ap.print_help()
