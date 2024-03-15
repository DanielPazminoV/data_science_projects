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
base_de_prospectos_principales = pd.read_csv("Datos/base_prospectos_principales.csv")
coordenadas_prospectos_principales = pd.read_csv("Datos/coordenadas_empresas_certificadas.csv")
datos_companias = pd.read_csv("Datos/datos_companias.csv") 
datos_companias_certificadas = datos_companias[datos_companias["certificada"] == 1]
compania = pd.read_csv("Datos/bi_compania.csv") 

# Convierte los tipos de datos
base_de_prospectos_principales["ruc"] = base_de_prospectos_principales['ruc'].astype(str)
coordenadas_prospectos_principales["latitude"] = coordenadas_prospectos_principales["latitude"].astype(float)
coordenadas_prospectos_principales["longitude"] = coordenadas_prospectos_principales["longitude"].astype(float)

## DESARROLLO DE LA APP
with st.sidebar.expander("Introducción"):
    st.write(""" ## BLUE LOAN AI """)
    st.image('Datos/mangroove_swamp_1.jpg')

    styled_text_introduccion = """
    <div style="font-family: 'Courier New', monospace;">
    Blue Loan AI es una plataforma de inteligencia artificial 
    que ayuda a las instituciones financieras a identificar 
    prospectos de empresas para la colocación de estos préstamos azules
    </div>
    """

    # Mostrar el texto formateado
    st.write(styled_text_introduccion, unsafe_allow_html=True)
    
with st.sidebar.expander("Prospectos Principales"):
    st.image('Datos/mangroove_swamp_2.jpg')
    styled_text_prospectos_principales = """
    <div style="font-family: 'Courier New', monospace;">
    Corresponden a empresas certificadas por la Aquaculture Stewarship Council (ASC) 
    en Ecuador que se encuentran económicamente activas. El mapa muestra su ubicación
    </div>
    """

    # Mostrar el texto formateado
    st.write(styled_text_prospectos_principales, unsafe_allow_html=True)

    
with st.sidebar.expander("Análisis Económico-Financiero de los Prospectos"):
    st.image('Datos/mangroove_swamp_3.jpg')

    styled_text_analisis_economico = """
    <div style="font-family: 'Courier New', monospace;">
    La aplicación selecciona empresas con características económico-financieras 
    similares a los prospectos principales usando datos del 2023
    </div>
    """

    # Mostrar el texto formateado
    st.write(styled_text_analisis_economico, unsafe_allow_html=True)


with st.sidebar.expander("Fuentes de datos"):
    st.image('Datos/mangroove_swamp_4.jpg')
    styled_text_datos = """
    <div style="font-family: 'Courier New', monospace;">

    1) https://shorturl.at/gpEJV
         
    2) https://asc-aqua.org/
    </div>
    """

    # Mostrar el texto formateado
    st.write(styled_text_datos, unsafe_allow_html=True)


st.image('Datos/banner.png')

#st.write(""" # ¿QUIÉN RECIBIRÁ EL PRÓXIMO CRÉDITO AZUL?""") 

# Mostrar la lista desplegable en la aplicación Streamlit

st.write(""" ### ANÁLISIS ECONÓMICO-FINANCIERO DE LOS PROSPECTOS """) 

selected_option = st.selectbox('En la siguiente lista desplegable seleccione el prospecto principal para iniciar.', 
                               base_de_prospectos_principales["nombre"])

# A partir del RUC seleccionado, extrae el índice respectivo
indice = int(datos_companias.loc[datos_companias['nombre'] == str(selected_option)].index[0])

# Elimina el nombre de empresa en el archivo datos_companias.csv
datos_companias = datos_companias.drop(['nombre'], axis=1)

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

resultado_final = dataframe_de_resultados(datos_companias_escalado, indice, get_knn, 5, "euclidean")


# Realiza un "merge" para obtener los nombres de las empresas

compania['ruc'] = compania['ruc'].str.lstrip('0')
resultado_final = pd.merge(resultado_final, compania, on='ruc', how='left')
resultado_final = resultado_final.drop(["expediente", "pro_codigo", "Unnamed: 6", "tipo", "provincia"], axis=1)


# Configura los nombres de las columnas

resultado_final = resultado_final.rename({
                                            'ingresos_ventas': 'Ingresos por Ventas (USD)',
                                            'activos': 'Activos (USD)',                                           
                                            'utilidad_neta': 'Utilidad Neta (USD)',
                                            'liquidez_corriente': 'Índice de Liquidez Corriente',                                        
                                            'ruc': 'RUC',
                                            'certificada': 'Certificada',
                                            'nombre': 'Nombre'
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

    colors = {'Si':'#4BC9FF', 'No':'#262730'}

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

    colors = {'Si':'#4BC9FF', 'No':'#262730'}

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

    colors = {'Si':'#4BC9FF', 'No':'#262730'}

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

    colors = {'Si':'#4BC9FF', 'No':'#262730'}

    fig = px.bar(resultado_final, x='RUC', y='Índice de Liquidez Corriente',
                title="Comparación de liquidez corriente",
                width=600, height=400,
                template="simple_white",
                color="Certificada",
                color_discrete_map=colors)

    fig.update_layout(xaxis_title='<b>RUC</b>', yaxis_title='<b> Índice de Liquidez Corriente</b>')

    st.plotly_chart(fig)

# Estilo de dataframe en mode claro
# with tab5:
    
#     st.write(""" #### Prospectos similares a los principales        
#          """)

#     # # Función para resaltar la fila que tiene el número de RUC seleccionado
#     def color_coding(row):
#         return ['background-color:yellow'] * len(row) if row.Nombre == selected_option else ['background-color:white'] * len(row)

#     # # Aplicar el estilo personalizado al dataframe
#     st.dataframe(resultado_final.style.apply(color_coding, axis=1))


with tab5:

    st.write(""" #### Prospectos similares a los principales        
         """)
    
    #Define el estilo de dataframe para el modo oscuro
    custom_css = """
    <style>
        .dataframe { /* Target the DataFrame */
            background-color: #333; /* Change background color to dark gray */
            color: white; /* Change text color to white */
        }
    </style>
    """

    #Muestra el dataframe
    st.write(resultado_final, unsafe_allow_html=True)
    st.markdown(custom_css, unsafe_allow_html=True)  # Inject custom CSS

    
st.write(""" ### UBICACIÓN PROSPECTOS PRINCIPALES """)  


#st.map(coordenadas_prospectos_principales)       

# Calcual el centro
# centro_latitud = coordenadas_prospectos_principales['latitude'].mean() 
# centro_longitud = coordenadas_prospectos_principales['longitude'].mean() 

# Crea el objeto
# attr = (
#     '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> '
#     'contributors, &copy; <a href="https://cartodb.com/attributions">CartoDB</a>'
# )
# tiles = "https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}.png"
#m = folium.Map(location=[centro_latitud, centro_longitud], tiles=tiles, attr=attr, zoom_start=10)
m = folium.Map(location=[-1.20726, -80.37132], zoom_start=7)

# Añadir marcadores al mapa
for idx, row in coordenadas_prospectos_principales.iterrows():
    folium.CircleMarker([row['latitude'], row['longitude']], 
                        popup=row['RUC'], radius=3,
                        weight=0,
                        fill_color='red',
                        fill_opacity=1).add_to(m)

# call to render Folium map in Streamlit
st_data = st_folium(m, width=725)



st.markdown('<sub>Creado por Daniel Pazmiño Vernaza | Contacto: daniel.pazmino.v@gmail.com</sub>', unsafe_allow_html=True)