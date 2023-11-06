
# Import necessary modules
from config.db_config import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
load_dotenv()

from models.db_model import Base


DB_URL = f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
engine = create_engine(DB_URL, echo=True, pool_size=30, max_overflow=0, pool_recycle=3600)

# Create the tables in the database
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)
