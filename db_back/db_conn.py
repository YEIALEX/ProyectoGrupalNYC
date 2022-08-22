from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists

url = 'mysql://admin:dNUDifZnz5V4QiH@nyc-1.cidguezqij2o.us-east-1.rds.amazonaws.com/nyc'
engine = create_engine(url)

if not database_exists(engine.url):
    create_database(engine.url)

if __name__ == '__main__':
    connect = engine.connect()
