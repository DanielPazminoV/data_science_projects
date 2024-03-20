# Blue Loan AI 🌊💲

Blue Loan AI es una plataforma de inteligencia artificial diseñada para ayudar a las instituciones financieras a evaluar y gestionar préstamos azules. 

## Skillset ⚒️

Python 3 (Anaconda installation). Libraries: pandas, matplotlib, sklearn, plotly, folium, streamlit.

- 💻 &nbsp;
  ![Python](https://img.shields.io/badge/-Python-333333?style=flat&logo=python)

- 📚 &nbsp;
  ![Pandas](https://img.shields.io/badge/-Pandas-333333?style=flat&logo=pandas)
  ![Matplotlib](https://img.shields.io/badge/-Matplotlib-333333?style=flat&logo=matplotlib)
  ![Scikitlearn](https://img.shields.io/badge/-Scikitlearn-333333?style=flat&logo=scikitlearn)
  ![Plotly](https://img.shields.io/badge/-Plotly-333333?style=flat&logo=plotly)
  ![Folium](https://img.shields.io/badge/-Folium-333333?style=flat&logo=folium)
  ![Streamlit](https://img.shields.io/badge/-Streamlit-333333?style=flat&logo=streamlit)

- 📊 &nbsp;
![Tableau](https://img.shields.io/badge/-Tableau-333333?style=flat&logo=tableau)

- ⚙️ &nbsp;
  ![Git](https://img.shields.io/badge/-Git-333333?style=flat&logo=git)
  ![GitHub](https://img.shields.io/badge/-GitHub-333333?style=flat&logo=github)
  ![Jupyter](https://img.shields.io/badge/-Jupyter-333333?style=flat&logo=jupyter)
  ![Visual Studio Code](https://img.shields.io/badge/-Visual%20Studio%20Code-333333?style=flat&logo=visual-studio-code&logoColor=007ACC)
  ![Markdown](https://img.shields.io/badge/-Markdown-333333?style=flat&logo=markdown)

## Enlaces 🔗

[La aplicación se encuentra disponible para su uso en este enlace.](https://blueloanai.streamlit.app/)


## Objetivo 🎯

Identificar prospectos de empresas del sector de acuicultura del Ecuador con potencial de recibir préstamos azules.

## Alcance 📐

En su versión de producto mínimo viable (MVP), Blue Loan AI identifica empresas prospectos para la colocación de préstamos azules.

## Fuentes de datos 🗃️

Para este MVP se utilizaron dos bases de datos:

1.- Registros de la Superintendencia de Compañías de Ecuador.
2.- Empresas de Ecuador que han obtenido una certificación con el "Aquaculture Stewarship Council" (ASC).

Los datos de la Superintendencia de Compañias de Ecuador fueron descargados de la página: https://appscvsmovil.supercias.gob.ec/ranking/reporte.html. Los datos corresponden a los registros del año 2023.

En cuanto a los datos de las empresas del ASC, los mismos se obtuvieron de su página web: https://asc-aqua.org/

## Contexto 📚

El término "finanzas azules" se refiere a un enfoque de inversión y gestión financiera que prioriza la sostenibilidad ambiental y la responsabilidad social. Este concepto surge en respuesta a la creciente conciencia sobre el impacto negativo que las actividades económicas pueden tener en el medio ambiente y en las comunidades locales.

El color "azul" se asocia comúnmente con el agua y el medio ambiente, por lo que el término "finanzas azules" enfatiza la importancia de proteger los recursos naturales, especialmente los relacionados con el agua, como mares, océanos, ríos y lagos.

Las finanzas azules abordan tanto la mitigación como la adaptación al cambio climático, financiando proyectos y empresas que promueven la conservación de los recursos hídricos, la gestión sostenible de los océanos, la reducción de la contaminación del agua y la promoción de tecnologías limpias.

Este enfoque también considera la importancia de las comunidades locales y los derechos de las poblaciones que dependen de los recursos marinos y acuáticos para su sustento. Por lo tanto, las finanzas azules pueden incluir inversiones en proyectos que fomenten la equidad social, la creación de empleo local y el empoderamiento de las comunidades costeras.

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
