from backend.dal import integrates_dal


TABLE = 'fi_project_names'


def exists(project_name):
    primary_key = {'project_name': project_name.lower()}
    return integrates_dal.attribute_exists(
        TABLE, primary_key, ['project_name'])


def remove_project_name(project_name):
    primary_keys = {'project_name': project_name.lower()}
    return integrates_dal.delete_item(TABLE, primary_keys)


def get_all_project_names():
    names = [project['project_name']
             for project in integrates_dal.get_data_dynamo_filter(TABLE)]
    return names
