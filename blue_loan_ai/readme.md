# Blue Loan AI

Blue Loan AI es una plataforma de inteligencia artificial diseñada para ayudar a las instituciones financieras a evaluar y gestionar préstamos azules. 
En su versión MVP, identifica empresas prospectos para la colocación de estos préstamos.

## Skillset

## Enlaces

## Objetivo

## Alcance

## Fuentes de datos

## Contexto

## Impacto del Projecto 

BlueLoan AI promueve la asignación de préstamos azules a empresas del sector de acuicultura en Ecuador. 
Al dirigir capital hacia estas iniciativas, la plataforma acelera la transición hacia una economía baja en carbono.

## Modelo de Machine Learning

Utiliza el algoritmo “K neareast Neighbors” para identificar compañías similares (vecinas en el espacio vectorial) 
a aquellas que ya han recibido una acreditción del Aquaculture Stwewarshiop Council (ASC)”. 
Se utilizan estos datos como un segundo “proxy”, de la capacidad de la empresa de gestionar proyectos ambientales.

## Aplicación Web

## Limitaciones MVP

**Falta de acceso a bases de datos ambientales empresariales**: Un proyecto a gran escala necesitará necesariamente la generación 
de bases de datos ambientales empresarias a nivel nacional. O en su defecto, la inversión para el acceso a APIs internacionales que permitan 
hacer una comparación. En ese sentido, los resultados resultarían ser una aproximación que requerirá una investigación personalizada de cada prospecto. 

**Falta de datos etiquetados**: En virtud de que no se cuenta con información de que empresas ya han recibido préstamos azules, 
no se puede realizar una modelación predictiva supervisada con la mayoría de algoritmos de machine learning. 
En ese sentido se optará por aplicar “K nearest neiborhs” para buscar empresas similares con los pocos datos etiquetados con los que se cuentan. 
Además, se aplicará la misma metodología con otros “proxys” (empresas que han recibido préstamos verdes y 
empresas que cuenten con buenos índices de sostenibilidad). No obstante, los resutlados podrían ser imprecisos. 
Por ejemplo, se podrían identificar empresas que ya hayan recibido préstamos verdes pero que no lo sepamos por falta de cruce de 
información entre instituciones financieras.
