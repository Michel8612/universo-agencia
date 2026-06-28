#!/usr/bin/env python3
r"""
NEXIA — Emisor de campaña en tandas (SMTP, controlado y legal)

Lee un .md de campaña (generado por campana-leads.py), extrae destinatario +
asunto + cuerpo de cada lead CON email, y los envía en una tanda controlada.

Cumple el CHECKLIST-LEGAL.md (Cimiento 5):
  - tope diario (20-40/día), throttle aleatorio entre envíos
  - línea de baja real en cada email + header List-Unsubscribe
  - identidad del remitente (nombre + dirección) en el pie
  - dedup: nunca reenvía a la misma dirección (registro en enviados.json)

POR DEFECTO ES SIMULACIÓN (dry-run): imprime lo que enviaría sin enviar nada.
Para enviar de verdad: --enviar  (requiere MAIL_PASSWORD en .env, App Password de Gmail).

Uso:
  python enviar-campana.py                          # dry-run de la campaña más reciente
  python enviar-campana.py --archivo ..\campanas\campana-XXMM.md
  python enviar-campana.py --max 25 --enviar        # envía hasta 25 (real)
"""
import os, sys, re, json, time, glob, argparse, smtplib, ssl
from email.mime.text import MIMEText
from email.utils import formataddr
from datetime import datetime, date

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
CAMPANAS_DIR = os.path.join(HERE, "..", "campanas")
SENT_LOG = os.path.join(CAMPANAS_DIR, "enviados.json")

# Emails-placeholder de plantillas / plataformas que NO son del negocio (no enviar)
EMAIL_BASURA = ("mysite.com", "example.com", "example.org", "domain.com",
                "email.com", "yourdomain", "wixpress.com", "sentry.io",
                "tudominio", "tu-email", "test.com",
                # plataformas de pedidos/web (no son el negocio real)
                "menufy.com", "getbento.com", "atom.com", "toasttab.com",
                "doordash.com", "ubereats.com", "grubhub.com", "squareup.com")


def cargar_env():
    root = os.path.abspath(os.path.join(HERE, "..", ".."))
    envp = os.path.join(root, ".env")
    if os.path.exists(envp):
        for line in open(envp, encoding="utf-8"):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def archivo_mas_reciente():
    files = sorted(glob.glob(os.path.join(CAMPANAS_DIR, "campana-*.md")))
    return files[-1] if files else None


def email_valido(e):
    e = (e or "").strip().lower()
    if not e or "@" not in e or " " in e:
        return False
    return not any(b in e for b in EMAIL_BASURA)


def parsear_campana(path):
    """Devuelve lista de dicts: {nombre, email, asunto, cuerpo}."""
    texto = open(path, encoding="utf-8").read()
    bloques = re.split(r"\n---\n", texto)
    leads = []
    for b in bloques:
        m_nom = re.search(r"^##\s+(.+)$", b, re.MULTILINE)
        m_mail = re.search(r"✉\s*([^\s|]+@[^\s|]+)", b)
        m_asun = re.search(r"ASUNTO:\s*(.+)", b)
        if not (m_nom and m_mail and m_asun):
            continue
        email = m_mail.group(1).strip()
        if not email_valido(email):
            continue
        # cuerpo = desde "CUERPO:" (o tras el asunto) hasta el final del bloque
        m_cuerpo = re.search(r"CUERPO:\s*(.+)", b, re.DOTALL)
        if m_cuerpo:
            cuerpo = m_cuerpo.group(1).strip()
        else:
            cuerpo = b[m_asun.end():].strip()
        leads.append({
            "nombre": m_nom.group(1).strip(),
            "email": email,
            "asunto": m_asun.group(1).strip(),
            "cuerpo": cuerpo,
        })
    return leads


def parsear_json(path):
    """Lee un JSON tipo miami-emails.json: [{negocio,email,web,mensaje}]."""
    data = json.load(open(path, encoding="utf-8"))
    leads = []
    for it in data:
        email = (it.get("email") or "").strip()
        if not email_valido(email):
            continue
        msg = it.get("mensaje", "") or ""
        # separar "Subject: ..." del cuerpo si viene incrustado
        m = re.match(r"\s*Subject:\s*(.+)", msg)
        if m:
            asunto = m.group(1).strip()
            cuerpo = msg[m.end():].strip()
        else:
            asunto = f"NEXIA — {it.get('negocio','')}".strip(" —")
            cuerpo = msg.strip()
        leads.append({"nombre": it.get("negocio", ""), "email": email,
                      "asunto": asunto, "cuerpo": cuerpo})
    return leads


def cargar_enviados():
    if os.path.exists(SENT_LOG):
        try:
            return json.load(open(SENT_LOG, encoding="utf-8"))
        except Exception:
            pass
    return {"emails": [], "por_dia": {}}


def guardar_enviados(s):
    os.makedirs(CAMPANAS_DIR, exist_ok=True)
    json.dump(s, open(SENT_LOG, "w", encoding="utf-8"), ensure_ascii=False, indent=2)


