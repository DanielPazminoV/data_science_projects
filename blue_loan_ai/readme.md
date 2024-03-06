# Blue Loan AI 🌊💲

Blue Loan AI es una plataforma de inteligencia artificial diseñada para ayudar a las instituciones financieras a evaluar y gestionar préstamos azules. 
En su versión de producto mínimo viable (MVP), identifica empresas prospectos para la colocación de estos préstamos.

## Skillset ⚒️

Python 3 (Anaconda installation). Libraries: pandas, matplotlib, sklearn, plotly, folium, streamlit.

## Enlaces 🔗

## Objetivo 🎯

Identificar prospectos de empresas del sector de acuicultura del Ecuador con potencial de recibir préstamos azules.

## Alcance 📐

## Fuentes de datos 🗃️

Para este MVP se utilizaron dos bases de datos:

1.- Registros de la Superintendencia de Compañías de Ecuador.
2.- Empresas de Ecuador que han obtenido una certificación con el "Aquaculture Stewarship Council" (ASC).

Los datos de la Superintendencia de Compañias de Ecuador fueron descargados de la página: https://appscvsmovil.supercias.gob.ec/ranking/reporte.html. Los datos corresponden a los registros del año 2023.

En cuanto a los datos de las empresas del ASC, los mismos se obtuvieron de su página web: https://asc-aqua.org/

## Contexto 📚

## Impacto del Projecto 💥

BlueLoan AI promueve la asignación de préstamos azules a empresas del sector de acuicultura en Ecuador. 
Al dirigir capital hacia estas iniciativas, la plataforma acelera la transición hacia una economía baja en carbono.

## Modelo de Machine Learning 📈

Utiliza el algoritmo “K neareast Neighbors” para identificar compañías similares (vecinas en el espacio vectorial) 
a aquellas que ya han recibido una acreditción del Aquaculture Stwewarshiop Council (ASC)”. 
Se utilizan estos datos como un segundo “proxy”, de la capacidad de la empresa de gestionar proyectos ambientales.

## Aplicación Web 🌐

## Limitaciones MVP 🚦

**Falta de acceso a bases de datos ambientales empresariales**: Un proyecto a gran escala necesitará necesariamente la generación 
de bases de datos ambientales empresarias a nivel nacional. O en su defecto, la inversión para el acceso a APIs internacionales que permitan 
hacer una comparación. En ese sentido, los resultados resultarían ser una aproximación que requerirá una investigación personalizada de cada prospecto. 

**Falta de datos etiquetados**: En virtud de que no se cuenta con información de que empresas ya han recibido préstamos azules, 
no se puede realizar una modelación predictiva supervisada con la mayoría de algoritmos de machine learning. 
En ese sentido se optará por aplicar “K nearest neiborhs” para buscar empresas similares con los pocos datos etiquetados con los que se cuentan.
