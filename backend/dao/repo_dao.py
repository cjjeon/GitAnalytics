from backend.dao.schema.repo import Repo
from backend.dao.create_engine import get_session


class RepoDAO:
    def insert(self, username: str, password: str, url: str):
        with get_session() as session:
            session.add(Repo(username=username, password=password, url=url))
            session.flush()
