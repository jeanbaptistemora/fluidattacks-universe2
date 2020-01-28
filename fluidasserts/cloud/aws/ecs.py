# -*- coding: utf-8 -*-
"""AWS cloud checks (ECS)."""

# standard imports

# 3rd party imports
from botocore.exceptions import BotoCoreError
from botocore.vendored.requests.exceptions import RequestException
from pyparsing import Literal, Optional

# local imports
from fluidasserts import DAST, MEDIUM
from fluidasserts.helper import aws
from fluidasserts.cloud.aws import _get_result_as_tuple
from fluidasserts.utils.decorators import api, unknown_if


def _get_tasks_running(key_id: str,
                       secret: str,
                       session_token: str = None,
                       retry: bool = True):
    """Get definition_arn of tasks running."""
    arn_task = []
    clusters = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={'aws_session_token': session_token},
        service='ecs',
        func='list_clusters',
        param='clusterArns',
        retry=retry)
    for cluster in clusters:
        tasks_list = aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
            boto3_client_kwargs={'aws_session_token': session_token},
            service='ecs',
            func='list_tasks',
            cluster=cluster,
            param='taskArns',
            retry=retry)
        if tasks_list:
            tasks = aws.run_boto3_func(
                key_id=key_id,
                secret=secret,
                boto3_client_kwargs={'aws_session_token': session_token},
                service='ecs',
                cluster=cluster,
                func='describe_tasks',
                tasks=tasks_list,
                retry=retry)['tasks']
            tasks = list(map(lambda x: x['taskDefinitionArn'], tasks))
            arn_task += tasks

    return arn_task


def _is_root(user):
    """Check if the user is root."""
    root = (Literal('root') | Literal('0'))
    grammar = root + Optional(':' + root)
    return grammar.matches(user)


