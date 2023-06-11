from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, INTEGER, String, TIMESTAMP, BIGINT, BOOLEAN, text, FLOAT
from config.db import Base

class books(Base):
    __tablename__ = "books"
    ISBN = Column(INTEGER, primary_key=True)
    BookTitle = Column(String, nullable=False)
    BookAuthor = Column(String, nullable=False)
    YearOfPublication = Column(INTEGER, nullable=False)
    Publisher = Column(String)
    ImageURLL = Column(String, nullable=False)
    Author = Column(String)
    Summary = Column(String)
    AvgRating = Column(FLOAT)
    CountRating = Column(INTEGER)
    Genres = Column(String)
