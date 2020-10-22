""" Calcula los promedio anuales y
grafica el resultado como serie de tiempo (Ej:temperatura media)"""

import glob
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Crea una base de datos con todas estaciones disponibles (ej: temperatura media )
Obs_TMed = pd.concat([pd.read_csv(f, sep='\t') for f in glob.glob('*.txt')], ignore_index=True)

# Crea un "dataframe" vacio para guardar los datos de promedios anuales
TMed_promedios_anuales = pd.DataFrame(columns=['Años', 'Promedios'])

# Llena la columna de "Años" correspondinete a los años con datos disponibles
Anyos = pd.Series(range(1981, 2011))
for a in Anyos:
    TMed_promedios_anuales = TMed_promedios_anuales.append({'Años': a}, ignore_index=True)

# Genera un "dataframe" de indices (ubicaciòn en serie) de cada año del periodo de estudio
unique_index = pd.Index(range(1981, 2011))

# Calcula los promedios anuales de la base de datos y
# los almancena en la columna de resultados correspondiente
for a in Anyos:
    Obs_TMed_anyo_a = Obs_TMed.loc[Obs_TMed['Anyo'] == a]
    P_anyo_a = Obs_TMed_anyo_a['Valor'].mean()
    i = unique_index.get_loc(a)
    TMed_promedios_anuales.iloc[i, 1] = P_anyo_a

# Escribe los resultados en un archile .cvs
TMed_promedios_anuales.to_csv(r'/home/daniel/Python/Analisis_proyecciones_climaticas_EC/Tempertura_media/Observaciones/promedios_anuales_observaciones.csv', index=False, header=True)
                              
# Grafica los resultados como una serie de tiempo
sns.lineplot(x='Años', y='Promedios', data=TMed_promedios_anuales,
             legend='full', label=str('Observaciones'))
plt.title('Temperatura Media en Ecuador')
sns.set_context('talk')
plt.savefig('TMed_obs.png')
plt.show()
