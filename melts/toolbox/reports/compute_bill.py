# Standard library
import csv
import glob
import json
import os
import sys


def get_common_columns():
    return [
        'authored_at',
        'integration_authored_at',
        'organization',
        'repository',
        'sha1',
        'summary',
    ]


def get_rolling_month_actors_data():
    snapshots_bucket: str = os.environ['local_snapshots_bucket']

    data = {}

    for file_path in glob.glob(f'{snapshots_bucket}/*.csv'):
        with open(file_path) as file:
            for row in csv.DictReader(file):
                group = row['subscription']
                actor = row['author_name'] + ' <' + row['author_email'] + '>'

                data.setdefault(actor, {})
                data[actor].setdefault(group, [])
                data[actor][group].append({
                    key: row.get(key, '')
                    for key in get_common_columns()
                })

    print(json.dumps(data, indent=2), file=sys.stderr)

    return data


def create_bills():
    data = get_rolling_month_actors_data()
    aggregates_bucket: str = os.environ['local_aggregates_bucket']

    for group in map(os.path.basename, glob.glob('groups/*')):
        group_bill_path: str = os.path.join(aggregates_bucket, f'{group}.csv')

        with open(group_bill_path, 'w') as file:
            writer = csv.DictWriter(
                file,
                fieldnames=[
                    'actor',
                    'groups',
                    '# groups',
                ] + get_common_columns(),
                quoting=csv.QUOTE_NONNUMERIC,
            )
            writer.writeheader()

            for actor, actor_groups in data.items():
                if group in actor_groups:
                    groups_contributed = [
                        group_contributed
                        for group_contributed in actor_groups
                        if actor_groups[group][-1]['organization']
                        == actor_groups[group_contributed][-1]['organization']
                    ]
                    writer.writerow({
                        'actor': actor,
                        'groups': ', '.join(groups_contributed),
                        '# groups': len(groups_contributed),
                        **{
                            key: actor_groups[group][-1][key]
                            for key in get_common_columns()
                        },
                    })
        return True
