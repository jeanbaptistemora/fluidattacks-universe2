# pylint: disable=too-many-lines

from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import rollbar

from backend import util
from backend.utils import forms

from backend.dal.helpers import dynamodb

DYNAMODB_RESOURCE = dynamodb.DYNAMODB_RESOURCE


def attribute_exists(table_name, primary_key, data):
    return get_table_attributes_dynamo(
        table_name, primary_key, data)


def get_comments_dynamo(finding_id, comment_type):
    """ Get comments of a finding. """
    table = DYNAMODB_RESOURCE.Table('FI_comments')
    filter_key = 'finding_id'
    comment_types = comment_type.split(',')
    filter_exp_lst = ['comment_type=:' + val for val in comment_types]
    filtering_exp = filter_key + '=:' + filter_key + ' AND ('
    filter_attr_dict = {':' + val: val for val in comment_types}
    filter_attr_dict[':' + filter_key] = finding_id
    filtering_exp += ' OR '.join(filter_exp_lst) + ')'
    response = table.scan(
        FilterExpression=filtering_exp,
        ExpressionAttributeValues=filter_attr_dict)
    items = response['Items']
    while True:
        if response.get('LastEvaluatedKey'):
            response = table.scan(
                FilterExpression=filtering_exp,
                ExpressionAttributeValues=filter_attr_dict,
                ExclusiveStartKey=response['LastEvaluatedKey'])
            items += response['Items']
        else:
            break
    return items


def add_finding_comment_dynamo(finding_id, email, comment_data):
    """ Add a comment in a finding. """
    table = DYNAMODB_RESOURCE.Table('FI_comments')
    try:
        payload = {
            'finding_id': finding_id,
            'email': email
        }
        payload.update(comment_data)
        response = table.put_item(
            Item=payload
        )
        resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
        return resp
    except ClientError:
        rollbar.report_exc_info()
        return False


def get_project_comments_dynamo(project_name):
    """ Get comments of a project. """
    table = DYNAMODB_RESOURCE.Table('fi_project_comments')
    filter_key = 'project_name'
    filtering_exp = Key(filter_key).eq(project_name)
    response = table.scan(FilterExpression=filtering_exp)
    items = response['Items']
    while True:
        if response.get('LastEvaluatedKey'):
            response = table.scan(
                FilterExpression=filtering_exp,
                ExclusiveStartKey=response['LastEvaluatedKey'])
            items += response['Items']
        else:
            break
    return items


def delete_comment_dynamo(finding_id, user_id):
    """ Delete a comment in a finding. """
    table = DYNAMODB_RESOURCE.Table('FI_comments')
    try:
        response = table.delete_item(
            Key={
                'finding_id': finding_id,
                'user_id': user_id
            }
        )
        resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
        return resp
    except ClientError:
        rollbar.report_exc_info()
        return False


def get_project_dynamo(project):
    """Get a project info."""
    filter_value = project.lower()
    table = DYNAMODB_RESOURCE.Table('FI_projects')
    filter_key = 'project_name'
    filtering_exp = Key(filter_key).eq(filter_value)
    response = table.query(KeyConditionExpression=filtering_exp)
    items = response['Items']
    while True:
        if response.get('LastEvaluatedKey'):
            response = table.query(
                KeyConditionExpression=filtering_exp,
                ExclusiveStartKey=response['LastEvaluatedKey'])
            items += response['Items']
        else:
            break
    return items


def add_user_to_project_dynamo(project_name, user_email, role):
    """Adding user role in a project."""
    table = DYNAMODB_RESOURCE.Table('FI_projects')
    item = get_project_dynamo(project_name)
    if item == []:
        try:
            response = table.put_item(
                Item={
                    'project_name': project_name.lower(),
                    role: set([user_email])
                }
            )
            resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
            return resp
        except ClientError:
            rollbar.report_exc_info()
            return False
    else:
        try:
            response = table.update_item(
                Key={
                    'project_name': project_name.lower(),
                },
                UpdateExpression='ADD #rol :val1',
                ExpressionAttributeNames={
                    '#rol': role
                },
                ExpressionAttributeValues={
                    ':val1': set([user_email])
                }
            )
            resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
            return resp
        except ClientError:
            rollbar.report_exc_info()
            return False


