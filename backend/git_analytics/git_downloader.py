import git
import os

from backend.dao.repo_dao import RepoDAO


class CloneProgress(git.RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        if message:
            print(message)


class GitDownloader:
    def __init__(self, username: str, password: str, http_url: str):
        self._username = username
        self._password = password
        self._http_url = http_url

    def authentication(self):
        os.environ['GIT_USERNAME'] = self._username
        os.environ['GIT_PASSWORD'] = self._password

    def get_project_name(self):
        # TODO Extract Project Name from URL
        project_name = self._http_url
        return project_name

    def clone_repo_by_http_url(self):
        # Need to get git_analytics Name?
        self.authentication()

        # Clone the git_analytics
        git.Repo.clone_from(self._http_url, "/random/directory", branch='master', progress=CloneProgress())

        # Add to the database
        RepoDAO().insert(self._username, self._password, self._http_url)

    def extract_data(self):
        return None
