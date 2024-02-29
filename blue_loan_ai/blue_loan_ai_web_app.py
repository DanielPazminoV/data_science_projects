# Importa librerías
import pandas as pd
import sklearn.neighbors
import sklearn.preprocessing
from sklearn.neighbors import NearestNeighbors
import plotly.express as px

import streamlit as st

# Carga los datos del proyecto
base_de_prospectos_principales = pd.read_csv("base_prospectos_principales.csv")
coordenadas_prospectos_principales = pd.read_csv("Datos/coordenadas_empresas_certificadas.csv")
datos_companias = pd.read_csv("datos_companias.csv") 
datos_companias_certificadas = datos_companias[datos_companias["certificada"] == 1] 

# Convierte los tipos de datos
base_de_prospectos_principales["ruc"] = base_de_prospectos_principales['ruc'].astype(str)
coordenadas_prospectos_principales["latitude"] = coordenadas_prospectos_principales["latitude"].astype(float)
coordenadas_prospectos_principales["longitude"] = coordenadas_prospectos_principales["longitude"].astype(float)

## DESARROLLO DE LA APP

st.image('Datos/mangroove_swamp.jpg')

st.write(""" # QUIÉN RECIBIRÁ EL PRÓXIMO CRÉDITO AZUL?: INTRODUCIENDO A BLUE LOAN AI 

Descripción: Blue Loan AI es una plataforma de inteligencia artificial 
         diseñada para ayudar a las instituciones financieras a evaluar y 
         gestionar préstamos azules. En su versión de producto mínimo viable (MVP), 
         identifica empresas prospectos para la colocación de estos préstamos.

Impacto del proyecto: BlueLoan AI promueve la asignación de préstamos 
         azules a empresas del sector de acuicultura en Ecuador. 
         Al dirigir capital hacia estas iniciativas, la plataforma acelera 
         la transición hacia una economía baja en carbono.         
         """)


st.write(""" ## PROSPECTOS PRINCIPALES
Corresponden a empresas certificadas por la "Aquaculture Stewarship Council" (ASC)
          en Ecuador con un índice de liquidez corriente mayor o igual a 1.
         El siguiente mapa muestra su ubicación.
""")

st.map(coordenadas_prospectos_principales)

st.write(""" ## ANÁLISIS ECONÓMICO-FINANCIERO DE LOS PROSPECTOS
La aplicación selecciona empresas con características económico-financieras 
         similares a los prospectos principales. Adicionalmente, realiza
         un análisis económico-financiero comparando la empresa
         prospecto principal seleccionada con los 10 prospectos más semejantes.         
         """)

# Mostrar la lista desplegable en la aplicación Streamlit
selected_option = st.selectbox('Seleccione el RUC de un prospecto principal', 
                               base_de_prospectos_principales["ruc"])

# A partir del RUC seleccionado, extrae el índice respectivo
indice = int(datos_companias.loc[datos_companias['ruc'] == int(selected_option)].index[0])

# Escalado de datos

feature_names = ['cia_imvalores', 'ingresos_ventas', 'activos', 
                          'patrimonio', 'utilidad_an_imp',
                          'impuesto_renta', 'n_empleados',
                          'ingresos_totales', 'utilidad_ejercicio',
                          'total_gastos']

transformer_mas = sklearn.preprocessing.MaxAbsScaler().fit(datos_companias[feature_names].to_numpy())

datos_companias_escalado = datos_companias.copy()
datos_companias_escalado.loc[:, feature_names] = transformer_mas.transform(datos_companias[feature_names].to_numpy())

#Función que devuelve los vecinos más cercanos 

