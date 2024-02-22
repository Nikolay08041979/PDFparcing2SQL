from sqlalchemy import create_engine
import psycopg2
from dotenv import load_dotenv
import os
from dataframe_create import get_data_frame_from_json

load_dotenv()
password = os.getenv('DB_PASSWORD')
login = os.getenv('DB_LOGIN')
name_db = os.getenv('DB_NAME')
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')

def export_dataframe_to_sql():
    DSN = f'postgresql://{login}:{password}@{host}:{port}/{name_db}'
    engine = create_engine(DSN)
    dataframe = get_data_frame_from_json()
    dataframe.to_sql('spare_parts', con=engine, if_exists='replace', index=False)
    return 'Данные успешно внесены в базу данных'

def get_count_sql():
    conn = psycopg2.connect(database=name_db, user=login, password=password, host=host, port=port)
    with conn.cursor() as cur:
        cur.execute("""SELECT COUNT(*) FROM spare_parts""")
        count = cur.fetchone()
        return f' Количество записей в базе данных: {count[0]}'
    conn.close()


#print(get_count_sql())
#print(export_dataframe_to_sql())