def remove_role_to_project_dynamo(project_name, user_email, role):
    """Remove user role in a project."""
    table = DYNAMODB_RESOURCE.Table('FI_projects')
    try:
        response = table.update_item(
            Key={
                'project_name': project_name.lower(),
            },
            UpdateExpression='DELETE #rol :val1',
            ExpressionAttributeNames={
                '#rol': role
            },
            ExpressionAttributeValues={
                ':val1': set([user_email])
            }
        )
        resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
        return resp
    except ClientError:
        rollbar.report_exc_info()
        return False


def weekly_report_dynamo(
        init_date, finish_date, registered_users, logged_users, companies):
    """ Save the number of registered and logged users weekly. """
    table = DYNAMODB_RESOURCE.Table('FI_weekly_report')
    try:
        response = table.put_item(
            Item={
                'init_date': init_date,
                'finish_date': finish_date,
                'registered_users': registered_users,
                'logged_users': logged_users,
                'companies': companies,
            }
        )
        resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
        return resp
    except ClientError:
        rollbar.report_exc_info()
        return False


def get_project_access_dynamo(user_email, project_name):
    """Get user access of a project."""
    user_email = user_email.lower()
    project_name = project_name.lower()
    table = DYNAMODB_RESOURCE.Table('FI_project_access')
    filter_key = 'user_email'
    filter_sort = 'project_name'
    filtering_exp = Key(filter_key).eq(user_email) & \
        Key(filter_sort).eq(project_name)
    response = table.query(KeyConditionExpression=filtering_exp)
    items = response['Items']
    while True:
        if response.get('LastEvaluatedKey'):
            response = table.query(
                KeyConditionExpression=filtering_exp,
                ExclusiveStartKey=response['LastEvaluatedKey'])
            items += response['Items']
        else:
            break
    return items


def add_project_access_dynamo(
        user_email, project_name, project_attr, attr_value):
    """Add project access attribute."""
    table = DYNAMODB_RESOURCE.Table('FI_project_access')
    item = get_project_access_dynamo(user_email, project_name)
    if item == []:
        try:
            response = table.put_item(
                Item={
                    'user_email': user_email.lower(),
                    'project_name': project_name.lower(),
                    project_attr: attr_value
                }
            )
            resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
            return resp
        except ClientError:
            rollbar.report_exc_info()
            return False
    else:
        return update_project_access_dynamo(
            user_email,
            project_name,
            project_attr,
            attr_value
        )


def remove_project_access_dynamo(user_email, project_name):
    """Remove project access in dynamo."""
    table = DYNAMODB_RESOURCE.Table('FI_project_access')
    try:
        response = table.delete_item(
            Key={
                'user_email': user_email.lower(),
                'project_name': project_name.lower(),
            }
        )
        resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
        return resp
    except ClientError:
        rollbar.report_exc_info()
        return False


def update_project_access_dynamo(
        user_email, project_name, project_attr, attr_value):
    """Update project access attribute."""
    table = DYNAMODB_RESOURCE.Table('FI_project_access')
    try:
        response = table.update_item(
            Key={
                'user_email': user_email.lower(),
                'project_name': project_name.lower(),
            },
            UpdateExpression='SET #project_attr = :val1',
            ExpressionAttributeNames={
                '#project_attr': project_attr
            },
            ExpressionAttributeValues={
                ':val1': attr_value
            }
        )
        resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
        return resp
    except ClientError:
        rollbar.report_exc_info()
        return False


def get_data_dynamo(table_name, primary_name_key, primary_key):
    """Get atributes data."""
    table = DYNAMODB_RESOURCE.Table(table_name)
    primary_key = primary_key.lower()
    filter_key = primary_name_key
    filtering_exp = Key(filter_key).eq(primary_key)
    response = table.query(KeyConditionExpression=filtering_exp)
    items = response['Items']
    while True:
        if response.get('LastEvaluatedKey'):
            response = table.query(
                KeyConditionExpression=filtering_exp,
                ExclusiveStartKey=response['LastEvaluatedKey'])
            items += response['Items']
        else:
            break
    return items


def get_data_dynamo_filter(table_name, filter_exp='', data_attr=''):
    """Get atributes data."""
    table = DYNAMODB_RESOURCE.Table(table_name)
    scan_attrs = {}
    if data_attr:
        scan_attrs['ProjectionExpression'] = data_attr
    else:
        # ProjectionExpression not especified
        pass
    if filter_exp:
        scan_attrs['FilterExpression'] = filter_exp

    response = table.scan(**scan_attrs)
    items = response['Items']
    while response.get('LastEvaluatedKey'):
        scan_attrs['ExclusiveStartKey'] = response['LastEvaluatedKey']
        response = table.scan(**scan_attrs)
        items += response['Items']

    return items


