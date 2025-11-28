# Dependency to get DB session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 👇 GLOBAL CONFIG
# Connection details
MYSQL_USER = "manamalai"
MYSQL_PASSWORD = "Chenagai_12345"
MYSQL_HOST = "127.0.0.1"  # Localhost because of SSH tunnel
MYSQL_PORT = 3306         # Local port forwarded to remote 3306
MYSQL_DB = "manamalai_dev"

# SQLAlchemy connection string
connection_url = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"

# Create engine and session
engine = create_engine(connection_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()