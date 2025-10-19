from sqlalchemy import create_engine, text

# Connection details
MYSQL_USER = "manamalai"
MYSQL_PASSWORD = "Chenagai_12345"
MYSQL_HOST = "127.0.0.1"  # Localhost because of SSH tunnel
MYSQL_PORT = 3306         # Local port forwarded to remote 3306
MYSQL_DB = "manamalai_db"

# SQLAlchemy connection string
connection_url = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"

# Create engine
engine = create_engine(connection_url, echo=True)

# Sample query
with engine.connect() as conn:
    result = conn.execute(text("SHOW TABLES"))
    print("Tables in database:")
    for row in result:
        print(row[0])