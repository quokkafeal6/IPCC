import numpy as np
import plotly.graph_objects as go

# Coordonnées des contours des continents à l'échelle
continents = {
    "Africa": [
        [-17.8, 14.8], [-3.5, 18], [11.5, 22], [13.5, 25],
        [15, 24], [22, 18], [29.6, 14], [29.6, 14.8], [36.8, 10.25],
        [31.5, 5], [34, -0.5], [30.2, -3.8], [24.6, -4.6], [23.6, -12.6],
        [14.5, -12.4], [5.8, -5.5], [-17.8, 0], [-17.8, 14.8]
    ],
    "North America": [
        [8, -145], [11.5, -147], [20, -148], [25, -150], [30, -150],
        [35, -151], [40, -151], [45, -145], [60, -150], [70, -140],
        [50, -30], [20, -30], [8, -145]
    ],
    "South America": [
        [-53, -58], [-30, -58], [-12, -68], [-9.5, -60],
        [1, -57], [1, -50], [-12, -50], [-20, -58], [-27, -57],
        [-53, -58]
    ],
    "Europe": [
        [64, -27], [75, -15], [70, 55], [35, 30], [41, 18],
        [43, -4], [45, -4], [50, -12], [59, -4], [67, 0],
        [74, 21], [64, -27]
    ],
    "Asia": [
        [75, -15], [75, 165], [25, 165], [25, 85], [35, 45],
        [37, 55], [35, 30], [70, 55], [75, -15]
    ],
    "Australia": [
        [-10, 105], [-10, 155], [-45, 155], [-45, 105],
        [-10, 105]
    ],
    "Arctic": [
        [75, -175], [75, 175], [90, 175], [90, -175],
        [75, -175]
    ],
    "Antarctica": [
        [-60, -180], [-60, 180], [-90, 180], [-90, -180],
        [-60, -180]
    ]
}

# Rayon de la Terre en kilomètres
radius_earth = 6371

# Rayon de la sphère
radius_sphere = 6372

# Facteur d'agrandissement des continents
scale_factor_continents = 1.25

# Création de la figure
fig = go.Figure()

# Ajout de la sphère représentant la Terre
phi, theta = np.mgrid[0.0:np.pi:100j, 0.0:2.0*np.pi:100j]
x = radius_sphere * np.sin(phi) * np.cos(theta)
y = radius_sphere * np.sin(phi) * np.sin(theta)
z = radius_sphere * np.cos(phi)
fig.add_trace(go.Surface(x=x, y=y, a=z, colorscale='Blues', showscale=False))

# Ajout des continents comme des bandes de terre à l'échelle
for continent, points in continents.items():
    lon, lat = zip(*points)
    lon = np.array(lon)
    lat = np.array(lat)
    theta = np.radians(lon)
    phi = np.radians(90 - lat)
    x_continent = radius_sphere * np.sin(phi) * np.cos(theta) * scale_factor_continents
    y_continent = radius_sphere * np.sin(phi) * np.sin(theta) * scale_factor_continents
    z_continent = radius_sphere * np.cos(phi) * scale_factor_continents
    fig.add_trace(go.Carpet(x=x_continent, y=y_continent, z=z_continent, color='brown'))

# Paramètres de la mise en page
fig.update_layout(scene=dict(aspectratio=dict(x=1, y=1, z=1), 
                             aspectmode='manual',
                             xaxis=dict(visible=False),
                             yaxis=dict(visible=False),
                             zaxis=dict(visible=False)),
                  margin=dict(r=0, l=0, b=0, t=0))

# Affichage du tracé
fig.show()
