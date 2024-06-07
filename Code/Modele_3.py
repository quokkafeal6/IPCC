import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

# Constantes
S = 1361  # Constante solaire en W/m^2
sigma = 5.67e-8  # Constante de Stefan-Boltzmann en W/m^2/K^4
w = 2 * math.pi / 24  # En h^-1

def calculate_temperature(S, A, sigma, lat, lon, t):
    """
    Calcule la température d'équilibre radiatif de la Terre.

    :param S: Constante solaire en W/m^2
    :param A: Albédo terrestre
    :param sigma: Constante de Stefan-Boltzmann en W/m^2/K^4
    :param lat: Latitude en degrés
    :param lon: Longitude en degrés
    :param t: Temps en heures décimales
    :return: Température d'équilibre en Kelvin
    """
    # Calcul de l'énergie reçue en fonction de la latitude
    Slatlon = S * np.cos(w * t) * np.sin((90 - lat) * 2 * math.pi / 360) * np.sin(lon * 2 * math.pi / 360) - S * np.sin(w * t) * np.sin((90 - lat) * 2 * math.pi / 360) * np.cos(lon * 2 * math.pi / 360)

    # Vérifier que la latitude est dans la plage valide
    if lat < -90 or lat > 90:
        raise ValueError("La latitude doit être comprise entre -90 et 90 degrés.")
    elif lon < -180 or lon > 180:
        raise ValueError("La longitude doit être comprise entre -180 et 180 degrés.")
    elif Slatlon < 0:
        raise ValueError("Nous sommes la nuit.")

    # Énergie moyenne reçue par unité de surface
    energy_received = (1 - A) * Slatlon / 4

    # Température d'équilibre
    T = (energy_received / sigma) ** 0.25
    return T

# Dictionnaire des valeurs d'albédo pour chaque partie de la Terre
data_albedo = {
    # Continents
    "Amérique": 0.25,
    "Europe": 0.3,
    "Asie": 0.2,
    "Afrique_Continentale": 0.35,
    "Afrique_Désertique": 0.4,
    # Océans
    "Océans": 0.12,
    # Pôles
    "Pole Nord": 0.75,
    "Pole Sud": 0.8
}

# Fonction pour déterminer la partie de la Terre en fonction des coordonnées de latitude et de longitude
def determiner_partie_terre(lat, lon):
    if lat >= 60:  # Pole Nord
        return "Pole Nord"
    elif lat <= -60:  # Pole Sud
        return "Pole Sud"
    elif 45 <= lat <= 70 and -180 <= lon <= -30:  # Europe
        return "Europe"
    elif -60 <= lat <= 10 and -120 <= lon <= -30:  # Amérique
        return "Amérique"
    elif -60 <= lat <= 40 and -30 <= lon <= 160:  # Asie
        return "Asie"
    elif -60 <= lat <= 40 and -30 <= lon <= 40:  # Afrique
        if 15 <= lat <= 30 and -20 <= lon <= 40:  # Afrique_Désertique
            return "Afrique_Désertique"
        else:
            return "Afrique_Continentale"
    else:
        return "Océans"

# Fonction pour obtenir l'albédo en fonction des coordonnées de latitude et de longitude
def obtenir_albedo(lat, lon):
    partie_terre = determiner_partie_terre(lat, lon)
    return data_albedo[partie_terre]

try:
    # Entrer la latitude
    lat = float(input("Entrer la latitude (entre -90 et 90 degrés) : "))
    lon = float(input("Entrer la longitude (entre -180 et 180 degrés) : "))
    time_input = input("Entrer le temps UTC-0 à Greenwich (format HH:MM) : ")

    # Diviser l'entrée du temps en heures et minutes
    hours, minutes = map(int, time_input.split(':'))
    t = hours + minutes / 60.0  # Convertir en heures décimales

    # Obtention de l'albédo pour les coordonnées spécifiées
    A = obtenir_albedo(lat, lon)

    # Calcul de la température moyenne de la Terre
    T_earth = calculate_temperature(S, A, sigma, lat, lon, t + 6)  # t+6 pour avoir la température maximale à Greenwich à 12h
    print(f"La température moyenne de la Terre à la latitude {lat}° et la longitude {lon}° est de {T_earth:.2f} K")

    # Convertir en Celsius
    T_earth_Celsius = T_earth - 273.15
    print(f"Ce qui correspond à {T_earth_Celsius:.2f} °C")


    # Affichage du globe avec le point
    fig, ax = plt.subplots(figsize=(10, 7))

    # Création de la carte
    m = Basemap(projection='ortho', lat_0=lat, lon_0=lon, resolution='l', ax=ax)
    m.drawcoastlines()
    m.drawcountries()
    m.fillcontinents(color='coral', lake_color='aqua')
    m.drawmapboundary(fill_color='aqua')

    # Ajouter le point spécifié
    x, y = m(lon, lat)
    m.plot(x, y, 'ro', markersize=10)

    plt.title(f'Point ({lat}°, {lon}°) sur le globe')
    plt.show()

except ValueError as e:
    print(e)
10