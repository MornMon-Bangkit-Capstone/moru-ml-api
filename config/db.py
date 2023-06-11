from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

mysql_user = os.environ.get("DATABASE_USER")
mysql_password = os.environ.get("DATABASE_PASSWORD")
mysql_port = os.environ.get("DATABASE_PORT")
mysql_database = os.environ.get("DATABASE")
mysql_host = os.environ.get("DATABASE_HOST")
# MYSQL_URL = f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_database}"
MYSQL_URL= "mysql+pymysql://root:an1m3w1bu@34.128.102.196:3306/moru_database?charset=utf8"
POOL_SIZE = 20
POOL_RECYCLE = 3600
POOL_TIMEOUT = 15
MAX_OVERFLOW = 2
CONNECT_TIMEOUT = 60

# class Database():
#     def __init__(self) -> None:
#         self.connection_is_active = False
#         self.engine = None

#     def get_db_connection(self):
#         if self.connection_is_active == False:
#             connect_args = {"connect_timeout":CONNECT_TIMEOUT}
#             try:
#                 self.engine = create_engine(MYSQL_URL, pool_size=POOL_SIZE, pool_recycle=POOL_RECYCLE,
#                         pool_timeout=POOL_TIMEOUT, max_overflow=MAX_OVERFLOW, connect_args=connect_args)
#                 return self.engine
#             except Exception as ex:
#                 print("Error connecting to DB : ", ex)
#         return self.engine

#     def get_db_session(self,engine):
#         try:
#             Session = sessionmaker(bind=engine)
#             session = Session()
#             return session
#         except Exception as ex:
#             print("Error getting DB session : ", ex)
#             return None
engine = create_engine(MYSQL_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()