from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey
from database.initialize import Base


class Sponsor(Base):
    __tablename__ = 'sponsors'
    id = Column(Integer, primary_key=True, autoincrement=True)
    sponsor_username = Column(String)


class RegisteredUser(Base):
    __tablename__ = 'registered_users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user = Column(String)
    password = Column(String)
    email = Column(String)
    sponsor_username = Column(String, ForeignKey('sponsors.sponsor_username'))
    sponsor = relationship("Sponsor", backref="registered_users")
