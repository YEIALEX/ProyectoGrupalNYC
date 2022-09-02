from db_back.db_conn import engine
import pandas as pd

collision = pd.read_sql('SELECT * FROM collision', engine)
