from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# DATABASE = 'sql://root:toor@localhost/lbmib'

DATABASE = 'sqlite:///database.sqlite'

engine = create_engine(DATABASE, convert_unicode=True)
# db_session = scoped_session(sessionmaker(autocommit=False, bind=engine))
Session = sessionmaker(autocommit=False, bind=engine)


Base = declarative_base()
