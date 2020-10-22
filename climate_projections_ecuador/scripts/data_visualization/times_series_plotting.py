""" Grafica serie de tiempo"""

# Importa librerías

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Lee datos y los ordena para usar Seaborn

Promedios_TMed = pd.read_csv('promedios_anuales_obs_y_proy.csv')
Promedios_TMed_pivot = Promedios_TMed.pivot("Años", "Fuente", "Temperatura Media")

# Grafica la figura

plt.figure(figsize=(16, 6))
ax = sns.lineplot(data=Promedios_TMed_pivot)
plt.title('Temperatura Media en Ecuador', fontsize='30')
plt.setp(ax.get_legend().get_texts(), fontsize='20') 
ax.set_xlabel("Años", fontsize='25')
ax.set_ylabel("Temperatura ($^oC$)", fontsize='25')
plt.savefig('TMed_obs_y_proy.png')
plt.show()
