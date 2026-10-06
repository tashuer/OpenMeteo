"""Consulta la API pública de Open-Meteo y muestra el clima de Bogotá de hoy.

No requiere llave de acceso ni librerías externas (solo la biblioteca estándar).
"""
import json
import urllib.parse
import urllib.request

URL = "https://api.open-meteo.com/v1/forecast"

PARAMS = {
    "latitude": 4.7110,
    "longitude": -74.0721,
    "timezone": "America/Bogota",
    "forecast_days": 1,
    "current": ",".join([
        "temperature_2m",
        "relative_humidity_2m",
        "apparent_temperature",
        "precipitation",
        "weather_code",
        "wind_speed_10m",
        "wind_direction_10m",
    ]),
    "daily": ",".join([
        "weather_code",
        "temperature_2m_max",
        "temperature_2m_min",
        "precipitation_sum",
        "precipitation_probability_max",
        "sunrise",
        "sunset",
    ]),
}

# Códigos WMO de condición del tiempo, tal como los usa Open-Meteo.
WMO = {
    0: "Despejado", 1: "Mayormente despejado", 2: "Parcialmente nublado", 3: "Nublado",
    45: "Niebla", 48: "Niebla con escarcha",
    51: "Llovizna ligera", 53: "Llovizna moderada", 55: "Llovizna densa",
    56: "Llovizna helada ligera", 57: "Llovizna helada densa",
    61: "Lluvia ligera", 63: "Lluvia moderada", 65: "Lluvia fuerte",
    66: "Lluvia helada ligera", 67: "Lluvia helada fuerte",
    71: "Nevada ligera", 73: "Nevada moderada", 75: "Nevada fuerte", 77: "Granos de nieve",
    80: "Chubascos ligeros", 81: "Chubascos moderados", 82: "Chubascos violentos",
    85: "Chubascos de nieve ligeros", 86: "Chubascos de nieve fuertes",
    95: "Tormenta eléctrica", 96: "Tormenta con granizo ligero", 99: "Tormenta con granizo fuerte",
}


def obtener_clima():
    url = f"{URL}?{urllib.parse.urlencode(PARAMS)}"
    with urllib.request.urlopen(url, timeout=15) as respuesta:
        return json.load(respuesta)


def main():
    datos = obtener_clima()

    print("=== Respuesta cruda de la API ===")
    print(json.dumps(datos, indent=2, ensure_ascii=False))

    c, cu = datos["current"], datos["current_units"]
    d, du = datos["daily"], datos["daily_units"]

    print("\n=== Clima de Bogotá ===")
    print(f"Fecha: {d['time'][0]}  (zona horaria: {datos['timezone']}, altitud: {datos['elevation']:.0f} m)")
    print("\nAhora mismo:")
    print(f"  Condición:        {WMO.get(c['weather_code'], c['weather_code'])}")
    print(f"  Temperatura:      {c['temperature_2m']} {cu['temperature_2m']}")
    print(f"  Sensación térmica:{c['apparent_temperature']} {cu['apparent_temperature']}")
    print(f"  Humedad:          {c['relative_humidity_2m']} {cu['relative_humidity_2m']}")
    print(f"  Precipitación:    {c['precipitation']} {cu['precipitation']}")
    print(f"  Viento:           {c['wind_speed_10m']} {cu['wind_speed_10m']} "
          f"(dirección {c['wind_direction_10m']}{cu['wind_direction_10m']})")
    print("\nResumen del día:")
    print(f"  Condición:        {WMO.get(d['weather_code'][0], d['weather_code'][0])}")
    print(f"  Máx / Mín:        {d['temperature_2m_max'][0]} / {d['temperature_2m_min'][0]} {du['temperature_2m_max']}")
    print(f"  Lluvia total:     {d['precipitation_sum'][0]} {du['precipitation_sum']}")
    print(f"  Prob. de lluvia:  {d['precipitation_probability_max'][0]} {du['precipitation_probability_max']}")
    print(f"  Amanecer:         {d['sunrise'][0][11:]}")
    print(f"  Atardecer:        {d['sunset'][0][11:]}")


if __name__ == "__main__":
    main()
