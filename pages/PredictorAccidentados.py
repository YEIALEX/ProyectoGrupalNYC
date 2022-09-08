from db_back.db_table import collision
import pandas as pd
import numpy as np
import datetime as dt
import time
import math

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
import matplotlib.pyplot as plt
import streamlit as st

import seaborn as sns
sns.set()

# Filtro y procesamiento de tabla collision, principal en la base de datos
collision.drop(collision.filter(regex='vehicle_2|vehicle_3|vehicle_4|vehicle_5|code_2|code_3|code_4|code_5|killed'
                                      '|motorist|cyclist|pedestrians').columns,
               axis=1, inplace=True)
collision = collision.convert_dtypes()
collision['Date'] = pd.to_datetime(collision['Date'], format="%Y/%m/%d")
collision['Time'] = collision['Time'] = pd.to_datetime(collision['Time'], format="%H:%M")
collision['number_of_persons_injured'] = collision['number_of_persons_injured'].fillna(0)

# Eliminacion de NaN y Outliers
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

# Union de dataframes filtrados para el modelado
dataset = pd.merge(df3, df2, left_index=True, right_index=True)
dataset.reset_index(inplace=True)
dataset['crash_date_time'] = pd.to_datetime(dataset['crash_date_time'], format="%Y-%m-%d %H:%M:%S")

dataset['Year'] = dataset['crash_date_time'].dt.year
dataset['Month'] = dataset['crash_date_time'].dt.month
dataset['Day'] = dataset['crash_date_time'].dt.day
dataset['Hour'] = dataset['crash_date_time'].dt.hour

dataset = dataset.groupby(['Year', 'Month', 'Day', 'Hour', 'Borough', 'on_street_name']).sum()
dataset.reset_index(inplace=True)
distritos = {
        'Manhattan': 0,
        'Brooklyn': 1,
        'Queens': 2,
        'Bronx': 3,
        'Staten Island': 4
    }
########################################################################################################################
st.title('**_Predictor de Accidentados | NYC_**')
page_names = ['Dia', 'Dia y Hora']
# Entrenamiento del modelo x dia
data_byday = pd.DataFrame(dataset.groupby(['Year', 'Month', 'Day', 'Borough'])['number_of_persons_injured']
                          .sum().reset_index())
data_byday.Borough = data_byday.Borough.map({
    'Manhattan': 0,
    'Brooklyn': 1,
    'Queens': 2,
    'Bronx': 3,
    'Staten Island': 4
})

X = data_byday[['Year', 'Month', 'Day', 'Borough']].values
y = data_byday.number_of_persons_injured.values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.35, random_state=37)

reg_tree = DecisionTreeRegressor(criterion='squared_error', max_depth=18, random_state=37)
reg_tree.fit(X_train, y_train)

########################################################################################################################
# Entrenamiento del modelo x hora
data_byhour = pd.DataFrame(dataset.groupby(['Year', 'Month', 'Day', 'Hour', 'Borough'])['number_of_persons_injured']
                           .sum().reset_index())
data_byhour.Borough = data_byhour.Borough.map({
    'Manhattan': 0,
    'Brooklyn': 1,
    'Queens': 2,
    'Bronx': 3,
    'Staten Island': 4
})

X2 = data_byhour[['Year', 'Month', 'Day', 'Hour', 'Borough']].values
y2 = data_byhour.number_of_persons_injured.values

X2_train, X2_test, y2_train, y2_test = train_test_split(X2, y2, test_size=0.35, random_state=38)

reg_tree2 = DecisionTreeRegressor(criterion='squared_error', max_depth=20, random_state=0)
reg_tree2.fit(X2_train, y2_train)

########################################################################################################################
def main():
    page = st.radio('Seleccione el modo', page_names)
    if page == 'Dia':
        with st.form(key='dia'):
            d = st.date_input('Ingrese la fecha')
            district = st.selectbox('Seleccione el distrito', dataset.Borough.unique())
            day_injuries = reg_tree.predict([[d.year, d.month, d.day, distritos[district]]])
            day_sub = st.form_submit_button('Calcular')
        if day_sub:
            st.write('El numero aproximado de personas accidentadas es: ', math.ceil(day_injuries[0]))

    if page == 'Dia y Hora':
        with st.form(key='dia'):
            d = st.date_input('Ingrese la fecha')
            h = st.time_input('Ingrese la hora')
            district2 = st.selectbox('Seleccione el distrito', dataset.Borough.unique())
            hour_injuries = reg_tree2.predict([[d.year, d.month, d.day, h.hour, distritos[district2]]])
            hour_sub = st.form_submit_button('Calcular')
        if hour_sub:
            st.write(f'El numero aproximado de personas accidentadas a las {h.hour} horas es: '
                     f'{math.ceil(hour_injuries[0])}')


if __name__ == '__main__':
    main()
