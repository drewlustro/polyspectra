from polyspectra.database import Base
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True)
    email = Column(String(120), unique=True)
    password = Column(String(255))
    name = Column(String(80))
    #entries = db.relationship('Entry')
    
    def __init__(self, username, email, password, name):
        self.username = username
        self.email = email
        self.password = password
        self.name = name
        
    def __repr__(self):
        return '<User %r (%r)>' % (self.username, self.email)


