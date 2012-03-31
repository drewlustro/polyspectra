from polyspectra.database import Base
from sqlalchemy import Column, Integer, Boolean, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship, backref
from datetime import datetime
from polyspectra.database import db_session
import re


class EntryType:
    BLOG = 'blog'
    IMAGE = 'image'
    MUSIC = 'music'
    QUOTE = 'quote'
    LINK = 'link'
    
    @classmethod
    def all(cls):
        return [cls.BLOG, cls.IMAGE, cls.MUSIC, cls.QUOTE, cls.LINK]
    
    
class Entry(Base):
    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    entry_type = Column(String(255)) # used as Entry.entry_
    title = Column(String(255))
    slug = Column(String(60), unique=True)
    published = Column(Boolean)    
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', backref=backref('entries', lazy='dynamic'))
    category_id = Column(Integer, ForeignKey('categories.id'))
    # category = relationship('Category', backref=backref('entries', lazy='dynamic'))
    type_meta = Column(Text)
    text = Column(Text)
    heart_count = Column(Integer)
    comment_count = Column(Integer)
    
    def __init__(self, user_id, **kwargs):
        self.user_id = user_id
        self.title = kwargs.get('title', '')
        self.text = kwargs.get('text', '')
        self.date = kwargs.get('date', datetime.utcnow())
        self.category_id = kwargs.get('category_id', 0)
        self.entry_type = kwargs.get('entry_type', EntryType.BLOG)    
        self.type_meta = kwargs.get('type_meta','')
        self.heart_count = kwargs.get('heart_count', 0)
        self.comment_count = kwargs.get('comment_count', 0)
        
        self.published = False
        
    def __repr__(self):
            return "%s(%s)" % ((self.__class__.__name__), ', '.join(["%s=%r" % \
            (key, getattr(self, key)) for key in sorted(self.__dict__.keys()) \
            if not key.startswith('_')]))
    
    def generate_slug(self):
        title = self.title.lower()
        convert_spaces = re.sub(r'\s+', '-', title)
        alphanumericspace = re.sub(r'-\W+', '', convert_spaces)
        newslug = alphanumericspace[0:50].strip()
                
        # auto-generate slightly differnt slug when collision is found
        collision_exists = True
        cnt = 2
        testslug = newslug
        while collision_exists:
            collision = Entry.query.filter(Entry.slug == testslug 
                        and Entry.id != self.id).first()
            if collision:
                testslug = newslug + '-' + str(cnt)
                cnt += 1
            else:
                collision_exists = False
                newslug = testslug
            
        return newslug
        
    # todo - convert to getter/setter
    def publish(self):
        self.published = True
        if not self.slug:
            self.slug = self.generate_slug()
        

    def create(self):
        # TODO: move this out of here and find out how to do custom
        # getters and setters with SQLAlchemy
        if not self.entry_type in EntryType.all():
            raise Exception('Invalid EntryType')
            return False
        db_session.add(self)
        db_session.commit()
        return True
        
    def save(self):
        return self.create()
        
    def delete(self):
        db_session.delete(self)
        db_session.commit()
    
    
    