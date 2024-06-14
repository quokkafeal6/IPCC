import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np

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

# Création de la carte
fig, ax = plt.subplots(figsize=(12, 8))
m = Basemap(projection='cyl', resolution='c', ax=ax)

# Dessiner les côtes et les pays
m.drawcoastlines()
m.drawcountries()

# Définir les couleurs pour chaque zone
zone_colors = {
    "Pole Nord": "blue",
    "Pole Sud": "cyan",
    "Amérique du Nord": "green",
    "Amérique du Sud": "lime",
    "Europe de l'Ouest": "yellow",
    "Europe de l'Est": "orange",
    "Asie du Sud": "red",
    "Asie de l'Est": "purple",
    "Asie du Sud-Est": "magenta",
    "Afrique_Désertique": "brown",
    "Afrique du Nord": "pink",
    "Afrique Sub-saharienne": "olive",
    "Océans": "lightblue"
}

# Créer un maillage de points pour couvrir la carte
lats = np.linspace(-90, 90, 360)
lons = np.linspace(-180, 180, 720)
lat_grid, lon_grid = np.meshgrid(lats, lons)

# Déterminer les couleurs pour chaque point du maillage
colors = np.empty(lat_grid.shape, dtype=int)
color_mapping = {zone: i for i, zone in enumerate(zone_colors.keys())}
for i in range(lat_grid.shape[0]):
    for j in range(lat_grid.shape[1]):
        zone = determiner_partie_terre(lat_grid[i, j], lon_grid[i, j])
        colors[i, j] = color_mapping[zone]

# Afficher les couleurs sur la carte
cmap = plt.cm.get_cmap('tab20', len(zone_colors))  # Utiliser une colormap avec le nombre de zones
m.imshow(colors.T, origin='lower', extent=[-180, 180, -90, 90], cmap=cmap)

# Ajouter une légende
import matplotlib.patches as mpatches
handles = [mpatches.Patch(color=cmap(i), label=zone) for i, zone in enumerate(zone_colors.keys())]
plt.legend(handles=handles, bbox_to_anchor=(0.95, 1), loc='upper left')

plt.title('Zones géographiques selon la latitude et la longitude')
plt.show()

