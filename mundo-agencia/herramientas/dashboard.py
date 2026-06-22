# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""Dashboard ejecutivo de la agencia."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import os
import re
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).parent.parent.parent  # D:\Proyectos claude

def leer_archivo(ruta):
    try:
        return Path(ruta).read_text(encoding="utf-8")
    except:
        return ""

def contar_leads(crm):
    leads = re.findall(r'\| L\d+', crm)
    ganados = re.findall(r'ganado', crm, re.IGNORECASE)
    return len(leads), len(ganados)

def extraer_mrr(facturacion):
    match = re.search(r'MRR.*?(\d+)€/mes', facturacion)
    return match.group(1) if match else "0"

def main():
    print("\n" + "="*50)
    print("  AGENCIA IA — DASHBOARD EJECUTIVO")
    print(f"  {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("="*50)

    crm = leer_archivo(BASE / "mundo-agencia/memoria/clientes.md")
    facturacion = leer_archivo(BASE / "mundo-agencia/memoria/facturacion.md")
    estado = leer_archivo(BASE / "mundo-agencia/memoria/estado-fase.md")

    total_leads, clientes_ganados = contar_leads(crm)
    mrr = extraer_mrr(facturacion)

    print(f"\n[VENTAS]")
    print(f"   Leads en pipeline: {max(0, total_leads - 1)}")
    print(f"   Clientes activos:  {clientes_ganados}")
    print(f"   MRR actual:        {mrr} EUR/mes")

    # Proyectos activos
    proyectos = list(Path(BASE / "mundo-dev-clientes/proyectos").glob("*/") ) if (BASE / "mundo-dev-clientes/proyectos").exists() else []
    print(f"\n[PROYECTOS]")
    print(f"   En desarrollo:     {len(proyectos)}")
    for p in proyectos[:5]:
        print(f"   -> {p.name}")

    # Mundos activos
    mundos = [d.name for d in BASE.glob("mundo-*/") if d.is_dir()]
    print(f"\n[MUNDOS ACTIVOS: {len(mundos)}]")
    for m in mundos:
        print(f"   + {m}")

    print(f"\n[FASE: PRE-CLIENTE — usando modelos gratuitos]")
    print(f"   Objetivo: conseguir primer proyecto 500-2.000 EUR")
    print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    main()
