from typing import List
import datetime

from backend.git_analytics.bitbucket.model import Repository, Commit, DiffStat


def convert_json_to_repository(json: any) -> Repository:
    uuid = ''
    if 'uuid' in json:
        uuid = json['uuid']

    link = ''
    if 'links' in json and 'self' in json['links'] and 'href' in json['links']['self']:
        link = json['links']['self']['href']

    name = ''
    if 'name' in json:
        name = json['name']

    created_on = ''
    if 'created_on' in json:
        created_on = datetime.datetime.strptime(json['created_on'].replace('+00:00', ''), "%Y-%m-%dT%H:%M:%S.%f")

    main_branch = ''
    if 'mainbranch' in json and 'name' in json['mainbranch']:
        main_branch = json['mainbranch']['name']

    updated_on = ''
    if 'updated_on' in json:
        updated_on = datetime.datetime.strptime(json['updated_on'].replace('+00:00', ''), "%Y-%m-%dT%H:%M:%S.%f")

    size = 0
    if 'size' in json:
        size = int(json['size'])

    slug = 0
    if 'slug' in json:
        slug = json['slug']

    type = ''
    if 'type' in json:
        type = json['type']

    return Repository(
        created_on=created_on,
        link=link,
        main_branch=main_branch,
        name=name,
        type=type,
        updated_on=updated_on,
        uuid=uuid,
        size=size,
        slug=slug
    )


def convert_json_to_diff_stat(json: any) -> DiffStat:
    status = ''
    if 'status' in json:
        status = json['status']

    lines_removed = 0
    if 'lines_removed' in json:
        lines_removed = json['lines_removed']

    lines_added = 0
    if 'lines_added' in json:
        lines_added = json['lines_added']

    new_path = ''
    if 'new' in json and json['new'] is not None and 'path' in json['new']:
        new_path = json['new']['path']

    old_path = ''
    if 'old' in json and json['old'] is not None and 'path' in json['old']:
        old_path = json['old']['path']

    return DiffStat(
        insertions=lines_added,
        deletions=lines_removed,
        status=status,
        new_path=new_path,
        old_path=old_path
    )


def convert_json_to_commit(json: any, diff_stats: List[DiffStat]) -> Commit:
    hash = ''
    if 'hash' in json:
        hash = json['hash']

    user = ''
    account_id = ''
    if 'author' in json:
        if 'user' in json['author']:
            if 'display_name' in json['author']['user']:
                user = json['author']['user']['display_name']

            if 'account_id' in json['author']['user']:
                account_id = json['author']['user']['account_id']

    message = ''
    if 'message' in json:
        message = json['message']

    date = ''
    if 'date' in json:
        # TODO Need to find a way to get correct Timezone
        date = datetime.datetime.strptime(json['date'].replace('+00:00', ''), "%Y-%m-%dT%H:%M:%S")

    commit_type = ''
    if 'type' in json:
        commit_type = json['type']

    parent_hashes = []
    if 'parents' in json:
        for parent in json['parents']:
            if 'hash' in parent:
                parent_hashes.append(parent['hash'])

    return Commit(
        hash=hash,
        user=user,
        account_id=account_id,
        message=message,
        date=date,
        type=commit_type,
        parent_hashes=parent_hashes,
        diff_stats=diff_stats,
    )