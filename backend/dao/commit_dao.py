from datetime import datetime

from backend.dao.schema.commit import Commit
from backend.dao.create_engine import get_session


class CommitDAO:
    def check_if_commit_exists(self, hexsha: str) -> bool:
        with get_session() as session:
            output = session.query(Commit).filter(Commit.hexsha == hexsha).one_or_none()
        if output is None:
            return False
        return True

    def insert(self, repo_id: int, user_id: int, summary: str, message: str, hexsha: str, is_merge: bool, datetime: datetime) -> Commit:
        with get_session() as session:
            commit = session.add(Commit(
                repo_id=repo_id,
                user_id=user_id,
                summary=summary,
                message=message,
                hexsha=hexsha,
                is_merge=is_merge,
                datetime=datetime,
            ))
            session.commit()

        return commit