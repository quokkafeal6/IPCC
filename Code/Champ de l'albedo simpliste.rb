# Dictionnaire des valeurs d'albédo pour chaque partie de la Terre
data_albedo = {
    # Continents
    "Amérique": 0.25,
    "Europe": 0.3,
    "Asie": 0.2,
    "Afrique_Continentale": 0.25,
    "Afrique_Désertique": 0.45,
    # Océans
    "Océans": 0.12,
    # Pôles
    "Pole Nord": 0.75,
    "Pole Sud": 0.8
}

data_conductivitetherm = {
    # Continents
    "Amérique": 1.5,             # W/m·K, moyenne approximative pour divers sols et terrains
    "Europe": 1.8,               # W/m·K, moyenne approximative pour divers sols et terrains
    "Asie": 1.3,                 # W/m·K, moyenne approximative pour divers sols et terrains
    "Afrique_Continentale": 1.6, # W/m·K, moyenne approximative pour divers sols et terrains
    "Afrique_Désertique": 0.5,   # W/m·K, sable désertique a une conductivité thermique plus basse
    # Océans
    "Océans": 0.6,               # W/m·K, moyenne pour l'eau de mer
    # Pôles
    "Pole Nord": 2.2,            # W/m·K, pour la glace et le permafrost
    "Pole Sud": 2.1              # W/m·K, pour la glace et le permafrost
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
