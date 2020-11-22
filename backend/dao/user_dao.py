from typing import Optional

from backend.dao.schema.user import User
from backend.dao.create_engine import get_session


class UserDAO:
    def check_if_user_exists(self, repo_id: int, email: str) -> bool:
        with get_session() as session:
            output = session.query(User).filter(User.repo_id == repo_id).filter(User.email == email).one_or_none()
        if output is None:
            return False
        return True

    def insert(self, repo_id: int, email: str, name: str):
        with get_session() as session:
            user = session.add(User(repo_id=repo_id, email=email, name=name))
            session.commit()

    def get_by_email(self, repo_id: int, email: str) -> Optional[User]:
        with get_session() as session:
            user = session.query(User).filter(User.repo_id == repo_id).filter(User.email == email).one_or_none()
        return user