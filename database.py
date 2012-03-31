from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import polyspectra.config

# extend the declarative base object
class BaseExt():
    # stolen from http://bit.ly/btqa1C comments
    def __repr__(self):
        return "%s(%s)" % ((self.__class__.__name__), ', '.join(["%s=%r" % \
        (key, getattr(self, key)) for key in sorted(self.__dict__.keys()) \
        if not key.startswith('_')]))
        
engine = create_engine(polyspectra.config.SQLALCHEMY_DATABASE_URI)
db_session = scoped_session(sessionmaker(autocommit=False,
            autoflush=False, bind=engine))
            
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    from polyspectra.models import User
    from polyspectra.models import Category
    from polyspectra.models import Entry
    
    Base.metadata.create_all(bind=engine)