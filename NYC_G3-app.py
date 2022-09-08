import streamlit as st
from PIL import Image

image = Image.open('Docs/images/DW_Pipeline.png')
image2 = Image.open('Docs/images/crash.jpg')
image3 = Image.open('Docs/images/gitpng.png')
image4 = Image.open('Docs/images/youtube-logo-5-2.png')
image5 = Image.open('Docs/images/henry.png')
# LINKS
main_repo = 'https://github.com/rupertsky/ProyectoGrupalNYC'
etl = 'https://youtu.be/V90fLjwq7KQ'
docs = 'https://github.com/rupertsky/ProyectoGrupalNYC/tree/main/Docs'
dash = 'https://github.com/rupertsky/ProyectoGrupalNYC/tree/main/Visualizaci%C3%B3n'
ia = 'https://rupertsky-proyectogrupalnyc-nyc-g3-app-tchzrg.streamlitapp.com/Predictor_Accidentados'
#
st.title('Análisis de accidentalidad en la ciudad de New York')

st.markdown('**Integrantes**')
st.caption('_Carlos Gaviria_')
st.caption('_Jean Carlos Betancourt_')
st.caption('_Alexander Imbachi_')
st.caption('_Juan Diego Gutierrez_')

st.header('Overview del proyecto')
st.subheader('_Vista General_')

c1 = st.container()
c1.write('La siniestralidad vial hace referencia al conjunto de eventos trágicos causados generalmente por errores '
         'humanos los cuales se podrían haber evitado. En la ciudad de Nueva York, una de las ciudades más grandes del '
         'mundo con aproximadamente 8.38 millones de habitantes para el 2020, diariamente se registra un gran numero '
         'de siniestros viales. '
         'Como principal objetivo de este proyecto, se busca proponer alternativas para la '
         'movilidad vehicular, que permitan reducir la siniestralidad vial de la ciudad de Nueva York')
c1.image(image2, caption='Accidente', width=350)

st.subheader('_Solución Propuesta_')
c2 = st.container()
c2.write('Para llevar a cabo el proyecto, se ideo un alcance en el que se especifican todas las '
         'características que este posee y de esta forma cumplir con el objetivo estratégico.')
c2.caption('_Vista al Proyecto: [GitHub](%s)_' % main_repo)
c2.image(image3, width=15)

st.header('ETL del Proyecto')
st.subheader('_Extracción, Transformación, Carga de Datos_')

c3 = st.container()
c3.write('El proceso de ETL tiene como principales actores el lenguaje de programación Python, '
         'el framework Apache Spark, Amazon AWS como encargado de carga incremental, almacenamiento en la nube (RDS) y '
         'finalmente MySQL como motor SQL. El mismo esta programado para ejecutarse todos los dias a las 19:00 GMT-5.')
c3.image(image, caption='DW Pipeline', width=350)
c3.write('Por medio de un video explicativo se demuestra el paso a paso del proceso.')
c3.caption('_Vista ETL: [Ir al Video](%s)_' % etl)
c3.image(image4, width=15)

st.header('Entregables')
st.subheader('_Dashboard, Documentación_')

c4 = st.container()
c4.write('Power BI, es una herramienta de visualización y análisis de datos enfocada a la productividad empresarial, '
         'por este motivo, se implemento un Dashboard en el que se evidencian diferentes tipos de siniestralidad, '
         'como por ejemplo accidentes por calle, tipo, trafico, etc. De esta forma se pueden tomar decisiones '
         'que disminuyan aquellas estadísticas con el fin de mejorar la calidad vial en la ciudad de New York.')
c4.write('Por otro lado, se realizo un aplicativo de Inteligencia Artificial, encargado de predecir los siniestros '
         'que ocurrirán en determinada Fecha, Dia, Hora, y Distrito. Esta herramienta es de vital importancia, ya que '
         'predecir los siniestros de X lugar a Y hora, nos da una ventana gigantesca de tiempo para manejar mejor '
         'los recursos y servicios, destinados a la atención de siniestros en multiples zonas.')
c4.write('Adicionalmente, se hace entrega del respectivo Manual de Usuario para el correcto manejo del Dashboard y '
         'de esta forma, aprovechar al máximo sus capacidades.')
c4.caption('_Para acceder a Documentos ingrese aquí: [Docs](%s)_' % docs,)
c4.caption('_Para acceder a Dashboard ingrese aquí: [Dashboard](%s)_' % dash)
c4.caption('_Para acceder a Predictor ingrese aquí: [IA](%s)_' % ia)

c4.image(image5, width=30)
st.caption('_**HENRY**_')
st.markdown("<a href='#an-lisis-de-accidentalidad-en-la-ciudad-de-new-york'>Ir Arriba ^</a>", unsafe_allow_html=True)
