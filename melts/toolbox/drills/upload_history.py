# Standard libraries
from os import listdir
from typing import List
from datetime import datetime

# Local libraries
from toolbox.drills import generic as drills_generic
from toolbox.utils.function import shield


@shield(on_error_return=False)
def main() -> None:
    '''
    Print all repositories that:
    1. Have their repos on s3
    2. Their repos were last uploaded at least 1 day ago
    '''
    bucket: str = 'continuous-repositories'
    subs_names: List[str] = listdir('groups')
    table_format: str = '{:<25} {:<25}'

    print(table_format.format('GROUP', 'DAYS SINCE LAST UPLOAD'))
    print('---------------------------------------------------')
    for subs in subs_names:
        if drills_generic.s3_path_exists(bucket, f'{subs}/'):
            last_upload_date: datetime = \
                drills_generic.get_last_upload(bucket, f'{subs}/')
            days: int = drills_generic.calculate_days_ago(last_upload_date)
            if days != 0:
                print(table_format.format(subs, days))
        else:
            print(table_format.format(subs, 'NOT UPLOADED'))