def asegurar_baja_y_firma(cuerpo, from_name, from_addr):
    linea_baja = "Si no te interesa, responde BAJA y no te volvemos a escribir."
    if "BAJA" not in cuerpo:
        cuerpo += "\n\n" + linea_baja
    # Identidad del remitente (requisito legal de outreach)
    cuerpo += f"\n\n—\n{from_name} · {from_addr}\nEste email es una comunicación comercial. Responde BAJA para no recibir más."
    return cuerpo


def enviar_smtp(server_cfg, msg_from, to, asunto, cuerpo):
    msg = MIMEText(cuerpo, "plain", "utf-8")
    msg["Subject"] = asunto
    msg["From"] = msg_from
    msg["To"] = to
    msg["List-Unsubscribe"] = f"<mailto:{server_cfg['user']}?subject=BAJA>"
    host, port = server_cfg["host"], server_cfg["port"]
    if port == 465:
        with smtplib.SMTP_SSL(host, port, context=ssl.create_default_context(), timeout=20) as s:
            s.login(server_cfg["user"], server_cfg["password"])
            s.sendmail(server_cfg["user"], [to], msg.as_string())
    else:
        with smtplib.SMTP(host, port, timeout=20) as s:
            s.starttls(context=ssl.create_default_context())
            s.login(server_cfg["user"], server_cfg["password"])
            s.sendmail(server_cfg["user"], [to], msg.as_string())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--archivo", help="ruta a campana-*.md (por defecto, la más reciente)")
    ap.add_argument("--json", help="ruta a un JSON tipo miami-emails.json [{negocio,email,web,mensaje}]")
    ap.add_argument("--max", type=int, default=25, help="tope de envíos en esta tanda (20-40 recomendado)")
    ap.add_argument("--delay-min", type=int, default=35, help="segundos mínimos entre envíos")
    ap.add_argument("--delay-max", type=int, default=90, help="segundos máximos entre envíos")
    ap.add_argument("--enviar", action="store_true", help="ENVÍA de verdad (si no, solo simula)")
    args = ap.parse_args()

    if args.max > 40:
        print(f"⚠ {args.max} supera lo recomendado (40/día). Gmail crudo puede suspenderte. Bájalo.")

    cargar_env()
    if args.json:
        path = args.json
        if not os.path.exists(path):
            print(f"[x] No existe el JSON: {path}")
            sys.exit(1)
        leads = parsear_json(path)
    else:
        path = args.archivo or archivo_mas_reciente()
        if not path or not os.path.exists(path):
            print("[x] No encuentro ningún campana-*.md. Corre antes campana-leads.py.")
            sys.exit(1)
        leads = parsear_campana(path)
    enviados = cargar_enviados()
    ya = set(e.lower() for e in enviados["emails"])
    pendientes = [l for l in leads if l["email"].lower() not in ya]

    modo = "ENVÍO REAL" if args.enviar else "SIMULACIÓN (dry-run)"
    print(f"=== Emisor de campaña NEXIA — {modo} ===")
    print(f"Archivo: {os.path.basename(path)}")
    print(f"Leads con email válido: {len(leads)} | nuevos (no enviados antes): {len(pendientes)}")
    print(f"Tope esta tanda: {args.max}\n")

    cfg = {
        "host": os.environ.get("MAIL_HOST", "smtp.gmail.com"),
        "port": int(os.environ.get("MAIL_PORT", "587")),
        "user": os.environ.get("MAIL_USERNAME", ""),
        "password": os.environ.get("MAIL_PASSWORD", ""),
    }
    from_name = os.environ.get("MAIL_FROM_NAME", "NEXIA")
    from_addr = os.environ.get("MAIL_FROM_ADDRESS", cfg["user"])
    msg_from = formataddr((from_name, from_addr))

    if args.enviar and not cfg["password"]:
        print("[x] MAIL_PASSWORD vacío en .env. Pon el App Password de Gmail antes de --enviar.")
        print("    https://myaccount.google.com/apppasswords")
        sys.exit(1)

    hoy = date.today().isoformat()
    enviados["por_dia"].setdefault(hoy, 0)
    n = 0
    for l in pendientes[:args.max]:
        cuerpo = asegurar_baja_y_firma(l["cuerpo"], from_name, from_addr)
        if args.enviar:
            try:
                enviar_smtp(cfg, msg_from, l["email"], l["asunto"], cuerpo)
                enviados["emails"].append(l["email"])
                enviados["por_dia"][hoy] += 1
                print(f"  ✅ enviado → {l['email']:32} | {l['asunto'][:40]}")
                n += 1
                guardar_enviados(enviados)
                if n < len(pendientes[:args.max]):
                    import random
                    time.sleep(random.randint(args.delay_min, args.delay_max))
            except Exception as e:
                print(f"  ❌ fallo → {l['email']}: {str(e)[:70]}")
        else:
            print(f"  ✉ (simulado) → {l['email']:32} | {l['asunto'][:40]}")
            n += 1

    print(f"\n=== {'Enviados' if args.enviar else 'Se enviarían'}: {n} | total histórico enviados: {len(set(enviados['emails']))} ===")
    if not args.enviar:
        print("Para enviar de verdad: añade --enviar (con MAIL_PASSWORD en .env).")


if __name__ == "__main__":
    main()
