from enum import Enum
from typing import List, Optional
import datetime
import requests
import logging

from backend.dao.commit_dao import CommitDAO
from backend.dao.repo_dao import RepoDAO
from backend.dao.user_dao import UserDAO
from backend.git_analytics.bitbucket.converter import (
    convert_json_to_repository,
    convert_json_to_commit,
    convert_json_to_diff_stat,
)
from backend.git_analytics.bitbucket.model import Repository, Commit, DiffStat


class Method(Enum):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'


BITBUCKET_API_URL = 'https://api.bitbucket.org/2.0'


class BitBucketDownloader:
    def __init__(self, username: str, password: str, workspace: str):
        self.username = username
        self.password = password
        self.workspace = workspace

        self.repo_dao = RepoDAO()
        self.commit_dao = CommitDAO()
        self.user_dao = UserDAO()

    def _request(self, method: Method, url: str):
        session = requests.Session()

        request = session.request(
            method.value, url, auth=(self.username, self.password)
        )
        request.raise_for_status()
        return request.json()

    def get_repositories(self) -> List[Repository]:
        url = f'{BITBUCKET_API_URL}/repositories/{self.workspace}?pagelen=100'
        json_value = self._request(Method.GET, url)

        repositories = []
        if 'values' in json_value:
            for value in json_value['values']:
                repositories.append(convert_json_to_repository(value))

        return repositories

    def get_commits(self, repository: Repository, page: int = 1, page_length: int = 100, branch: Optional[str] = None) -> List[Commit]:
        if branch is None:
            branch = repository.main_branch

        url = f'{BITBUCKET_API_URL}/repositories/{self.workspace}/{repository.slug}/commits/{branch}?page={page}&pagelen={page_length}'
        json_value = self._request(Method.GET, url)

        commits = []
        if 'values' in json_value:
            for value in json_value['values']:
                if 'hash' in value:
                    hash = value['hash']
                    diff_stat = self.get_stats_for_commit(repository, hash)
                    commits.append(convert_json_to_commit(value, diff_stat))

        return commits

    def get_stats_for_commit(self, repository: Repository, commit_hash: str) -> List[DiffStat]:
        url = f'{BITBUCKET_API_URL}/repositories/{self.workspace}/{repository.slug}/diffstat/{commit_hash}'
        json_value = self._request(Method.GET, url)

        diff_stats = []
        if 'values' in json_value:
            for value in json_value['values']:
                diff_stats.append(convert_json_to_diff_stat(value))

        return diff_stats

    def fetch_and_save_commit_info(self, repository: Repository, page: int = 1, page_length: int = 100) -> None:
        repo = self.repo_dao.get_by_project_name(repository.name)
        if repo is None:
            logging.warning(f"Unable to find the project name {repository.name}. Creating a new one.")
            self.repo_dao.insert(url=repository.link, project_name=repository.name)
            repo = self.repo_dao.get_by_project_name(repository.name)

        commits = self.get_commits(repository, page=page, page_length=page_length, branch=repository.main_branch)
        for commit in commits:
            # Check if this commit exists in database
            if not self.commit_dao.check_if_commit_exists(commit.hash):
                if not self.user_dao.check_if_user_exists(repo.id, commit.user):
                    self.user_dao.insert(repo_id=repo.id, email=commit.user, name=commit.user)

                user = self.user_dao.get_by_email(repo_id=repo.id, email=commit.user)
                if user is None:
                    raise Exception("Unable to find the user from database")

                insertion, deletions, files = commit.total_stats()

                self.commit_dao.insert(
                    repo_id=repo.id,
                    user_id=user.id,
                    branch=repository.main_branch,
                    summary=commit.message,
                    message=commit.message,
                    hexsha=commit.hash,
                    is_merge=True if len(commit.parent_hashes) > 1 else False,
                    datetime=commit.date,
                    insertions=insertion,
                    deletions=deletions,
                    files=files,
                )


