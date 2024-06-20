import numpy as np
import matplotlib.pyplot as plt

# Constantes
sigma = 5.67e-8  # Constante de Stefan-Boltzmann, W/m²·K⁴
epsilon = 0.95  # Émissivité de la surface
h = 2  # Coefficient de transfert de chaleur par convection, W/m²·K
k = 1.5  # Conductivité thermique du sol, W/m·K
c = 800  # Capacité thermique spécifique du sol, J/kg·K
rho = 1600  # Densité du sol, kg/m³
d = 0.1  # Épaisseur de la couche de sol, m
A = 1  # Surface considérée, m²

# Températures initiales
T_s = 293  # Température initiale de la surface, K (20°C)
T_a = 283  # Température de l'air, K (10°C)
T_sub = 283  # Température de la sous-couche du sol, K (10°C)

# Temps de simulation
dt = 60  # Intervalle de temps, s
total_time = 3600 * 8  # 8 heures de nuit, s
time_steps = int(total_time / dt)

# Masse de la couche de sol considérée
m = rho * A * d

# Listes pour stocker les températures
surface_temperatures = [T_s]
air_temperatures = [T_a]

# Évolution des températures
for _ in range(time_steps):
    # Calculer les flux de chaleur
    Q_rad = epsilon * sigma * A * T_s**4
    Q_conv = h * A * (T_s - T_a)
    Q_cond = k * A * (T_s - T_sub) / d

    # Changement de température de la surface
    dT_s = (- Q_rad - Q_conv + Q_cond) * dt / (m * c)

    # Mise à jour de la température de la surface en s'assurant qu'elle reste réaliste
    T_s = max(0, T_s + dT_s)

    # Mise à jour de la température de l'air
    dT_a = Q_conv * dt / (c * rho * d)  # Simplification : baisse due au transfert convectif
    T_a = max(0, T_a - dT_a)

    # Stocker les températures
    surface_temperatures.append(T_s)
    air_temperatures.append(T_a)

# Affichage des résultats
print(f"Température finale de la surface après 8 heures: {T_s:.2f} K")
print(f"Température finale de l'air après 8 heures: {T_a:.2f} K")

# Visualisation
times = np.arange(0, total_time + dt, dt) / 3600  # Convertir en heures
plt.plot(times, surface_temperatures, label='Température de la surface')
plt.plot(times, air_temperatures, label='Température de l\'air', linestyle='--')
plt.xlabel('Temps (heures)')
plt.ylabel('Température (K)')
plt.title('Évolution de la température de la surface et de l\'air pendant la nuit')
plt.legend()
plt.grid(True)
plt.show()
