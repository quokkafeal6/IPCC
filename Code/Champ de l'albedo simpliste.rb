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
def determiner_partie_terre(latitude, longitude):
    if latitude >= 60:  # Pole Nord
        return "Pole Nord"
    elif latitude <= -60:  # Pole Sud
        return "Pole Sud"
    elif 45 <= latitude <= 70 and -180 <= longitude <= -30:  # Europe
        return "Europe"
    elif -60 <= latitude <= 10 and -120 <= longitude <= -30:  # Amérique
        return "Amérique"
    elif -60 <= latitude <= 40 and -30 <= longitude <= 160:  # Asie
        return "Asie"
    elif -60 <= latitude <= 40 and -30 <= longitude <= 40:  # Afrique
        if 15 <= latitude <= 30 and -20 <= longitude <= 40:  # Afrique_Désertique
            return "Afrique_Désertique"
        else:
            return "Afrique_Continentale"
    else:
        return "Océans"

# Fonction pour obtenir l'albédo en fonction des coordonnées de latitude et de longitude
def obtenir_albedo(latitude, longitude):
    partie_terre = determiner_partie_terre(latitude, longitude)
    return data_albedo[partie_terre]

# Coordonnées de latitude et de longitude en entrée
latitude_entree = float(input("Entrez la latitude : "))
longitude_entree = float(input("Entrez la longitude : "))

# Obtention de l'albédo pour les coordonnées spécifiées
albedo = obtenir_albedo(latitude_entree, longitude_entree)

print("L'albédo est de :", albedo)
