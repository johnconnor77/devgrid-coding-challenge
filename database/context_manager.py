from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker


#DATABASE_URL = "sqlite:///./test.db"
DATABASE_URL = "postgresql://postgres:postgres@postgres:5432/test-db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = MetaData()