def _flatten(elements, aux_list=None):
    aux_list = aux_list if aux_list is not None else []
    for i in elements:
        if isinstance(i, list):
            _flatten(i, aux_list)
        else:
            aux_list.append(i)
    return aux_list


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_not_resources_usage_limits(key_id: str,
                                   secret: str,
                                   session_token: str = None,
                                   retry: bool = True) -> tuple:
    """
    Check if ECS containers do not have a defined resource usage limit.

    Limit use of memory, CPU allocation and set resources limits.

    See:
        - `Set ulimits in containers <https://docs.docker.com/engine/reference/
          commandline/run/#set-ulimits-in-container---ulimit>`_
        - https://linux.die.net/man/5/limits.conf

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.

    :returns: - ``OPEN`` if there are users with outdated SSH public keys.
                Encryption enabled.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`

    """
    def _no_limits(container):
        vulnerable = True
        if 'ulimits' in container.keys():
            limits_names = set(map(lambda x: x['name'], container['ulimits']))
            vulnerable = len(limits_names.intersection({'cpu', 'memlock'})) < 2

        return vulnerable

    msg_open: str = 'The use of resources in containers is not limited.'
    msg_closed: str = 'The use of resources in containers is limited.'
    vulns, safes = [], []

    tasks = _get_tasks_running(key_id, secret, session_token, retry)
    for task in tasks:
        task_description = aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
            boto3_client_kwargs={'aws_session_token': session_token},
            service='ecs',
            func='describe_task_definition',
            taskDefinition=task,
            param='taskDefinition',
            retry=retry)
        vulnerable = any(
            list(map(_no_limits, task_description['containerDefinitions'])))
        (vulns if vulnerable else safes).append(
            (task, ('Set a resource usage limit in the defined'
                    ' containers in the task.')))

    return _get_result_as_tuple(
        service='ECS',
        objects='Tasks',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def write_root_file_system(key_id: str,
                           secret: str,
                           session_token: str = None,
                           retry: bool = True) -> tuple:
    """
    Check if there are tasks that allow writing to the root file system.

    Set `readonlyRootFilesystem` property as `true`.

    See `ContainerDefinition <https://docs.aws.amazon.com/AmazonECS/latest/
    APIReference/API_ContainerDefinition.html>`_.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.

    :returns: - ``OPEN`` if there are tasks with `readonlyRootFilesystem`.
                property undefined or `false`.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = 'Tasks allow writing to the root file system.'
    msg_closed: str = 'Tasks do not allow writing to the root file system.'
    vulns, safes = [], []

    tasks = _get_tasks_running(key_id, secret, session_token, retry=retry)
    for task in tasks:
        task_description = aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
            boto3_client_kwargs={'aws_session_token': session_token},
            service='ecs',
            func='describe_task_definition',
            taskDefinition=task,
            param='taskDefinition',
            retry=retry)
        vulnerable = any(map(lambda x: not x['readonlyRootFilesystem'] if
                             'readonlyRootFilesystem' in x.keys() else True,
                             task_description['containerDefinitions']))
        (vulns if vulnerable else safes).append(
            (task, ('Set readonlyRootFilesystem property as true in'
                    ' the containers of the task.')))

    return _get_result_as_tuple(
        service='ECS',
        objects='Tasks',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def no_iam_role_for_tasks(key_id: str,
                          secret: str,
                          session_token: str = None,
                          retry: bool = True) -> tuple:
    """
    Check if there are tasks that do not use IAM roles.

    Using IAM roles per task allows:

    - Simplify usage of AWS SDKs in containers.
    - Credential isolation between tasks / container.
    - Authorisation per task / container.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.

    :returns: - ``OPEN`` if there are tasks that do not use IAM roles.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = 'Tasks do not use IAM roles.'
    msg_closed: str = 'Tasks use IAM roles.'
    vulns, safes = [], []

    tasks = _get_tasks_running(key_id, secret, session_token, retry)
    for task in tasks:
        task_description = aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
            boto3_client_kwargs={'aws_session_token': session_token},
            service='ecs',
            func='describe_task_definition',
            taskDefinition=task,
            param='taskDefinition',
            retry=retry)
        (vulns if 'taskRoleArn' not in task_description.keys() else
         safes).append((task, 'Set an IAM role for the task.'))

    return _get_result_as_tuple(
        service='ECS',
        objects='Tasks',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def run_containers_as_root_user(key_id: str,
                                secret: str,
                                session_token: str = None,
                                retry: bool = True) -> tuple:
    """
    Check if the containers are running as root user.

    Processes In Containers Should Not Run As Root.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.

    :returns: - ``OPEN`` if there are containers that run as root user.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = 'Containers run as root user.'
    msg_closed: str = 'Containers run as non-root user.'
    vulns, safes = [], []

    tasks = _get_tasks_running(key_id, secret, session_token, retry)
    for task in tasks:
        task_description = aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
            boto3_client_kwargs={'aws_session_token': session_token},
            service='ecs',
            func='describe_task_definition',
            taskDefinition=task,
            param='taskDefinition',
            retry=retry)
        vulnerable = any(map(lambda x: True if 'user' not in x.keys() else
                             _is_root(x['user']),
                             task_description['containerDefinitions']))
        (vulns if vulnerable else safes).append(
            (task, 'Run the container as a non-root user.'))

    return _get_result_as_tuple(
        service='ECS',
        objects='Tasks',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def write_volumes(key_id: str,
                  secret: str,
                  session_token: str = None,
                  retry: bool = True) -> tuple:
    """
    Check if there are tasks that allow containers write en in the volumes.

    In the definition of containers set `mountPoints*.readOnly` property
    as `true`.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.

    :returns: - ``OPEN`` if there are tasks with `mount Points*.readOnly`
                property as `false`.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = 'The containers of the tasks allow write in the volumes.'
    msg_closed: str = \
        'The containers of the tasks do not allow write in the volumes.'
    vulns, safes = [], []

    tasks = _get_tasks_running(key_id, secret, session_token, retry)
    for task in tasks:
        task_description = aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
            boto3_client_kwargs={'aws_session_token': session_token},
            service='ecs',
            func='describe_task_definition',
            taskDefinition=task,
            param='taskDefinition',
            retry=retry)
        vulnerable = any(_flatten(list(map(lambda x: list(map(
            lambda y: not y['readOnly'],
            x['mountPoints'])), task_description['containerDefinitions']))))

        (vulns if vulnerable else safes).append(
            (task, ('Set property mountPoints.readOnly as true in the'
                    ' containers of the tasks')))

    return _get_result_as_tuple(
        service='ECS',
        objects='Tasks',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)
