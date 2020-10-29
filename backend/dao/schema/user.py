from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from backend.dao.schema.base import Base


class User(Base):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    repo_id = Column(Integer, ForeignKey("Repo.id"), nullable=False)
    email = Column(String, nullable=False)
    name = Column(String, nullable=False)

    Repo = relationship("Repo", foreign_keys=[repo_id])
