# -*- coding: utf-8 -*-
"""AWS cloud checks (ECS)."""

# standard imports

# 3rd party imports
from botocore.exceptions import BotoCoreError
from botocore.vendored.requests.exceptions import RequestException

# local imports
from fluidasserts import DAST, MEDIUM
from fluidasserts.helper import aws
from fluidasserts.cloud.aws import _get_result_as_tuple
from fluidasserts.utils.decorators import api, unknown_if


def _get_tasks_running(key_id: str,
                       secret: str,
                       retry: bool = True):
    """Get definition_arn of tasks running."""
    arn_task = []
    clusters = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        service='ecs',
        func='list_clusters',
        param='clusterArns',
        retry=retry)
    for cluster in clusters:
        tasks_list = aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
            service='ecs',
            func='list_tasks',
            cluster=cluster,
            param='taskArns',
            retry=retry)
        if tasks_list:
            tasks = aws.run_boto3_func(
                key_id=key_id,
                secret=secret,
                service='ecs',
                cluster=cluster,
                func='describe_tasks',
                tasks=tasks_list,
                retry=retry)['tasks']
            tasks = list(map(lambda x: x['taskDefinitionArn'], tasks))
            arn_task += tasks

    return arn_task


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_not_resources_usage_limits(key_id: str,
                                   secret: str,
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

    tasks = _get_tasks_running(key_id, secret, retry)
    for task in tasks:
        task_description = aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
            service='ecs',
            func='describe_task_definition',
            taskDefinition=task,
            param='taskDefinition',
            retry=retry)
        vulnerable = any(
            list(
                map(_no_limits,
                    task_description['containerDefinitions'])))
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
def write_root_file_system(key_id: str, secret: str,
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

    tasks = _get_tasks_running(key_id, secret, retry)
    for task in tasks:
        task_description = aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
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
def no_iam_role_for_tasks(key_id: str, secret: str,
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

    tasks = _get_tasks_running(key_id, secret, retry)
    for task in tasks:
        task_description = aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
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
