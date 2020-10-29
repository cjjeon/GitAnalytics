from sqlalchemy import Column, Integer, String

from backend.dao.schema.base import Base


class Repo(Base):
    __tablename__ = 'Repo'

    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    project_name = Column(String, nullable=False)
