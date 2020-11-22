import datetime
import pytest

from backend.git_analytics.bitbucket.converter import convert_json_to_repository, convert_json_to_commit, \
    convert_json_to_diff_stat
from backend.git_analytics.bitbucket.model import Repository, DiffStat


def test_convert_json_to_repository():
    json = {
        "scm": "git",
        "website": "",
        "has_wiki": False,
        "uuid": "{1234-567-8910}",
        "links": {
            "self": {
                "href": "https://api.bitbucket.org/2.0/repositories/OWNER/project_name"
            },
        },
        "full_name": "OWNER/project_name",
        "name": "project_name",
        "created_on": "2017-01-05T00:40:53.214665+00:00",
        "mainbranch": {
            "type": "branch",
            "name": "master"
        },
        "updated_on": "2017-09-23T09:53:02.713898+00:00",
        "size": 18855171,
        "type": "repository",
        "slug": "project_name",
        "is_private": True,
        "description": ""
    }
    output = convert_json_to_repository(json)

    assert output.created_on == datetime.datetime(2017, 1, 5, 0, 40, 53, 214665)
    assert output.link == "https://api.bitbucket.org/2.0/repositories/OWNER/project_name"
    assert output.main_branch == "master"
    assert output.name == "project_name"
    assert output.type == "repository"
    assert output.updated_on == datetime.datetime(2017, 9, 23, 9, 53, 2, 713898)
    assert output.uuid == "{1234-567-8910}"
    assert output.size == 18855171
    assert output.slug == "project_name"


def test_convert_json_to_diff_stat():
    json = {
        "status": "modified",
        "lines_removed": 1,
        "lines_added": 4,
        "type": "diffstat",
        "old": {
            "path": "old_path"
        },
        "new": {
            "path": "new_path"
        }
    }

    output = convert_json_to_diff_stat(json)

    assert output.insertions == 4
    assert output.deletions == 1
    assert output.status == 'modified'
    assert output.old_path == 'old_path'
    assert output.new_path == 'new_path'


def test_convert_json_to_commit():
    json = {
        "hash": "abcdef",
        "author": {
            "user": {
                "display_name": "Jenni Hantula",
                "account_id": "123123123"
            }
        },
        "parents": [
            {
                "hash": "aaaaaaaaaaaaaaaa",
            },
            {
                "hash": "bbbbbbbbbbbb",
            }
        ],
        "date": "2020-11-20T07:09:53+00:00",
        "message": "Message",
        "type": "commit"
    }

    diff_stats = [DiffStat(
        insertions=1,
        deletions=2,
        status='status',
        old_path='old_path',
        new_path='new_path'
    )]

    output = convert_json_to_commit(json, diff_stats)

    assert output.hash == 'abcdef'
    assert output.user == 'Jenni Hantula'
    assert output.account_id == '123123123'
    assert output.message == 'Message'
    assert output.date == datetime.datetime(2020, 11, 20, 7, 9, 53)
    assert output.type == 'commit'
    assert output.parent_hashes == ['aaaaaaaaaaaaaaaa', 'bbbbbbbbbbbb']
    assert output.diff_stats == diff_stats