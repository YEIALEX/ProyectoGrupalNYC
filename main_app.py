from db_back.db_conn import engine
import pandas as pd
import numpy as np
import datetime as dt
import time

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import seaborn as sns

import warnings

warnings.filterwarnings('once')


def get_sec(time_str):
    """Get seconds from time."""
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)


def reg_prep_data(data1, data2):
    """
    Funcion que recibe columnas de datos para entrenar X & Y.

    Parametros
    ----------
    :param data1: Valores de X
    :param data2: Valores de Y

    Return
    ----------
    :return: Tupla contenedora de np.array
    Shape 2
    """
    try:
        x = data1.values
        y = data2.values
        x = x.reshape(-1, 1)
        return x, y
    except Exception as e:
        return e


collision = pd.read_sql('SELECT * FROM collision', engine)
bicycle = pd.read_sql('SELECT * FROM bicycle', engine)
routes = pd.read_sql('SELECT * FROM routes', engine)
traffic = pd.read_sql('SELECT * FROM traffic', engine)

# Eliminacion de columnas que no aportan mucho al modelado
collision.drop(collision.filter(regex='vehicle_2|vehicle_3|vehicle_4|vehicle_5|code_2|code_3|code_4|code_5').columns,
               axis=1, inplace=True)
collision = collision.convert_dtypes()

# Asignacion de tipo correcto de dato en fechas
collision['Date'] = pd.to_datetime(collision['Date'], format="%Y/%m/%d")
collision['Date'] = collision['Date'].map(dt.datetime.toordinal)

# Transformacion de tipo de dato Date a Int
collision['Time'] = collision['Time'] = pd.to_datetime(collision['Time'], format="%H:%M")
collision['Time'] = collision['Time'].apply(lambda x: int(get_sec(str(x.time()))))
collision['crash_date_time'] = pd.to_datetime(collision['crash_date_time'], format='%Y/%m/%d %H:%M:%S')
collision['crash_date_time'] = collision['crash_date_time'].apply(lambda x: time.mktime(x.timetuple()))
collision['number_of_persons_injured'] = collision['number_of_persons_injured'].fillna(0)

# Filtro por columna elegida para el modelado
regtree = collision.drop(columns=['Borough', 'Zip_code', 'Latitude', 'Longitude', 'Street_name',
                                  'contributing_factor_vehicle_1', 'vehicle_type_code_1', 'off_street_name'], axis=1)
regtree = regtree.groupby(['Time', 'Date'])[['number_of_persons_injured']].sum().reset_index()
total = regtree.groupby('Time')['number_of_persons_injured'].sum().reset_index()
dates = regtree.drop_duplicates(subset='Time')
dates = dates.drop(columns='number_of_persons_injured')
regtree = pd.merge(dates, total)

# Eliminacion de outliers (2 veces para mas precision)
for i in range(2):
    Q1 = np.percentile(regtree['number_of_persons_injured'], 25,
                       method='midpoint')

    Q3 = np.percentile(regtree['number_of_persons_injured'], 75,
                       method='midpoint')
    IQR = Q3 - Q1

    # Upper bound
    upper = np.where(regtree['number_of_persons_injured'] >= (Q3 + 1.5 * IQR))
    # Lower bound
    lower = np.where(regtree['number_of_persons_injured'] <= (Q1 - 1.5 * IQR))

    ''' Removing the Outliers '''
    regtree.drop(upper[0], inplace=True)
    regtree.drop(lower[0], inplace=True)
    regtree = regtree.reset_index(drop=True)
##########################################################################################
# Grafico de los datos a medir
sns.scatterplot(data=regtree, x='Time', y='number_of_persons_injured')

##########################################################################################
# Primer modelo de prueba
model = LinearRegression(fit_intercept=True)
x, y = reg_prep_data(regtree[['Time']], regtree['number_of_persons_injured'])
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.7, random_state=33)
model.fit(X_train, y_train)

y_train_pred = model.predict(X_train)
y_test_pred = model.predict(X_test)

print('Error en datos de train:', mean_squared_error(y_train, y_train_pred))
print('Error en datos de test:', mean_squared_error(y_test, y_test_pred))

plt.figure(figsize=(7, 6))
plt.scatter(X_train, y_train, color='green', label='Blue Train')
plt.plot(X_train, y_train_pred, color='k', linestyle='--', label='Prediccion Train')

plt.scatter(X_test, y_test, color='blue', label='Blue Test')
plt.plot(X_test, y_test_pred, color='red', linewidth=3.0, label='Prediccion Test')

plt.legend()
plt.show()
##########################################################################################
# Modelo de prediccion
modelo = LinearRegression()
modelo.fit(regtree[['Date', 'Time']], regtree.number_of_persons_injured)
# Recibe fecha (ordinal) y hora (segundos)
modelo.predict([[737435, 60000]])
