from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

from models import Base

DB_NAME = "olist_db"

def make_url(database):
    return URL.create(
        "mssql+pyodbc",
        host="localhost",
        database=database,
        query={
            "driver": "ODBC Driver 18 for SQL Server",
            "TrustServerCertificate": "yes",
            "Trusted_Connection": "yes",
        },
    )

# 1. Create the database
master_engine = create_engine(make_url("master"), isolation_level="AUTOCOMMIT")
with master_engine.connect() as conn:
    conn.execute(text(f"IF DB_ID('{DB_NAME}') IS NULL CREATE DATABASE [{DB_NAME}]"))
print(f"Database '{DB_NAME}' ready.")

# 2. Create the empty tables inside it
engine = create_engine(make_url(DB_NAME))
Base.metadata.create_all(engine)
print("Tables created:", ", ".join(Base.metadata.tables))