from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Table
from sqlalchemy import MetaData
import datetime

def create_connection(login, password, database, host='localhost', port=3306):
    engine = create_engine(f'mysql+pymysql://{login}:{password}@{host}:{port}/{database}', echo=False)
    return engine

def create_table(engine, table_name):
    metadata = MetaData()
    table = Table(table_name, metadata,
                  Column('id', Integer, primary_key=True),
                  Column('address', String(255)),
                    Column('city', String(255)),
                    Column('state', String(255)),
                    Column('zipcode', String(255)),
                    Column('price', Integer),
                    Column('beds', Integer),
                    Column('baths', Float))
    metadata.create_all(engine)
    return table

def insert_data(engine, table, data):
    with engine.connect() as conn:
        querry = table.insert().values(address=data[0], city=data[1], state=data[2], zipcode=data[3], price=data[4], beds=data[5], baths=data[6])
        conn.execute(querry)

def save_data(data):
    engine = create_connection('root', '602364', 'zillowdb')
    table = create_table(engine, 'zillow{}'.format(datetime.datetime.now().strftime('%H%M%S')))
    for i in data:
        insert_data(engine, table, i)