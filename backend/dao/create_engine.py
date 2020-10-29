from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from backend.dao.schema.base import Base

engine = create_engine('sqlite:////usr/local/bin/db/git_analytics.db')


def create_database():
    Base.metadata.create_all(engine)


@contextmanager
def get_session():
    session_maker = sessionmaker(engine)
    session: Session = session_maker()
    try:
        yield session
    finally:
        session.close()