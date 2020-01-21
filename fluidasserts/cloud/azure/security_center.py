# -*- coding: utf-8 -*-

"""Fluid Asserts Security Center package."""

# standar imports
from typing import Tuple
from itertools import repeat

# 3rd party imports
from msrest.exceptions import AuthenticationError, ClientException
from azure.mgmt.security import SecurityCenter
from azure.mgmt.resource import PolicyClient

# local imports
from fluidasserts import DAST, MEDIUM
from fluidasserts.utils.decorators import api, unknown_if
from fluidasserts.cloud.azure import _get_result_as_tuple, _get_credentials


def _has_monitoring_param_value(client_id: str, secret: str, tenant: str,
                                subscription_id: str, param_name: str,
                                param_value: str) -> Tuple:
    """
    Check if the value of a parameter is present in a policy assignment.

    :param client_id: Azure service client_id.
    :param secret: Azure service secret.
    :param tenant: Azure service tenant.
    :param subscription_id: Azure subscription ID.
    :param param_name: name of the parameter to verify.
    :param param_value: value that must have the parameter.
    """
    success, fail = [], []

    credentials = _get_credentials(client_id, secret, tenant)
    policies = PolicyClient(credentials, subscription_id).policy_assignments

    for policy in policies.list():
        if param_name in policy.parameters:
            (success if policy.parameters[param_name]['value'] == param_value
             else fail).append(policy.id)
        else:
            pol = policies.get_by_id(policy.policy_definition_id)
            (success
             if pol.parameters[param_name]['defaultValue'] == param_value else
             fail).append(policy.id)
    return (success, fail)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(ClientException, AuthenticationError)
def has_admin_security_alerts_disabled(client_id: str,
                                       secret: str,
                                       tenant: str,
                                       subscription_id: str,
                                       region: str = 'east-us') -> Tuple:
    """
    Check if security alerts are not configured to be sent to admins.

    Enabling security alerts to be sent to admins ensures that detected
    vulnerabilities and security issues are sent to the subscription admins for
    quick remediation.

    :param client_id: Azure service client_id.
    :param secret: Azure service secret.
    :param tenant: Azure service tenant.
    :param subscription_id: Azure subscription ID.

    :returns: - ``OPEN`` if security alerts are not configured to be sent to
                 admins.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = 'Security alerts are not configured to be sent to admins.'
    msg_closed: str = 'Security alerts are configured to be sent to admins.'
    vulns, safes = [], []

    credentials = _get_credentials(client_id, secret, tenant)
    center = SecurityCenter(credentials, subscription_id,
                            region).security_contacts

    (vulns if not list(center.list()) else
     safes).append((f'subscriptions/{subscription_id}',
                    'configure security alerts.'))

    return _get_result_as_tuple(
        objects='Security center',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(ClientException, AuthenticationError)
def has_high_security_alerts_disabled(client_id: str,
                                      secret: str,
                                      tenant: str,
                                      subscription_id: str,
                                      region: str = 'east-us') -> Tuple:
    """
    Check if high security alerts are disabled.

    Enabling high severity alerts ensures that microsoft alerts for potential
    security issues are sent and allows for quick mitigation of the associated
    risks.

    :param client_id: Azure service client_id.
    :param secret: Azure service secret.
    :param tenant: Azure service tenant.
    :param subscription_id: Azure subscription ID.

    :returns: - ``OPEN`` if high security alerts are disabled.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = 'High security alerts are disabled.'
    msg_closed: str = 'High security alerts are enabled.'
    vulns, safes = [], []

    credentials = _get_credentials(client_id, secret, tenant)
    center = SecurityCenter(credentials, subscription_id,
                            region).security_contacts

    for contact in center.list():
        (vulns if contact.alert_notifications == 'Off' else
         safes).append((contact.id, 'enable high security alerts.'))

    if not safes:
        vulns.append((f'subscriptions/{subscription_id}',
                      'configure security alerts.'))

    return _get_result_as_tuple(
        objects='Security center',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(ClientException, AuthenticationError)
def has_blob_encryption_monitor_disabled(
        client_id: str,
        secret: str,
        tenant: str,
        subscription_id: str) -> Tuple:
    """
    Check if Blob Storage Encryption monitoring is disabled.

    When this setting is enabled, Security Center audits blob encryption in all
    storage accounts to enhance data at rest protection.

    Display name: Audit missing blob encryption for storage accounts.

    :param client_id: Azure service client_id.
    :param secret: Azure service secret.
    :param tenant: Azure service tenant.
    :param subscription_id: Azure subscription ID.

    :returns: - ``OPEN`` if Blob Storage Encryption monitoring is disabled.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = 'Blob Storage Encryption monitoring is disabled.'
    msg_closed: str = 'Blob Storage Encryption monitoring is enabled.'
    vulns, safes = _has_monitoring_param_value(
        client_id, secret, tenant, subscription_id,
        'storageEncryptionMonitoringEffect', 'Disabled')

    message = 'enable Blob Storage Encryption monitoring.'
    vulns = list(zip(vulns, repeat(message)))
    safes = list(zip(safes, repeat(message)))

    return _get_result_as_tuple(
        objects='Security center',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(ClientException, AuthenticationError)
def has_disk_encryption_monitor_disabled(
        client_id: str,
        secret: str,
        tenant: str,
        subscription_id: str) -> Tuple:
    """
    Check if Disk encryption monitor is disabled.

    When this setting is enabled, Security Center audits disk encryption in all
    virtual machines to enhance data at rest protection.

    Display name: Disk encryption should be applied on virtual machines.

    :param client_id: Azure service client_id.
    :param secret: Azure service secret.
    :param tenant: Azure service tenant.
    :param subscription_id: Azure subscription ID.

    :returns: - ``OPEN`` if Disk encryption monitor is disabled.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = 'Disk encryption monitor is disabled.'
    msg_closed: str = 'Disk encryption monitor is enabled.'
    vulns, safes = _has_monitoring_param_value(
        client_id, secret, tenant, subscription_id,
        'diskEncryptionMonitoringEffect', 'Disabled')

    message = 'enable Disk encryption monitor.'
    vulns = list(zip(vulns, repeat(message)))
    safes = list(zip(safes, repeat(message)))

    return _get_result_as_tuple(
        objects='Security center',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(ClientException, AuthenticationError)
def has_api_endpoint_monitor_disabled(
        client_id: str,
        secret: str,
        tenant: str,
        subscription_id: str) -> Tuple:
    """
    Check if API endpoint monitor is disabled.

    When this setting is enabled, Security Center audits disk encryption in all
    virtual machines to enhance data at rest protection.

    Display name: Monitor missing Endpoint Protection in Azure Security Center.

    :param client_id: Azure service client_id.
    :param secret: Azure service secret.
    :param tenant: Azure service tenant.
    :param subscription_id: Azure subscription ID.

    :returns: - ``OPEN`` if API endpoint monitor is disabled.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = 'API endpoint monitor is disabled.'
    msg_closed: str = 'API endpoint monitor is enabled.'
    vulns, safes = _has_monitoring_param_value(
        client_id, secret, tenant, subscription_id,
        'endpointProtectionMonitoringEffect', 'Disabled')

    message = 'enable API endpoint monitor.'
    vulns = list(zip(vulns, repeat(message)))
    safes = list(zip(safes, repeat(message)))

    return _get_result_as_tuple(
        objects='Security center',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)