def get_knn(df, n, k, metric):
    
    """
    Devuelve los k vecinos más cercanos

    :param df: DataFrame de pandas utilizado para encontrar objetos similares dentro del mismo lugar    :param n: número de objetos para los que se buscan los vecinos más cercanos    :param k: número de vecinos más cercanos a devolver
    :param métrica: nombre de la métrica de distancia    
    :param k: el número de vecinos cercanos a calcular
    :param n: número de usuario para el que se buscan los vecinos más cercanos 
    """
    
    # Crea la instancia del algoritmo de clasificación
    # Define los parámetros del algoritmo de clasificación en donde:
        # "algorithm" es el algoritmo usado  para calcular los vecinos cercanos (fijado en "auto" para que la función escoja el, mejor algoritmo en base al ajuste de los datos usando el método "fit")
        # "metric" corresponde a la métrica de distancia
        # Ajusta el algoritmo a los datos de entrada provistos usando el método fit
    
    nbrs = NearestNeighbors(n_neighbors=k, algorithm='auto', metric=metric).fit(df) 
                                                                                      
    # Se aplica el método "kneighbors" al modelo para obtener los vecinos (en este caso clientes) más cercanos  
    # Los parámetros de método son:
        #"X", en este caso "[df.iloc[n]]" que seleciona el punto de consulta (en este caso cliente)                                                                                             
        #"return_distance=True" se establece que método devuelva las distancias que determinaron la selección de los vecinos                                                                                        
    # El método devuelve dos resultados:                                                                                          
        #"neigh_dist" en este caso "nbrs_distances", que representa una matriz con las distancias del punto de consulta (cliente) a los vecinos cercanos                                                                                 
        #"neigh_ind" en este caso "nbrs_indices", que representa los índices del "dataframe" de los vecinos cercanos al punto de consulta (cliente)                                                                                                                                                             
                                                                                        
    nbrs_distances, nbrs_indices = nbrs.kneighbors([df.iloc[n]], k, return_distance=True) 
    
    
    #Concatena los resultados de método "kneighbors" para devolver un "dataframe" de respuesta
    #Extrae todos los datos del vecino cercano seleccionado (en base al método "kneighbors") de acuerdo al valor de su índice. Estos datos se extraen del "dataframe" original "df"
    #Añade la columna de distancia al "dataframe" de respuesta, suando los siguientes parámetros: 
        #índice del vecino cercano (cliente) "index=nbrs_indices[0]"
        #matriz transpuesta de los resultados de las distancias de los vecinos cercanos
        #nombre de la nueva colunma "columns=['distance']"
        
    df_res = pd.concat([ 
        df.iloc[nbrs_indices[0]],   
        pd.DataFrame(nbrs_distances.T, index=nbrs_indices[0], columns=['distance']) 
        ], axis=1)                                                                      
                                                                                                                                                                                
    return df_res

# Función que devuelve el DataFrame de Resultados

def dataframe_de_resultados(df, n, function, k, metric):
    resultado_escalado = function(df, n, k, metric)
        
    indices = []
    for index in resultado_escalado.index:
        indices.append(index)

    resultado_no_escalado = datos_companias[datos_companias.index.isin(indices)]
    resultado_no_escalado['ruc'] = resultado_no_escalado['ruc'].map(str)

    return resultado_no_escalado 

resultado_final = dataframe_de_resultados(datos_companias_escalado, indice, get_knn, 10, "euclidean")

resultado_final = resultado_final.rename({'cia_imvalores': 'Empresas en Mercado de Valores', 
                                          'ingresos_ventas': 'Ingresos por Ventas',
                                          'activos': 'Activos',
                                          'n_empleados': 'Número de Empleados',
                                          'ingresos_totales': 'Ingresos Totales',
                                          'utilidad_ejercicio': 'Utilidad del Ejercicio',
                                          'total_gastos': 'Total de Gastos',
                                          'patrimonio': 'Patrimonio',
                                          'utilidad_an_imp': 'Utilidad Antes de Impuestos',
                                          'ruc': 'RUC',
                                          'certificada': 'Certificada',
                                          },
                                          axis=1)

st.write(""" #### Prospectos similares a los principales        
         """)
st.dataframe(resultado_final) 

# Visualizaciones de Análisis Económico-Financieros

# Genera gráficos de barras
fig = px.bar(resultado_final, x='RUC', y='Ingresos por Ventas',
             title="Comparación de ingresos por ventas",
             width=600, height=400,
             template="simple_white",
             color="Certificada")



st.plotly_chart(fig)
