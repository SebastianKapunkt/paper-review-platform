from sqlalchemy import Table, Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    paper_id = Column(Integer, ForeignKey('papers.id'))
    user = relationship("User", back_populates="authors")
    paper = relationship("Paper", back_populates="authors")

class Paper(Base):
    __tablename__ = 'papers'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    abstrct = Column(String)
    status = Column(Integer)

    authors = relationship("Author", back_populates="paper")
    reviews = relationship("Review", back_populates="paper")

class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    score = Column(Integer)

    user_id = Column(Integer, ForeignKey('users.id'))
    paper_id = Column(Integer, ForeignKey('papers.id'))
    user = relationship("User", back_populates="reviews")
    paper = relationship("Paper", back_populates="reviews")

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    authors = relationship("Author", back_populates="user")
    reviews = relationship("Review", back_populates="user")
