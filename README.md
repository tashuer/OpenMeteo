# Clima de Bogotá con Open-Meteo

Script en Python que consulta la API pública de [Open-Meteo](https://open-meteo.com/) y muestra el clima de Bogotá de hoy: condiciones actuales y resumen del día.

- No necesita llave de acceso (API key) ni registro.
- No tiene dependencias externas: usa solo la biblioteca estándar de Python.

## Requisitos

- Python 3.8 o superior
- Conexión a internet

## Uso

```bash
python clima_bogota.py
```

El script imprime primero la respuesta cruda de la API (JSON) y luego un resumen legible.

## Ejemplo de salida

```
=== Clima de Bogotá ===
Fecha: 2026-10-06  (zona horaria: America/Bogota, altitud: 2557 m)

Ahora mismo:
  Condición:        Llovizna densa
  Temperatura:      14.7 °C
  Sensación térmica:15.4 °C
  Humedad:          93 %
  Precipitación:    0.3 mm
  Viento:           3.1 km/h (dirección 111°)

Resumen del día:
  Condición:        Chubascos moderados
  Máx / Mín:        23.3 / 11.3 °C
  Lluvia total:     9.7 mm
  Prob. de lluvia:  100 %
  Amanecer:         05:42
  Atardecer:        17:45
```

## Cómo funciona

El script hace una petición `GET` al endpoint de pronóstico de Open-Meteo:

```
https://api.open-meteo.com/v1/forecast
```

con estos parámetros principales:

| Parámetro | Valor | Descripción |
|---|---|---|
| `latitude`, `longitude` | 4.7110, -74.0721 | Coordenadas de Bogotá |
| `timezone` | `America/Bogota` | Las horas se devuelven en hora local |
| `forecast_days` | 1 | Solo el día de hoy |
| `current` | temperatura, humedad, sensación térmica, precipitación, código del tiempo, viento | Condiciones actuales (se actualizan cada 15 min) |
| `daily` | código del tiempo, máx/mín, lluvia total, probabilidad de lluvia, amanecer, atardecer | Resumen del día |

### Campos de la respuesta

- **`current`**: medición actual. `temperature_2m` y `relative_humidity_2m` se miden a 2 m del suelo, `wind_speed_10m` y `wind_direction_10m` a 10 m. `apparent_temperature` es la sensación térmica. `precipitation` es la lluvia acumulada en el último intervalo.
- **`daily`**: resumen del día. Cada campo es una lista con un elemento por día pedido.
- **`weather_code`**: código [WMO](https://open-meteo.com/en/docs#weathervariables) de la condición del tiempo (por ejemplo, 0 = despejado, 55 = llovizna densa, 81 = chubascos moderados). El script lo traduce a texto con el diccionario `WMO`.
- **`*_units`**: unidades de cada campo (°C, %, mm, km/h, etc.).

Los datos provienen de un modelo meteorológico para una celda de la cuadrícula cercana a las coordenadas pedidas, no de una estación puntual. Por eso la latitud y longitud devueltas pueden diferir ligeramente de las enviadas.

## Personalización

Para consultar otra ciudad, cambia `latitude` y `longitude` (y `timezone`) en el diccionario `PARAMS` de [clima_bogota.py](clima_bogota.py). Para agregar más variables, consulta la [documentación de la API](https://open-meteo.com/en/docs) y añádelas a `current` o `daily`.

## Licencia y atribución

Open-Meteo ofrece su API gratuita para uso no comercial y exige atribución. Consulta sus [términos de uso](https://open-meteo.com/en/terms) antes de usarla en otros contextos.
