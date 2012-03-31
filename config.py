DEBUG = True
SECRET_KEY = 'OMG-RANDOM-KEY'
DB_USERNAME = 'root'
DB_PASSWORD = 'pass'
DB_HOST = 'localhost'
DB_PORT = '3306'
DB_NAME = 'polyspectra_development'
SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://%s:%s@%s:%s/%s' % \
                            (DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)
