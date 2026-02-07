# Pronosticador de resultados (Europa)

App sencilla en Python para pronosticar resultados entre equipos europeos de primera y segunda división usando un modelo Elo simplificado. Incluye una estructura de datos extensible para agregar ligas y equipos.

## Requisitos

- Python 3.10+

## Uso rápido

```bash
python app.py --league "LaLiga" --home "Real Madrid" --away "Barcelona"
```

Para listar ligas y equipos disponibles:

```bash
python app.py --list-leagues
python app.py --list-teams --league "LaLiga"
```

## Datos

Los datos viven en `data/teams.csv`. Puedes añadir más ligas/temporadas con tu propia fuente.

## Nota

Este proyecto es un punto de partida (modelo simple). Para mayor precisión, integra datos históricos y calibra el modelo.
