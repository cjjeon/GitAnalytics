from datetime import datetime
from typing import Optional

from backend.dao.schema.commit import Commit
from backend.dao.create_engine import get_session


class CommitDAO:
    def check_if_commit_exists(self, hexsha: str) -> bool:
        with get_session() as session:
            output = session.query(Commit).filter(Commit.hexsha == hexsha).one_or_none()
        if output is None:
            return False
        return True

    def insert(self, repo_id: int, user_id: int, branch: str, summary: str, message: str, hexsha: str, is_merge: bool, datetime: datetime, insertions: Optional[int], deletions: Optional[int], files: Optional[int]) -> Commit:
        with get_session() as session:
            commit = session.add(Commit(
                repo_id=repo_id,
                user_id=user_id,
                branch=branch,
                summary=summary,
                message=message,
                insertions=insertions,
                deletions=deletions,
                files=files,
                hexsha=hexsha,
                is_merge=is_merge,
                datetime=datetime,
            ))
            session.commit()

        return commit