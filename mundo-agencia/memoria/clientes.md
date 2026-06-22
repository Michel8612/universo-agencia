# CRM — Base de Clientes y Leads

## LEADS ACTIVOS
| ID | Nombre/Empresa | Sector | Servicio Interés | Presupuesto | Estado | Próxima Acción | Fecha |
|----|---------------|--------|-----------------|-------------|--------|----------------|-------|
| L001 | - | - | - | - | - | Conseguir primer lead | 2026-06-19 |

## CLIENTES ACTIVOS
| ID | Cliente | Servicio | Monto | Inicio | Estado | Próximo Cobro |
|----|---------|---------|-------|--------|--------|--------------|
| - | Sin clientes aún | - | - | - | - | - |

## Pipeline de Ventas
| Fase | Cantidad | Valor estimado |
|------|----------|---------------|
| Leads nuevos | 0 | - |
| Propuesta enviada | 0 | - |
| Negociación | 0 | - |
| Clientes activos | 0 | - |
| **MRR total** | - | **0€/mes** |

## Template de Ficha de Cliente
```
### [NOMBRE EMPRESA] — [FECHA ALTA]
- Contacto: nombre, email, teléfono
- Servicio: 
- Precio: 
- Estado: Prospecto / Activo / Completado
- Próxima acción:
- Notas:
```

## Cómo cambiar estado de un lead
nuevo → contactado → propuesta_enviada → negociando → ganado / perdido
Cuando esté en "ganado": mover a CLIENTES ACTIVOS y crear carpeta en mundo-dev-clientes/proyectos/
