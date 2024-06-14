import requests
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from PIL import Image
from io import BytesIO

def get_earth_texture():
    # Utilisation d'une image fixe de la Terre entière (Blue Marble)
    url = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Earth_Eastern_Hemisphere.jpg/2048px-Earth_Eastern_Hemisphere.jpg"
    response = requests.get(url)
    response.raise_for_status()
    img = Image.open(BytesIO(response.content))
    return img

def plot_3d_globe_with_texture(longitude, latitude):
    # Récupération de l'image texture de la Terre
    img = get_earth_texture()

    # Création de la figure et des axes en 3D
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    # Paramètres pour la sphère
    u = np.linspace(0, 2 * np.pi, img.size[0])
    v = np.linspace(0, np.pi, img.size[1])
    u, v = np.meshgrid(u, v)
    x = np.cos(u) * np.sin(v)
    y = np.sin(u) * np.sin(v)
    z = np.cos(v)

    # Appliquer la texture à la sphère
    img = np.array(img) / 255.0  # Normaliser les valeurs de l'image
    img = np.flipud(img)  # Inverser l'image verticalement pour correspondre aux coordonnées sphériques

    ax.plot_surface(x, y, z, rstride=1, cstride=1, facecolors=img, linewidth=0, antialiased=False)

    # Conversion des coordonnées de longitude et latitude en coordonnées cartésiennes pour le point
    def geographic_to_cartesian(lon, lat):
        lon = np.radians(lon)
        lat = np.radians(lat)
        x = np.cos(lat) * np.cos(lon)
        y = np.cos(lat) * np.sin(lon)
        z = np.sin(lat)
        return x, y, z

    # Placement du point sur la sphère
    x_point, y_point, z_point = geographic_to_cartesian(longitude, latitude)
    ax.scatter(x_point, y_point, z_point, color='red', s=100)

    # Ajustement de l'échelle et des labels
    ax.set_box_aspect([1, 1, 1])  # Egalité des axes pour un aspect sphérique
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.title(f'Point sur la planète à (Longitude: {longitude}, Latitude: {latitude})')

    # Centrer la vue sur le point spécifié
    ax.view_init(elev=latitude, azim=longitude + 180)

    plt.show()

# Exemple d'utilisation pour une position près de l'équateur
longitude = -74.006  # Longitude de New York
latitude = 40.7128  # Latitude de New York
plot_3d_globe_with_texture(longitude, latitude)
