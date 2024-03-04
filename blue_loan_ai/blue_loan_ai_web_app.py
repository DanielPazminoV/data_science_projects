# Importa librerías
import pandas as pd
import sklearn.neighbors
import sklearn.preprocessing
from sklearn.neighbors import NearestNeighbors
import plotly.express as px
import folium
from streamlit_folium import st_folium

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
with st.sidebar.expander("Introducción"):
    st.write(""" ## BLUE LOAN AI """)
    st.image('Datos/mangroove_swamp.jpg')
    st.write(""" Blue Loan AI es una plataforma de inteligencia artificial 
             que ayuda a las instituciones financieras a evaluar y gestionar 
             préstamos azules. Su producto mínimo viable (MVP) identifica 
             empresas prospectas para la colocación de estos préstamos, 
             priorizando aquellas del sector de acuicultura en Ecuador. 
             Al dirigir capital hacia estas iniciativas, la plataforma contribuye 
             a acelerar la transición hacia una economía baja en carbono.""")
    
with st.sidebar.expander("Prospectos Principales"):
    st.write(""" Corresponden a empresas certificadas por la Aquaculture Stewarship Council (ASC) 
             en Ecuador con un índice de liquidez corriente mayor o igual a 1. 
             El mapa muestra su ubicación.""")
    
with st.sidebar.expander("Análisis Económico-Financiero de los Prospectos"):
    st.write(""" La aplicación selecciona empresas con características económico-financieras 
             similares a los prospectos principales. Adicionalmente, realiza un análisis 
             económico-financiero comparando la empresa prospecto principal seleccionada con 
             los 9 prospectos más semejantes.""")

with st.sidebar.expander("Fuentes de datos"):
    st.write("""
                
1) https://www.supercias.gob.ec/portalscvs/index.htm
         
2) https://asc-aqua.org/
""")

st.image('Datos/banner.png')

st.write(""" # ¿QUIÉN RECIBIRÁ EL PRÓXIMO CRÉDITO AZUL? """)
#st.markdown()


# Mostrar la lista desplegable en la aplicación Streamlit

st.write(""" ### ANÁLISIS ECONÓMICO-FINANCIERO DE LOS PROSPECTOS """) 

selected_option = st.selectbox('En la siguiente lista desplegable seleccione el RUC de un prospecto principal para iniciar.', 
                               base_de_prospectos_principales["ruc"])

# A partir del RUC seleccionado, extrae el índice respectivo
indice = int(datos_companias.loc[datos_companias['ruc'] == int(selected_option)].index[0])

# Escalado de datos

feature_names = ['ingresos_ventas', 'activos', 
                          'utilidad_neta', 'liquidez_corriente']

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


resultado_final = resultado_final.rename({
                                            'ingresos_ventas': 'Ingresos por Ventas (USD)',
                                            'activos': 'Activos (USD)',                                           
                                            'utilidad_neta': 'Utilidad Neta (USD)',
                                            'liquidez_corriente': 'Índice de Liquidez Corriente',                                        
                                            'ruc': 'RUC',
                                            'certificada': 'Certificada',
                                            },
                                            axis=1)


# Reemplaza los valores númericos por categóricos
resultado_final['Certificada'] = resultado_final['Certificada'].replace(1,'Si')
resultado_final['Certificada'] = resultado_final['Certificada'].replace(0,'No')


## Visualizaciones de Análisis Económico-Financieros

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Ingresos por Ventas",
                                                    "Activos",
                                                    "Utilidad Neta",
                                                    "Liquidez Corriente",
                                                    "Datos Prospectos Similares"
                                                    ])

with tab1:

    # 1) Genera gráficos de barras para análisis de ingresos por ventas

    colors = {'Si': 'blue', 'No': 'gray'}

    fig = px.bar(resultado_final, x='RUC', y='Ingresos por Ventas (USD)',
                title="Comparación de ingresos por ventas entre prospectos",
                width=600, height=400,
                template="simple_white",
                color="Certificada",
                color_discrete_map=colors)

    fig.update_layout(xaxis_title='<b>RUC</b>', yaxis_title='<b>Ingresos por Ventas (USD)</b>')

    st.plotly_chart(fig)

with tab2:

    # 2) Genera gráficos de barras para análisis de activos

    colors = {'Si': 'blue', 'No': 'gray'}

    fig = px.bar(resultado_final, x='RUC', y='Activos (USD)',
                title="Comparación de activos entre prospectos",
                width=600, height=400,
                template="simple_white",
                color="Certificada",
                color_discrete_map=colors)

    fig.update_layout(xaxis_title='<b>RUC</b>', yaxis_title='<b> Activos (USD) </b>')

    st.plotly_chart(fig)

with tab3:

    # 3) Genera gráficos de barras para análisis de utilidad neta

    colors = {'Si': 'blue', 'No': 'gray'}

    fig = px.bar(resultado_final, x='RUC', y='Utilidad Neta (USD)',
                title="Comparación de utilidad neta",
                width=600, height=400,
                template="simple_white",
                color="Certificada",
                color_discrete_map=colors)

    fig.update_layout(xaxis_title='<b>RUC</b>', yaxis_title='<b> Utilidad Neta (USD)</b>')

    st.plotly_chart(fig)

with tab4:

    # 4) Genera gráficos de barras para análisis de liquidez corriente

    colors = {'Si': 'blue', 'No': 'gray'}

    fig = px.bar(resultado_final, x='RUC', y='Índice de Liquidez Corriente',
                title="Comparación de liquidez corriente",
                width=600, height=400,
                template="simple_white",
                color="Certificada",
                color_discrete_map=colors)

    fig.update_layout(xaxis_title='<b>RUC</b>', yaxis_title='<b> Índice de Liquidez Corriente</b>')

    st.plotly_chart(fig)

with tab5:

    st.write(""" #### Prospectos similares a los principales        
         """)
    
    # Función para resaltar la fila que tiene el número de RUC seleccionado
    def color_coding(row):
     return ['background-color:yellow'] * len(row) if row.RUC == selected_option else ['background-color:white'] * len(row)

    # Aplicar el estilo personalizado al dataframe
    st.dataframe(resultado_final.style.apply(color_coding, axis=1))
    
st.write(""" ### UBICACIÓN PROSPECTOS PRINCIPALES """)  


#st.map(coordenadas_prospectos_principales)       

# Calcual el centro
centro_latitud = coordenadas_prospectos_principales['latitude'].mean() 
centro_longitud = coordenadas_prospectos_principales['longitude'].mean() 

# Crea el objeto
# attr = (
#     '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> '
#     'contributors, &copy; <a href="https://cartodb.com/attributions">CartoDB</a>'
# )
# tiles = "https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}.png"
#m = folium.Map(location=[centro_latitud, centro_longitud], tiles=tiles, attr=attr, zoom_start=10)
m = folium.Map(location=[centro_latitud, centro_longitud], zoom_start=9)

# Añadir marcadores al mapa
for idx, row in coordenadas_prospectos_principales.iterrows():
    folium.CircleMarker([row['latitude'], row['longitude']], 
                        popup=row['RUC'], radius=3,
                        weight=0,
                        fill_color='red',
                        fill_opacity=1).add_to(m)

# call to render Folium map in Streamlit
st_data = st_folium(m, width=725)



st.markdown('<sub>Creado por Daniel Pazmiño Vernaza | Contacto: daniel.pazmino-v@gmail.com</sub>', unsafe_allow_html=True)