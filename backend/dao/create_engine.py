from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from backend.dao.schema.base import Base

engine = create_engine('sqlite:////usr/local/bin/db/git_analytics.db')


def create_database():
    Base.metadata.create_all(engine)


def get_session():
    session_maker = sessionmaker(engine)
    session: Session = session_maker()
    yield session
    session.close()