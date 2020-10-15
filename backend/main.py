import os

from backend.dao.create_engine import create_database
from backend.git_analytics.git_downloader import GitDownloader


# TODO: Figure out better way to do this.
username = os.environ['GIT_USERNAME']
password = os.environ['GIT_PASSWORD']
url = os.environ['GIT_URL']

# Careful, if you already create database, remove the database before doing this.
create_database()

downloader = GitDownloader(username, password, url)
downloader.clone_repo_by_http_url()

print("Hello World")