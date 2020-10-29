from typing import Optional

from backend.dao.schema.repo import Repo
from backend.dao.create_engine import get_session


class RepoDAO:
    def insert(self, username: str, password: str, url: str, project_name: str) -> Repo:
        with get_session() as session:
            repo = session.add(Repo(username=username, password=password, url=url, project_name=project_name))
            session.commit()

        return repo

    def get_by_project_name(self, project_name: str) -> Optional[Repo]:
        with get_session() as session:
            repo = session.query(Repo).filter(Repo.project_name == project_name).one_or_none()

        return repo
