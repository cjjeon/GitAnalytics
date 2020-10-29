from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship

from backend.dao.schema.base import Base


class Commit(Base):
    __tablename__ = 'Commit'

    id = Column(Integer, primary_key=True)
    repo_id = Column(Integer, ForeignKey("Repo.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("User.id"),  nullable=False)
    summary = Column(String, nullable=False)
    message = Column(String, nullable=False)
    hexsha = Column(String, nullable=False)
    is_merge = Column(Boolean, nullable=False, default=False)
    datetime = Column(DateTime, nullable=False)

    Repo = relationship("Repo", foreign_keys=[repo_id])
    User = relationship("User", foreign_keys=[user_id])
