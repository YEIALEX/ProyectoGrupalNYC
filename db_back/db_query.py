from db_conn import engine
from sodapy import Socrata
import pandas as pd


def df_sql(dataframe, tbl_name, table):
    return dataframe.to_sql(tbl_name, con=engine, index=False, schema=table, if_exists='append')


client = Socrata("data.cityofnewyork.us", 'MEDcEGe0ri1vxGecOfDXDb4dQ')
results = client.get("h9gi-nx95", limit=2000000)
df = pd.DataFrame(results)

if __name__ == '__main__':
    df_sql(df, 'nyc_api', 'nyc')
