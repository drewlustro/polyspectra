from polyspectra.database import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship, backref
from datetime import datetime
from polyspectra.database import db_session

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True)
    order = Column(Integer)
    entries = relationship('Entry', backref='category')
    created = Column(DateTime)
    
    @classmethod
    def uncategorized(cls):
        uncat = cls('Uncategorized')
        uncat.id = 0
        return uncat        
    
    def __init__(self, name, order=0):
        self.name = name
        self.order = order
        self.created = datetime.utcnow()
        
    def __repr__(self):
        return '<Category %r>' % (self.name)
        
    def create(self):
        db_session.add(self)
        db_session.commit()
        return True

    def save(self):
        return self.create()

    def delete(self):
        if (len(self.entries)) > 0:
            return False
        db_session.delete(self)
        db_session.commit()


