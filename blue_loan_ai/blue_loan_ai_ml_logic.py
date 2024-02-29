# Importa librerías
import pandas as pd
import sklearn.neighbors
import sklearn.preprocessing
from sklearn.neighbors import NearestNeighbors
import warnings
warnings.filterwarnings('ignore')

# Carga los datos del proyecto
ciuu = pd.read_csv("Datos/bi_ciiu.csv")
compania = pd.read_csv("Datos/bi_compania.csv") 
ranking = pd.read_csv("Datos/bi_ranking.csv", low_memory=False) 
segmento = pd.read_csv("Datos/bi_segmento.csv")
companias_certificadas_asc = pd.read_excel('Datos/companias_asc.xlsx')

# Convierte los datos de ruc en cadenas
companias_certificadas_asc['ruc'] = companias_certificadas_asc['ruc'].astype(str)

# Agrega ceros a los datos de ruc
companias_certificadas_asc['ruc'] = companias_certificadas_asc['ruc'].apply(lambda x: '0' + x if x[0] != '1' else x)

# Join no. 1
datos_companias_join_1 = pd.merge(compania,companias_certificadas_asc, on = "ruc", how='outer')

# Filtra los datos de la SuperCias para acuicultura
ranking["ciiu_n6"] = ranking['ciiu_n6'].fillna('')
ranking_ciiu_A032 = ranking[ranking['ciiu_n6'].str.contains('A032')]

 # Join no. 2
datos_companias = pd.merge(datos_companias_join_1, ranking_ciiu_A032, on = "expediente", how='outer')
datos_companias = datos_companias.drop_duplicates(subset=['ruc'])

# Elimina columnas que no son necesarias para la modelación
datos_companias = datos_companias.drop(["anio", 
                                            "posicion_general",
                                           "id_estado_financiero",
                                            "ciiu_n1",
                                            "ciiu_n6",
                                            "Unnamed: 6", 
                                            "expediente",
                                            "tipo",
                                            "pro_codigo",
                                            "provincia",
                                            "nombre_compania"
                                           ], axis=1)

# Filtra las empresas con índice de liquidez corriente mayor o igual a 1.
datos_companias = datos_companias[datos_companias['liquidez_corriente'] >= 1]

# Filtra la base de prospectos principales
base_prospectos_principales = datos_companias[datos_companias['certificada'] == 1]
ruc = base_prospectos_principales['ruc']
mask = compania['ruc'].isin(ruc)
base_prospectos_principales = compania[mask]
base_prospectos_principales = base_prospectos_principales.drop(["expediente", "pro_codigo", "Unnamed: 6", "tipo"], axis=1)
base_prospectos_principales.to_csv('base_prospectos_principales_copy.csv', index=False)

# Rellena de datos 
datos_companias['certificada'] = datos_companias['certificada'].fillna(0)
datos_companias[['apalancamiento', 
                 'apalancamiento_financiero',
                 'apalancamiento_c_l_plazo',
                 'margen_operacional',
                 'gastos_financieros',
                 'end_patrimonial_nct',
                 'gastos_admin_ventas',
                 'depreciaciones',
                 'amortizaciones',
                 'costos_ventas_prod',
                 'deuda_total_c_plazo',
                 'deuda_total',
                 'total_gastos'       
                ]] = datos_companias[['apalancamiento', 
                 'apalancamiento_financiero',
                 'apalancamiento_c_l_plazo',
                 'margen_operacional',
                 'gastos_financieros',
                 'gastos_admin_ventas',
                 'depreciaciones',
                 'amortizaciones',
                 'costos_ventas_prod',
                 'end_patrimonial_nct',
                 'deuda_total_c_plazo',
                 'deuda_total',
                 'total_gastos']].fillna(
                datos_companias[['apalancamiento', 
                 'apalancamiento_financiero',
                 'apalancamiento_c_l_plazo',
                 'margen_operacional',
                 'gastos_financieros',
                 'gastos_admin_ventas',
                 'depreciaciones',
                 'end_patrimonial_nct',
                 'amortizaciones',
                 'costos_ventas_prod',
                 'deuda_total_c_plazo',
                 'deuda_total',
                 'total_gastos']].median())

# Selección de variables
datos_companias = datos_companias[['cia_imvalores', 'ingresos_ventas', 'activos', 
                          'patrimonio', 'utilidad_an_imp',
                          'impuesto_renta', 'n_empleados',
                          'ingresos_totales', 'utilidad_ejercicio',
                          'total_gastos', 'ruc', 'certificada']]
datos_companias = datos_companias.reset_index(drop=True)

# Guarda los datos de las companias seleccionadas para el análisis
datos_companias.to_csv('datos_companias_copy.csv', index=False)  

# Escalado de datos
feature_names = ['cia_imvalores', 'ingresos_ventas', 'activos', 
                          'patrimonio', 'utilidad_an_imp',
                          'impuesto_renta', 'n_empleados',
                          'ingresos_totales', 'utilidad_ejercicio',
                          'total_gastos']
transformer_mas = sklearn.preprocessing.MaxAbsScaler().fit(datos_companias[feature_names].to_numpy())
datos_companias_escalado = datos_companias.copy()
datos_companias_escalado.loc[:, feature_names] = transformer_mas.transform(datos_companias[feature_names].to_numpy())

# Función que devuelve los vecinos más cercanos 
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

# Registros de compañías certificadas
datos_companias_certificadas = datos_companias[datos_companias["certificada"] == 1] 
datos_companias_certificadas

# Función que devuelve la base de prospectos ampliada
def dataframe_de_resultados(df1, df2, func, param1, param2):

    resultados = []
    for index in df1.index:
        resultado = func(df2, index, param1, param2) 
        resultados.append(resultado)
    
    # Concatena los resultados en un nuevo DataFrame
    nuevo_df = pd.concat(resultados)
    
    # Elimina los duplicados
    nuevo_df = nuevo_df.drop_duplicates(subset='ruc', keep='first')
    
    # Elimina los datos de las empresas certificadas
    
    nuevo_df = nuevo_df[nuevo_df.certificada == 0]
    
    # Devuelve los ceros a la columna de RUC
    
    nuevo_df['ruc'] = nuevo_df['ruc'].map(str)
    #nuevo_df['ruc'] = nuevo_df['ruc'].apply(lambda x: '0' + x if x[0] != '1' else x)
    
    ruc = nuevo_df['ruc']
    
    # Realiza un "join" para obtener los datos completos de las empresas
    mask = compania['ruc'].isin(ruc)
    df_final = compania[mask]
    df_final = df_final.drop(["expediente", "pro_codigo", "Unnamed: 6", "tipo"], axis=1)
    
    return df_final

# Llamado a la función que devuelve la base de prospectos ampliada
resultados = dataframe_de_resultados(datos_companias_certificadas, datos_companias_escalado, get_knn, 10, "euclidean")
resultados.to_csv('base_de_prospectos_ampliada_copy.csv', index=False) 