def add_list_resource_dynamo(table_name, primary_name_key, primary_key, data, attr_name):
    """Adding list attribute in a table."""
    table = DYNAMODB_RESOURCE.Table(table_name)
    item = get_data_dynamo(table_name, primary_name_key, primary_key)
    primary_key = primary_key.lower()
    try:
        if not item:
            response = table.put_item(
                Item={
                    primary_name_key: primary_key,
                    attr_name: data,
                }
            )
            resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
        else:
            if attr_name not in item[0]:
                table.update_item(
                    Key={
                        primary_name_key: primary_key,
                    },
                    UpdateExpression='SET #attrName = :val1',
                    ExpressionAttributeNames={
                        '#attrName': attr_name
                    },
                    ExpressionAttributeValues={
                        ':val1': []
                    }
                )
            update_response = table.update_item(
                Key={
                    primary_name_key: primary_key,
                },
                UpdateExpression='SET #attrName = list_append(#attrName, :val1)',
                ExpressionAttributeNames={
                    '#attrName': attr_name
                },
                ExpressionAttributeValues={
                    ':val1': data
                }
            )
            resp = update_response['ResponseMetadata']['HTTPStatusCode'] == 200
    except ClientError:
        rollbar.report_exc_info()
        resp = False
    return resp


def remove_list_resource_dynamo(
        table_name, primary_name_key, primary_key, attr_name, index):
    """Remove list attribute in a table."""
    table = DYNAMODB_RESOURCE.Table(table_name)
    try:
        response = table.update_item(
            Key={
                primary_name_key: primary_key.lower(),
            },
            UpdateExpression='REMOVE #attrName[' + str(index) + ']',
            ExpressionAttributeNames={
                '#attrName': attr_name
            }
        )
        resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
        return resp
    except ClientError:
        rollbar.report_exc_info()
        return False


def add_attribute_dynamo(table_name, primary_keys, attr_name, attr_value):
    """Adding an attribute to a dynamo table."""
    table = DYNAMODB_RESOURCE.Table(table_name)
    item = get_data_dynamo(table_name, primary_keys[0], primary_keys[1])
    if not item:
        try:
            response = table.put_item(
                Item={
                    primary_keys[0]: primary_keys[1],
                    attr_name: attr_value
                }
            )
            resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
            return resp
        except ClientError:
            rollbar.report_exc_info()
            return False
    else:
        return update_attribute_dynamo(
            table_name,
            primary_keys,
            attr_name,
            attr_value)


def update_attribute_dynamo(table_name, primary_keys, attr_name, attr_value):
    """Updating an attribute to a dynamo table."""
    table = DYNAMODB_RESOURCE.Table(table_name)
    try:
        response = table.update_item(
            Key={
                primary_keys[0]: primary_keys[1],
            },
            UpdateExpression='SET #attrName = :val1',
            ExpressionAttributeNames={
                '#attrName': attr_name
            },
            ExpressionAttributeValues={
                ':val1': attr_value
            }
        )
        resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
        return resp
    except ClientError:
        rollbar.report_exc_info()
        return False


def update_in_multikey_table_dynamo(table_name, multiple_keys, attr_name, attr_value):
    table = DYNAMODB_RESOURCE.Table(table_name)
    try:
        update_response = table.update_item(
            Key=multiple_keys,
            UpdateExpression='SET #attrName = :val1',
            ExpressionAttributeNames={
                '#attrName': attr_name
            },
            ExpressionAttributeValues={
                ':val1': attr_value
            }
        )
        resp = update_response['ResponseMetadata']['HTTPStatusCode'] == 200
        return resp
    except ClientError:
        rollbar.report_exc_info()
        return False


def get_vulnerabilities_dynamo(finding_id):
    """Get vulnerabilities of a finding."""
    table = DYNAMODB_RESOURCE.Table('FI_vulnerabilities')
    filtering_exp = Key('finding_id').eq(finding_id)
    response = table.query(KeyConditionExpression=filtering_exp)
    items = response['Items']
    while response.get('LastEvaluatedKey'):
        response = table.query(
            KeyConditionExpression=filtering_exp,
            ExclusiveStartKey=response['LastEvaluatedKey'])
        items += response['Items']
    return items


