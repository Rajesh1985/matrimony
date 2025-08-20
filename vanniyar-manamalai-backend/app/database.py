# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 👇 GLOBAL CONFIG
DB_SERVER = "localhost"           # Change to remote address later
DB_NAME = "manamalai"
DB_USER = "manamalai"
DB_PASSWORD = "Cvm_1234"
DB_DRIVER = "ODBC Driver 17 for SQL Server"

# Format: mssql+pyodbc://user:password@server/database?driver=...
DATABASE_URL = (
    f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME}"
    f"?driver={DB_DRIVER.replace(' ', '+')}"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
