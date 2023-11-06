from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    fullname = Column(String(200))
    username = Column(String(200), unique=True)
    password = Column(String(200))
    email = Column(String(200))
    mobile = Column(String(200))
    agree = Column(Integer)
    login_token = Column(String(200), default=None)
    login_token_date = Column(DateTime, default=None)
    created = Column(DateTime, server_default=func.now())
    role = Column(String(200), default="users") # users, admin

    employees = relationship('Employees', back_populates='user')

class Employees(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    emp_code = Column(String(200), unique=True)
    name = Column(String(200), default=None)
    designation = Column(String(200), default=None)
    profile = Column(String(200), default=None)
    created = Column(DateTime, server_default=func.now()) # set by default time

    user = relationship('User', back_populates='employees')


class Logs(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True)
    action = Column(Text, default=None)
    ip_address = Column(String(200))
    req_header = Column(Text, default=None)
    browser = Column(String(200)) #chrome, firefox, safari, opera
    platform = Column(String(200)) #ios, android, windows, macos
    mobile = Column(String(200))
    referer = Column(String(200)) #Referer
    city = Column(String(200))
    country = Column(String(200))
    region = Column(String(200)) 
    latitude = Column(String(200)) 
    longitude = Column(String(200)) 
    timezone = Column(String(200)) 
    log_date = Column(DateTime, server_default=func.now()) # set by default time
    called_api = Column(String(200)) 
    user_id = Column(String(200))
    emp_id = Column(String(200))
    req_data = Column(Text, default=None)
    

