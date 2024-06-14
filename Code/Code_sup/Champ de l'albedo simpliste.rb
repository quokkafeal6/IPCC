# Dictionnaire des valeurs d'albédo pour chaque partie de la Terre
data_albedo = {
    # Continents
    "Amérique du Nord": 0.25,
    "Amérique du Sud": 0.18,
    "Europe de l'Ouest": 0.25,
    "Europe de l'Est": 0.3,
    "Asie du Sud": 0.15,
    "Asie de l'Est": 0.2,
    "Asie du Sud-Est": 0.2,
    "Afrique du Nord": 0.25,
    "Afrique Sub-saharienne": 0.18,
    "Afrique_Désertique": 0.45,
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
    elif 30 <= latitude <= 60 and -130 <= longitude <= -60:  # Amérique du Nord
        return "Amérique du Nord"
    elif -60 <= latitude <= 15 and -90 <= longitude <= -30:  # Amérique du Sud
        return "Amérique du Sud"
    elif 45 <= latitude <= 70 and -10 <= longitude <= 40:  # Europe
        if -10 <= longitude <= 20:  # Europe de l'Ouest
            return "Europe de l'Ouest"
        else:  # Europe de l'Est
            return "Europe de l'Est"
    elif -10 <= latitude <= 40 and 60 <= longitude <= 160:  # Asie
        if 5 <= latitude <= 30 and 60 <= longitude <= 120:  # Asie du Sud
            return "Asie du Sud"
        elif 30 <= latitude <= 50 and 100 <= longitude <= 140:  # Asie de l'Est
            return "Asie de l'Est"
        else:  # Asie du Sud-Est
            return "Asie du Sud-Est"
    elif 15 <= latitude <= 30 and -20 <= longitude <= 40:  # Afrique_Désertique
        return "Afrique_Désertique"
    elif -35 <= latitude <= 15 and -20 <= longitude <= 50:  # Afrique
        if latitude > 0:  # Afrique du Nord
            return "Afrique du Nord"
        else:  # Afrique Sub-saharienne
            return "Afrique Sub-saharienne"
    else:
        return "Océans"

# Fonction pour obtenir l'albédo en fonction des coordonnées de latitude et de longitude
def obtenir_albedo(latitude, longitude):
    partie_terre = determiner_partie_terre(latitude, longitude)
    return data_albedo.get(partie_terre, "Inconnu")

# Fonction pour obtenir la conductivité thermique en fonction des coordonnées de latitude et de longitude
def obtenir_conductivite(latitude, longitude):
    partie_terre = determiner_partie_terre(latitude, longitude)
    return data_conductivite.get(partie_terre, "Inconnu")

# Coordonnées de latitude et de longitude en entrée
latitude_entree = float(input("Entrez la latitude : "))
longitude_entree = float(input("Entrez la longitude : "))

# Obtention de l'albédo et de la conductivité thermique pour les coordonnées spécifiées
albedo = obtenir_albedo(latitude_entree, longitude_entree)
conductivite = obtenir_conductivite(latitude_entree, longitude_entree)

print(f"L'albédo est de : {albedo}")

