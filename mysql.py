from datetime import datetime

from sqlalchemy import MetaData
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, Table

from config import db_host, db_user, db_password, db_name


def create_connection(login, password, database, host='localhost', port=3306):
    engine = create_engine(f'mysql+pymysql://{login}:{password}@{host}:{port}/{database}', echo=False)
    return engine


def create_table(engine, table_name):
    metadata = MetaData()
    table = Table(table_name, metadata,
                  Column('id', Integer, primary_key=True),
                  Column('zpid', Integer),
                  Column('address', String(255)),
                  Column('city', String(255)),
                  Column('state', String(255)),
                  Column('zipcode', String(255)),
                  Column('price', Integer),
                  Column('beds', Integer),
                  Column('baths', Float),
                  Column('statusType', String(255)),
                  Column('statusText', String(255)),
                  Column('area', Integer),
                  Column('isZillowOwned', Boolean),
                  Column('BrokerName', String(255)),
                  Column('detailUrl', String(255)))

    metadata.create_all(engine)
    return table


def insert_data(engine, table, data):
    with engine.connect() as conn:
        query = table.insert().values(zpid=data[0], address=data[1], city=data[2], state=data[3], zipcode=data[4],
                                      price=data[5], beds=data[6], baths=data[7], statusType=data[8],
                                      statusText=data[9], area=data[10], isZillowOwned=data[11], BrokerName=data[12],
                                      detailUrl=data[13])
        conn.execute(query)


def save_data(data):
    engine = create_connection(db_user, db_password, db_name, db_host)
    table = create_table(engine, 'zillow{}'.format(datetime.now().strftime('%H%M%S')))
    for i in data:
        insert_data(engine, table, i)