def get_finding_project(finding_id):
    """ Get project associated to a finding. """
    table = DYNAMODB_RESOURCE.Table('FI_findings')
    response = table.get_item(
        Key={
            'finding_id': finding_id
        },
        AttributesToGet=['project_name']
    )
    item = response.get('Item').get('project_name') if 'Item' in response else None

    return item


def add_multiple_attributes_dynamo(table_name, primary_keys, dic_data):
    """Adding multiple attributes to a dynamo table."""
    table = DYNAMODB_RESOURCE.Table(table_name)
    item = get_data_dynamo(table_name, primary_keys[0], primary_keys[1])
    keys_dic = {str(primary_keys[0]): primary_keys[1]}
    if item:
        resp = update_mult_attrs_dynamo(table_name, keys_dic, dic_data)
    else:
        try:
            dic_data_field = {k: dic_data[k] for k in list(dic_data.keys())}
            attr_to_add = forms.dict_concatenation(keys_dic, dic_data_field)
            response = table.put_item(
                Item=attr_to_add
            )
            resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
        except ClientError:
            rollbar.report_exc_info()
            resp = False
    return resp


def update_mult_attrs_dynamo(table_name, primary_keys, dic_data):
    """Updating multiple data to a dynamo table."""
    table = DYNAMODB_RESOURCE.Table(table_name)
    try:
        str_format = '{metric} = :{metric}'
        empty_values = {k: v for k, v in list(dic_data.items()) if v == ""}
        for item in empty_values:
            remove_attr_dynamo(table_name, primary_keys, item)
            del dic_data[item]

        dic_data_params = [str_format.format(metric=x) for x in list(dic_data.keys())]
        query_params = 'SET ' + ', '.join(dic_data_params)
        expression_params = {':' + k: dic_data[k] for k in list(dic_data.keys())}
        response = table.update_item(
            Key=primary_keys,
            UpdateExpression=query_params,
            ExpressionAttributeValues=expression_params
        )
        resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
    except ClientError:
        rollbar.report_exc_info()
        resp = False
    return resp


def get_table_attributes_dynamo(table_name, primary_key, data_attributes):
    """ Get a group of attributes of a table. """
    table = DYNAMODB_RESOURCE.Table(table_name)
    try:
        response = table.get_item(
            Key=primary_key,
            AttributesToGet=data_attributes
        )
        items = response.get('Item')
    except ClientError:
        rollbar.report_exc_info()
        items = {}
    return items if items else {}


def get_finding_attributes_dynamo(finding_id, data_attributes):
    """ Get a group of attributes of a finding. """

    return get_table_attributes_dynamo(
        'FI_findings', {'finding_id': finding_id}, data_attributes)


def get_project_attributes_dynamo(project_name, data_attributes):
    """ Get a group of attributes of a project. """

    return get_table_attributes_dynamo(
        'FI_projects', {'project_name': project_name}, data_attributes)


def update_item_list_dynamo(
        primary_keys, attr_name, index, field, field_value):
    """update list attribute in a table."""
    table = DYNAMODB_RESOURCE.Table('FI_findings')
    try:
        response = table.update_item(
            Key={
                primary_keys[0]: primary_keys[1].lower(),
            },
            UpdateExpression='SET #attrName[' + str(index) + '].#field = :field_val',
            ExpressionAttributeNames={
                '#attrName': attr_name,
                '#field': field,
            },
            ExpressionAttributeValues={
                ':field_val': field_value
            }
        )
        resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
        return resp
    except ClientError:
        rollbar.report_exc_info()
        return False


def get_findings_data_dynamo(filtering_exp, data_attr=''):
    """Get all the findings of a project."""
    table = DYNAMODB_RESOURCE.Table('FI_findings')
    if data_attr:
        response = table.scan(
            FilterExpression=filtering_exp,
            ProjectionExpression=data_attr)
        items = response['Items']
        while True:
            if response.get('LastEvaluatedKey'):
                response = table.scan(
                    FilterExpression=filtering_exp,
                    ProjectionExpression=data_attr,
                    ExclusiveStartKey=response['LastEvaluatedKey'])
                items += response['Items']
            else:
                break
    else:
        response = table.scan(
            FilterExpression=filtering_exp)
        items = response['Items']
        while response.get('LastEvaluatedKey'):
            response = table.scan(
                FilterExpression=filtering_exp,
                ExclusiveStartKey=response['LastEvaluatedKey'])
            items += response['Items']
    return items


