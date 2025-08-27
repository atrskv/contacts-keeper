import os
import psycopg2
from app.data.repository import ContactsRepository


DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')


def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD
    )
    return conn


conn = get_db_connection()

repo = ContactsRepository(conn)
repo.generate_contacts_data(100)
