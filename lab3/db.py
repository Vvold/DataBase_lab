import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URI = 'postgresql+psycopg2://postgres:Vb09gh54ty12@localhost/music_service'
Library = declarative_base()
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)