def get_findings_dynamo(project, data_attr=''):
    """Get all the findings of a project."""
    project_name = project.lower()
    filter_key = 'project_name'
    filtering_exp = Attr(filter_key).eq(project_name)
    findings = get_findings_data_dynamo(filtering_exp, data_attr)
    return findings


def get_projects_data_dynamo(filtering_exp='', data_attr=''):
    """Get project from Dynamodb"""
    table = DYNAMODB_RESOURCE.Table('FI_projects')
    scan_attrs = {}
    if filtering_exp:
        scan_attrs['FilterExpression'] = filtering_exp
    else:
        # FilterExpression not especified
        pass

    if data_attr:
        scan_attrs['ProjectionExpression'] = data_attr
    else:
        # ProjectionExpression not especified
        pass

    response = table.scan(**scan_attrs)
    items = response['Items']
    while response.get('LastEvaluatedKey'):
        scan_attrs['ExclusiveStartKey'] = response['LastEvaluatedKey']
        response = table.scan(**scan_attrs)
        items += response['Items']

    return items


def get_findings_released_dynamo(project, data_attr=''):
    """Get all the findings that has been released."""
    filter_key = 'project_name'
    project_name = project.lower()
    filtering_exp = Attr(filter_key).eq(project_name) & Attr('releaseDate').exists()
    if data_attr and 'releaseDate' not in data_attr:
        data_attr += ', releaseDate'
    else:
        # By default it return all the attributes
        pass
    findings = get_findings_data_dynamo(filtering_exp, data_attr)
    findings_released = [i for i in findings if util.validate_release_date(i)]
    return findings_released


def delete_item(table_name, primary_keys):
    """ Remove item """

    table = DYNAMODB_RESOURCE.Table(table_name)
    try:
        item = table.get_item(Key=primary_keys)
        resp = False
        if item.get('Item'):
            response = table.delete_item(Key=primary_keys)
            resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
        else:
            # item not found
            pass
        return resp
    except ClientError:
        return False


def remove_attr_dynamo(table_name, primary_keys, attr_name):
    """ Remove given attribute """

    table = DYNAMODB_RESOURCE.Table(table_name)
    try:
        response = table.update_item(
            Key=primary_keys,
            UpdateExpression='REMOVE #attrName',
            ExpressionAttributeNames={
                '#attrName': attr_name
            }
        )
        resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
        return resp
    except ClientError:
        rollbar.report_exc_info()
        return False


def remove_set_element_dynamo(table_name, primary_keys, set_name, set_element):
    """Remove a element from a set."""
    table = DYNAMODB_RESOURCE.Table(table_name)
    try:
        response = table.update_item(
            Key={
                primary_keys[0]: primary_keys[1].lower(),
            },
            UpdateExpression='DELETE #name :val1',
            ExpressionAttributeNames={
                '#name': set_name
            },
            ExpressionAttributeValues={
                ':val1': set([set_element])
            }
        )
        resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
    except ClientError:
        rollbar.report_exc_info()
        resp = False
    return resp


def add_set_element_dynamo(table_name, primary_keys, set_name, set_values):
    """Adding elements to a set."""
    table = DYNAMODB_RESOURCE.Table(table_name)
    item = get_data_dynamo(table_name, primary_keys[0], primary_keys[1])
    if item:
        resp = update_set_element_dynamo(
            table_name, primary_keys, set_name, set_values)
    else:
        try:
            response = table.put_item(
                Item={
                    primary_keys[0]: primary_keys[1].lower(),
                    set_name: set(set_values)
                }
            )
            resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
        except ClientError:
            rollbar.report_exc_info()
            resp = False
    return resp


def update_set_element_dynamo(table_name, primary_keys, set_name, set_values):
    """Updating elements in a set."""
    table = DYNAMODB_RESOURCE.Table(table_name)
    try:
        response = table.update_item(
            Key={
                primary_keys[0]: primary_keys[1].lower(),
            },
            UpdateExpression='ADD #name :val1',
            ExpressionAttributeNames={
                '#name': set_name
            },
            ExpressionAttributeValues={
                ':val1': set(set_values)
            }
        )
        resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
    except ClientError:
        rollbar.report_exc_info()
        resp = False
    return resp
