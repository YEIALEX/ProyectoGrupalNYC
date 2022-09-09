from db_back.db_table import collision
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

# LINKS
ia = 'https://rupertsky-proyectogrupalnyc-nyc-g3-app-tchzrg.streamlitapp.com/Predictor_Accidentados'

# Filtro y procesamiento de tabla collision, principal en la base de datos
collision.drop(collision.filter(regex='vehicle_2|vehicle_3|vehicle_4|vehicle_5|code_2|code_3|code_4|code_5|killed'
                                      '|motorist|cyclist|pedestrians').columns,
               axis=1, inplace=True)
collision = collision.convert_dtypes()
collision['Date'] = pd.to_datetime(collision['Date'], format="%Y/%m/%d")
collision['Time'] = collision['Time'] = pd.to_datetime(collision['Time'], format="%H:%M")
collision['number_of_persons_injured'] = collision['number_of_persons_injured'].fillna(0)

# Eliminación de NaN y Outliers
df = collision.copy()
df = df.drop(df[(df['Borough'] == 'Sin Dato') | (df['on_street_name'] == 'Sin Dato')].index, axis=0)
df.reset_index(drop=True, inplace=True)

for i in range(2):
    Q1 = np.percentile(df['number_of_persons_injured'], 25,
                       method='midpoint')

    Q3 = np.percentile(df['number_of_persons_injured'], 75,
                       method='midpoint')
    IQR = Q3 - Q1

    # Upper bound
    upper = np.where(df['number_of_persons_injured'] >= (Q3 + 1.5 * IQR))
    # Lower bound
    lower = np.where(df['number_of_persons_injured'] <= (Q1 - 1.5 * IQR))

    df.drop(upper[0], inplace=True)
    df.drop(lower[0], inplace=True)
    df = df.reset_index(drop=True)

df2 = pd.DataFrame(df.groupby('crash_date_time')['number_of_persons_injured'].sum())

df3 = df[['crash_date_time', 'Borough', 'on_street_name']]
df3 = df3.drop_duplicates(subset='crash_date_time')
df3.sort_values(by='crash_date_time', inplace=True)
df3.set_index('crash_date_time', inplace=True)

# Union de dataframes filtrados para la visualización
dataset = pd.merge(df3, df2, left_index=True, right_index=True)
dataset.reset_index(inplace=True)
dataset['crash_date_time'] = pd.to_datetime(dataset['crash_date_time'], format="%Y-%m-%d %H:%M:%S")

dataset['Year'] = dataset['crash_date_time'].dt.year
dataset['Month'] = dataset['crash_date_time'].dt.month
dataset['Day'] = dataset['crash_date_time'].dt.day
dataset['Hour'] = dataset['crash_date_time'].dt.hour

dataset = dataset.groupby(['Year', 'Month', 'Day', 'Hour', 'Borough', 'on_street_name']).sum()
dataset.reset_index(inplace=True)

# Visualización de los datos
st.title('Predictor de Accidentados por Ciudad')
st.caption('**_New York City_**')
#########################################################
st.header('Vista general de heridos por accidentes | NYC')
st.subheader('_Vista por Mes de heridos en accidentes | NYC_')
fig = plt.figure(figsize=(12, 6))
sns.countplot(data=dataset, x='Month', palette='viridis')
st.pyplot(fig)
with st.expander('Ver mas...'):
    st.write('Se entiende por meses con mayor numero de personas involucradas en accidentes, '
             'aquellos cuya eventualidad esta representada por: Navidad, Vacaciones de verano/Fin de año. '
             'Representando asi mayor flujo de personas.')
#########################################################
st.subheader('_Vista por Dia de heridos en accidentes | NYC_')
fig2 = plt.figure(figsize=(12, 6))
sns.countplot(data=dataset, x='Day', palette='mako_r')
st.pyplot(fig2)
with st.expander('Ver mas...'):
    st.write('En lo que a dias se refiere, durante el 90% de estos la accidentalidad se mantiene "estable", '
             'a diferencia de los dias finales del mes, en los que esta baja casi un 50%.')
#########################################################
st.subheader('_Vista por Hora de heridos en accidentes | NYC_')
fig3 = plt.figure(figsize=(12, 6))
sns.countplot(data=dataset, x='Hour', palette='flare')
st.pyplot(fig3)
with st.expander('Ver mas...'):
    st.write('La vista por horas demuestra que durante la madrugada los accidentes son mínimos, pero, '
             'estos incrementan a lo largo del dia con su máximo en las horas pico (16h/17h/18h).')
#########################################################
st.subheader('_Vista general por Distrito | NYC_')
fig4 = plt.figure(figsize=(12, 6))
sns.countplot(data=dataset, x='Borough')
st.pyplot(fig4)
with st.expander('Ver mas...'):
    st.write('Los distritos con mayor numero de personas '
             'son aquellos que representan mayor accidentalidad en la ciudad.')
st.caption('_Para acceder a Predictor ingrese aquí: [IA](%s)_' % ia)
