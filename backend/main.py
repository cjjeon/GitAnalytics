import time
import os


from backend.dao.create_engine import create_database
from backend.git_analytics.git_downloader import GitDownloader


# TODO: Figure out better way to do this.
username = os.environ['GIT_USERNAME']
password = os.environ['GIT_PASSWORD']
url = os.environ['GIT_URL']
project_name = os.environ['GIT_PROJECT_NAME']

# Careful, if you already create database, remove the database before doing this.
create_database()

downloader = GitDownloader(username, password, url, project_name)
downloader.clone_repo_by_http_url()
downloader.fetch_latest_commit_info(50)

while 1:
    time.sleep(5)
    print("Hello World")