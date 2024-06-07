import numpy as np

# Constantes
sigma = 5.67e-8  # Constante de Stefan-Boltzmann, W/m²·K⁴
epsilon = 0.95  # Émissivité de la surface
h = 10  # Coefficient de transfert de chaleur par convection, W/m²·K
k = 1.5  # Conductivité thermique du sol, W/m·K
c = 800  # Capacité thermique spécifique du sol, J/kg·K
rho = 1600  # Densité du sol, kg/m³
d = 0.1  # Épaisseur de la couche de sol (valeur prise par la NASA pour  Sellers et al. (1996)), m
A = 1  # Surface considérée, m²

# Températures initiales
T_s = 293  # Température initiale de la surface, K
T_a = 283  # Température de l'air, K

# Temps de simulation
dt = 60  # Intervalle de temps, s
total_time = 3600 * 12  # 12 heures de nuit, s
time_steps = total_time // dt

# Masse de la surface considérée
m = rho * A * d

# Évolution de la température
temperatures = [T_s]
for _ in range(int(time_steps)):
    Q_rad = epsilon * sigma * A * T_s**4
    Q_conv = h * A * (T_s - T_a)
    Q_cond = k * A * (T_s - T_a) / d
    dT_s = (- Q_rad - Q_conv - Q_cond) * dt / (m * c)
    T_s += dT_s
    temperatures.append(T_s)

print(f"Température finale de la surface après 12 heures: {T_s:.2f} K")

# Visualisation (facultatif)
import matplotlib.pyplot as plt

times = np.arange(0, total_time + dt, dt) / 3600  # Convertir en heures
plt.plot(times, temperatures)
plt.xlabel('Temps (heures)')
plt.ylabel('Température de la surface (K)')
plt.title('Évolution de la température de la surface pendant la nuit')
plt.grid(True)
plt.show()
