import time
import os

from backend.dao.create_engine import create_database

# TODO: Figure out better way to do this.
username = os.environ['GIT_USERNAME']
password = os.environ['GIT_PASSWORD']
url = os.environ['GIT_URL']
project_name = os.environ['GIT_PROJECT_NAME']

# Careful, if you already create database, remove the database before doing this.
create_database()

"""
    Below is method to get data using Git (Not very prefered)
"""
# from backend.git_analytics.git_downloader import GitDownloader

# downloader = GitDownloader(username, password, url, project_name)
# downloader.clone_repo_by_http_url()
# downloader.fetch_latest_commit_info(300)

from backend.git_analytics.bitbucket.bitbucket_downloader import BitBucketDownloader

downloader = BitBucketDownloader(username, password, project_name)
repositories = downloader.get_repositories()

# Below should be edited to your needs
searching_repos = ['repo_names']
for repository in repositories:
    if repository.name in searching_repos:
        downloader.fetch_and_save_commit_info(repository, page=1, page_length=100)

while 1:
    time.sleep(5)
    print("Hello World")