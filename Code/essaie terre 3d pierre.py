import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import shapely.geometry as sgeom
from shapely.prepared import prep

def plot_3d_globe(longitude, latitude):
    # Création de la figure et des axes en 3D
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    # Réduction de la résolution pour moins de points
    u = np.linspace(-np.pi, np.pi, 180)  # 180 points pour 360 degrés de longitude (résolution réduite)
    v = np.linspace(0,np.pi, 180)       # 90 points pour 180 degrés de latitude (résolution réduite)
    u, v = np.meshgrid(u, v)
    x = np.cos(u) * np.sin(v)
    y = np.sin(u) * np.sin(v)
    z = np.cos(v)

    # Utilisation de cartopy pour obtenir les géométries des continents
    continents = cfeature.NaturalEarthFeature('physical', 'land', '110m', edgecolor='face', facecolor='none')

    # Obtention des géométries des continents
    land_geoms = list(continents.geometries())

    # Préparation des géométries pour un accès rapide
    prepared_land_geoms = [prep(geom) for geom in land_geoms]

    # Fonction pour convertir des coordonnées géographiques en coordonnées cartésiennes
    def geographic_to_cartesian(lon, lat):
        lon = np.radians(lon)
        lat = np.radians(lat)
        x = np.cos(lat) * np.cos(lon)
        y = np.cos(lat) * np.sin(lon)
        z = np.sin(lat)
        return x, y, z

    # Fonction pour vérifier si un point est sur terre (continent)
    def is_land(lon, lat):
        point = sgeom.Point(lon, lat)
        return any(geom.contains(point) for geom in prepared_land_geoms)

    # Création d'un masque pour colorier les continents et les océans
    colors = np.empty_like(x, dtype=object)
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            lon = np.degrees(u[i, j])
            lat = np.degrees(v[i, j] - np.pi / 2)
            if lat >= 85 or lat <= -85:  # Coloration des pôles
                colors[i, j] = 'white'
            elif is_land(lon, lat):
                colors[i, j] = 'orange'
            else:
                colors[i, j] = 'blue'

    # Tracé de la sphère avec les couleurs appropriées
    ax.plot_surface(x, y, z, facecolors=colors, rstride=1, cstride=1, linewidth=0, antialiased=False, shade=False)

    # Conversion des coordonnées de longitude et latitude en coordonnées cartésiennes pour le point
    x_point, y_point, z_point = geographic_to_cartesian(longitude, latitude)

    # Placement du point sur la sphère
    ax.scatter(x_point, y_point, z_point, color='red', s=100)

    # Ajustement de l'échelle et des labels
    ax.set_box_aspect([1, 1, 1])  # Egalité des axes pour un aspect sphérique
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.title(f'Point sur la planète à (Longitude: {longitude}, Latitude: {latitude})')

    # Centrer la vue sur le point spécifié
    ax.view_init(elev=latitude, azim=longitude)

    plt.show()

# Exemple d'utilisation pour une position près de l'équateur
longitude = -74.006  # Longitude de New York
latitude = 0  # Latitude près de l'équateur
plot_3d_globe(longitude, latitude)
