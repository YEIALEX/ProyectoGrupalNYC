import streamlit as st
from PIL import Image

image = Image.open('Docs/DW_Pipeline.png')
# LINKS
main_repo = 'https://github.com/rupertsky/ProyectoGrupalNYC'
etl = 'https://youtu.be/V90fLjwq7KQ'
#
st.title('Análisis de accidentalidad en la ciudad de New York')

st.header('Overview del proyecto')
st.subheader('_Vista General_')
c1 = st.container()
c1.write('La siniestralidad vial hace referencia al conjunto de eventos trágicos causados generalmente por errores '
         'humanos los cuales se podrían haber evitado. En la ciudad de Nueva York, una de las ciudades más grandes del '
         'mundo con aproximadamente 8.38 millones de habitantes para el 2020, diariamente se registra un gran numero '
         'de siniestros viales. \n'
         'Como principal motivo de este proyecto, se buscan proponer alternativas para la '
         'movilidad vehicular, que permitan reducir la siniestralidad vial de la ciudad de Nueva York')

st.subheader('_Solucion Propuesta_')
c2 = st.container()
c2.write('Para llevar a cabo el proyecto, se ideo un alcance en el que se especifican todas las '
         'caracteristicas que este posee y de esta forma cumplir con el objetivo estrategico.')
c2.caption('_Vista al Proyecto: [GitHub](%s)_' % main_repo)

st.header('ETL del Proyecto')
st.subheader('_Extraccion, Transformacion, Carga de Datos_')
c3 = st.container()
c3.write('El proceso de ETL tiene como principales actores el lenguaje de programacion Python, '
         'el framework Apache Spark, Amazon AWS como encargado de carga incremental, almacenamiento en la nube (RDS) y '
         'finalmente MySQL como motor SQL. El mismo esta programado para ejecutarse todos los dias a las 19:00 GMT-5.')
c3.image(image, caption='DW Pipeline', width=500)
c3.write('Por medio de un video explicativo se demuestra el paso a paso del proceso.')
c3.caption('_Vista ETL: [Ir al Video](%s)_' % etl)

st.markdown("<a href='#an-lisis-de-accidentalidad-en-la-ciudad-de-new-york'>Ir Arriba ^</a>", unsafe_allow_html=True)
