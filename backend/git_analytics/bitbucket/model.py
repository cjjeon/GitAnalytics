from dataclasses import dataclass
from typing import List, Tuple
import datetime


@dataclass
class Repository:
    created_on: str
    link: str
    main_branch: str
    name: str
    size: int
    slug: str
    type: str
    updated_on: datetime.datetime
    uuid: str


@dataclass
class DiffStat:
    insertions: int
    deletions: int
    status: str
    new_path: str
    old_path: str


@dataclass
class Commit:
    hash: str
    user: str
    account_id: str
    message: str
    date: datetime.datetime
    type: str
    parent_hashes: List[str]
    diff_stats: List[DiffStat]

    def total_stats(self) -> Tuple[int, int, int]:
        insertions = 0
        deletions = 0

        for diff_stat in self.diff_stats:
            insertions += diff_stat.insertions
            deletions += diff_stat.deletions

        return insertions, deletions, len(self.diff_stats)
