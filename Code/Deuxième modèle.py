import math
import numpy as np

# Constantes
S = 1361  # Constante solaire en W/m^2
A = 0.3  # Albédo terrestre
sigma = 5.67e-8  # Constante de Stefan-Boltzmann en W/m^2/K^4

def calculate_temperature(S, A, sigma, lat, lon):
    """
    Calcule la température d'équilibre radiatif de la Terre.

    :param S: Constante solaire en W/m^2
    :param A: Albédo terrestre
    :param sigma: Constante de Stefan-Boltzmann en W/m^2/K^4
    :param lat: Latitude en degrés
    :return: Température d'équilibre en Kelvin
    """
    # Vérifier que la latitude est dans la plage valide
    if lat < -90 or lat > 90:
        raise ValueError("La latitude doit être comprise entre -90 et 90 degrés.")
    elif lon < -90 or lon > 90:
        raise ValueError("La longitude doit être comprise entre -90 et 90 degrés.")

    # Calcul de l'énergie reçue en fonction de la latitude
    Slatlon = S * np.cos(lat * 2 * math.pi / 360)*np.sin(lon*2*math.pi/360)

    # Énergie moyenne reçue par unité de surface
    energy_received = (1 - A) * Slatlon / 4

    # Température d'équilibre
    T = (energy_received / sigma) ** 0.25
    return T

try:
    # Entrer la latitude
    lat = float(input("Entrer la latitude (entre -90 et 90 degrés) : "))
    lon = float(input("Entrer la longitude (entre -90 et 90 degrés) : "))

    # Calcul de la température moyenne de la Terre
    T_earth = calculate_temperature(S, A, sigma, lat,lon)
    print(f"La température moyenne de la Terre à la latitude {lat}° et la longitude {lon}°est de {T_earth:.2f} K")

    # Convertir en Celsius
    T_earth_Celsius = T_earth - 273.15
    print(f"Ce qui correspond à {T_earth_Celsius:.2f} °C")
except ValueError as e:
    print(e)
