import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import shapely.geometry as sgeom
from shapely.prepared import prep
from datetime import datetime, timedelta

def plot_3d_globe(longitude, latitude, point_longitude, point_latitude):
    # Création de la figure et des axes en 3D
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    # Réduction de la résolution pour moins de points
    u = np.linspace(-np.pi, np.pi, 180)  # 180 points pour 360 degrés de longitude (résolution réduite)
    v = np.linspace(0, np.pi, 180)       # 90 points pour 180 degrés de latitude (résolution réduite)
    u, v = np.meshgrid(u, v)
    x = np.cos(u) * np.sin(v)
    y = np.sin(u) * np.sin(v)
    z = -np.cos(v)  # Inversion des coordonnées z pour inverser le haut et le bas

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

    # Fonction pour calculer la position du soleil en fonction de l'heure
    def solar_position(date_time):
        # Calcul de l'heure en heures décimales
        hour = date_time.hour + date_time.minute / 60 + date_time.second / 3600
        # Jour julien
        julian_day = date_time.toordinal() + 1721424.5
        # Longitude moyenne du soleil
        mean_longitude = (280.46 + 0.9856474 * julian_day) % 360
        # Anomalie moyenne du soleil
        mean_anomaly = 357.528 + 0.9856003 * julian_day
        # Ecliptique
        ecliptic = (mean_longitude + 1.915 * np.sin(np.radians(mean_anomaly)) + 0.02 * np.sin(2 * np.radians(mean_anomaly))) % 360
        # Obliquité de l'écliptique
        obliquity = 23.439 - 0.0000004 * julian_day
        # Déclinaison du soleil
        declination = np.degrees(np.arcsin(np.sin(np.radians(obliquity)) * np.sin(np.radians(ecliptic))))
        # Angle horaire
        hour_angle = (15 * (hour - 12)) % 360
        # Hauteur du soleil
        solar_height = np.degrees(np.arcsin(np.sin(np.radians(latitude)) * np.sin(np.radians(declination)) + np.cos(np.radians(latitude)) * np.cos(np.radians(declination)) * np.cos(np.radians(hour_angle))))
        # Azimut du soleil
        solar_azimuth = np.degrees(np.arccos((np.sin(np.radians(declination)) - np.sin(np.radians(latitude)) * np.sin(np.radians(solar_height))) / (np.cos(np.radians(latitude)) * np.cos(np.radians(solar_height)))))
        # Conversion en coordonnées cartésiennes
        x_solar = np.cos(np.radians(solar_height)) * np.sin(np.radians(solar_azimuth))
        y_solar = np.cos(np.radians(solar_height)) * np.cos(np.radians(solar_azimuth))
        z_solar = np.sin(np.radians(solar_height))
        return x_solar, y_solar, z_solar

    # Création d'un masque pour colorier les continents et les océans
    colors = np.empty_like(x, dtype=object)
    current_time = datetime.utcnow()  # Utilisation de l'heure actuelle en UTC

    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            lon = np.degrees(u[i, j])
            lat = np.degrees(v[i, j] - np.pi / 2)
            if lat >= 85 or lat <= -85:  # Coloration des pôles
                colors[i, j] = 'white'
            else:
                x_solar, y_solar, z_solar = solar_position(current_time)
                x_point, y_point, z_point = geographic_to_cartesian(lon, lat)
                # Calcul du produit scalaire pour déterminer si le point est dans l'ombre
                dot_product = x_point * x_solar + y_point * y_solar + z_point * z_solar
                if dot_product < 0:  # Si le point est dans l'ombre
                    if is_land(lon, lat):
                        colors[i, j] = 'darkgreen'  # Couleur sombre pour la terre la nuit
                    else:
                        colors[i, j] = 'darkblue'   # Couleur sombre pour l'eau la nuit
                else:
                    if is_land(lon, lat):
                        colors[i, j] = 'orange'     # Couleur pour la terre le jour
                    else:
                        colors[i, j] = 'blue'       # Couleur pour l'eau le jour

    # Tracé de la sphère avec les couleurs appropriées
    ax.plot_surface(x, y, z, facecolors=colors, rstride=1, cstride=1, linewidth=0, antialiased=False, shade=False)

    # Conversion des coordonnées de longitude et latitude du point à afficher en coordonnées cartésiennes
    x_point, y_point, z_point = geographic_to_cartesian(point_longitude, point_latitude)

    # Placement du point rouge
    ax.scatter(x_point, y_point, z_point, color='red', s=100, label='Point spécifié')

    # Ajustement de l'échelle et des labels
    ax.set_box_aspect([1, 1, 1])  # Egalité des axes pour un aspect sphérique
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.title(f'Globe terrestre avec l\'ombre en fonction de l\'heure UTC ({current_time.strftime("%Y-%m-%d %H:%M:%S")} UTC)')

    # Centrer la caméra sur le point spécifié
    ax.view_init(elev=np.degrees(np.arcsin(z_point)), azim=np.degrees(np.arctan2(y_point, x_point)))

    plt.legend()
    plt.show()

# Exemple d'utilisation avec le point spécifié à New York
plot_3d_globe(-74.006, 40.7128, -74.006, 40.7128)
