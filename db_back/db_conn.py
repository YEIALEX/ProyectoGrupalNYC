from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists
import streamlit as st

url = f'mysql://{st.secrets["DB_USERNAME"]}:{st.secrets["DB_PASSWORD"]}@{st.secrets["DB_URL"]}'
engine = create_engine(url)

if not database_exists(engine.url):
    create_database(engine.url)

if __name__ == '__main__':
    connect = engine.connect()
