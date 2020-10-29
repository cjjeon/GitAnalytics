import git
import os

from backend.dao.commit_dao import CommitDAO
from backend.dao.repo_dao import RepoDAO
from backend.dao.user_dao import UserDAO


class CloneProgress(git.RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        if message:
            print(message)

LOCAL_GIT_DIRECTORY = '/random/directory/'

class GitDownloader:
    def __init__(self, username: str, password: str, http_url: str, project_name: str):
        self._username = username
        self._password = password
        self._http_url = http_url
        self._project_name = project_name

        self.repo_dao = RepoDAO()
        self.commit_dao = CommitDAO()
        self.user_dao = UserDAO()

    def authentication(self):
        os.environ['GIT_USERNAME'] = self._username
        os.environ['GIT_PASSWORD'] = self._password

    def _create_http_url_with_username_and_password(self) -> str:
        # Checking certain requirement for the url
        if 'https://' not in self._http_url:
            raise Exception("Git Link needs to be HTTPS")

        if '@' not in self._http_url:
            return f'https://{self._username}:{self._password}' + self._http_url[7:]

        url = self._http_url.split('@')
        if len(url) > 2:
            raise Exception("Unable to read the URL for this")

        return f'https://{self._username}:{self._password}@' + url[1]

    def get_local_git_path(self):
        return os.path.join(LOCAL_GIT_DIRECTORY, self._project_name)

    def clone_repo_by_http_url(self):
        # Clone the git_analytics
        git.Repo.clone_from(
            self._create_http_url_with_username_and_password(),
            self.get_local_git_path(),
            branch='master',
            progress=CloneProgress()
        )

        # Add to the database
        self.repo_dao.insert(self._username, self._password, self._http_url, self._project_name)

    def fetch_latest_commit_info(self, max_count: int = 50):
        git_repo = git.Repo(self.get_local_git_path())
        commits = list(git_repo.iter_commits('master', max_count=max_count))

        repo = self.repo_dao.get_by_project_name(self._project_name)
        if repo is None:
            raise Exception("Please clone the project first")

        for commit in commits:
            # Check if this commit exists in database
            if not self.commit_dao.check_if_commit_exists(commit.hexsha):
                author = commit.author

                if not self.user_dao.check_if_user_exists(author.email):
                    self.user_dao.insert(repo_id=repo.id, email=author.email, name=author.name)

                user = self.user_dao.get_by_email(repo_id=repo.id, email=author.email)
                if user is None:
                    raise Exception("Unable to find the user from database")

                self.commit_dao.insert(
                    repo_id=repo.id,
                    user_id=user.id,
                    summary=commit.summary,
                    message=commit.message,
                    hexsha=commit.hexsha,
                    is_merge=True if len(commit.parents) > 1 else False,
                    datetime=commit.committed_datetime,
                )

