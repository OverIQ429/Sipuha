from sqlalchemy import create_engine
from .models import Base, User
db_user = 'postgres'
db_password = 'postgres'
db_host = 'localhost'
db_port = '5432'
db_name = 'postgres'
SQLALCHEMY_DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
def create_tables():
    Base.metadata.create_all(bind=engine)