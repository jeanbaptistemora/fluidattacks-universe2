# coding=utf-8
""" Auxiliar functions for forms handling """

from datetime import datetime

# pylint: disable=redefined-builtin
try:
    type(reduce)
except NameError:
    from functools import reduce


def dict_concatenation(dict_1, dict_2):
    dict_1_copy = dict_1.copy()
    dict_1_copy.update(dict_2)
    return dict_1_copy


def drive_url_filter(drive):
    """ Gets ID of the drive image """
    if drive.find("s3.amazonaws.com") != -1:
        new_url = drive.split("/")[5]
        return new_url
    else:
        if drive.find("id=") != -1:
            new_url = drive.split("id=")[1]
            if new_url.find("&") != -1:
                return new_url.split("&")[0]
    return drive


def remove_standard_keys(dictionary):
    return {dictionary['field']: dictionary['value']}


def merge_dicts_list_into_dict(dicts_list):
    dicts_without_standard_keys = [remove_standard_keys(x)
                                   for x in dicts_list]
    return reduce(dict_concatenation, dicts_without_standard_keys)


def create_dict(remission_submission):
    remission_dict = merge_dicts_list_into_dict(remission_submission["data"])
    return remission_dict


def get_impact(severity, version):
    severity = float(severity)
    if version == '3':
        if severity == 0:
            impact = 'Ninguno'
        elif severity <= 3.9:
            impact = 'Bajo'
        elif severity <= 6.9:
            impact = 'Medio'
        elif severity <= 8.9:
            impact = 'Alto'
        else:
            impact = 'Crítico'
    else:
        if severity <= 3.9:
            impact = 'Bajo'
        elif severity <= 6.9:
            impact = 'Medio'
        else:
            impact = 'Alto'
    return impact


def is_exploitable(explotability, version):
    if version == '3':
        if explotability >= 0.97:
            exploitable = 'Si'
        else:
            exploitable = 'No'
    else:
        if explotability == 1.0 or explotability == 0.95:
            exploitable = 'Si'
        else:
            exploitable = 'No'
    return exploitable


def to_formstack(data):
    new_data = dict()
    for key, value in data.items():
        new_data["field_" + str(key)] = value
    return new_data


def round_date(date):
    seconds_in_hour = 3600
    hours = round(date.seconds / seconds_in_hour)
    if hours > 12:
        rounded_date = date.days + 1
    else:
        rounded_date = date.days
    return rounded_date


def string_to_date(string):
    return datetime.strptime(string, "%Y-%m-%d %H:%M:%S")


def cast_finding_attributes(finding):
    cast_finding_field = {
        'Detallado': 'DETAILED',
        'General': 'GENERAL',
        'Puntual': 'ONESHOT',
        'Continua': 'CONTINUOUS',
        'Análisis': 'ANALYSIS',
        'Aplicación': 'APP',
        'Binario': 'BINARY',
        'Código fuente': 'SOURCE_CODE',
        'Infraestructura': 'INFRASTRUCTURE',
        'Seguridad': 'SECURITY',
        'Higiene': 'HYGIENE',
        'Cualquier persona en Internet': 'ANYONE_INTERNET',
        'Cualquier cliente de la organización': 'ANY_CUSTOMER',
        'Solo algunos clientes de la organización': 'SOME_CUSTOMERS',
        'Cualquier persona con acceso a la estación': 'ANYONE_WORKSTATION',
        'Cualquier empleado de la organización': 'ANY_EMPLOYEE',
        'Solo algunos empleados': 'SOME_EMPLOYEES',
        'Solo un empleado': 'ONE_EMPLOYEE',
        'Anónimo desde internet': 'ANONYMOUS_INTERNET',
        'Anónimo desde intranet': 'ANONYMOUS_INTRANET',
        'Extranet usuario autorizado': 'AUTHORIZED_USER_EXTRANET',
        'Extranet usuario no autorizado': 'UNAUTHORIZED_USER_EXTRANET',
        'Internet usuario autorizado': 'AUTHORIZED_USER_INTERNET',
        'Internet usuario no autorizado': 'UNAUTHORIZED_USER_INTERNET',
        'Intranet usuario autorizado': 'AUTHORIZED_USER_INTRANET',
        'Intranet usuario no autorizado': 'UNAUTHORIZED_USER_INTRANET',
        'Aplicaciones': 'APPLICATIONS',
        'Bases de Datos': 'DATABASES',
        'Búsqueda': 'SEARCHING',
        'Cierre': 'CLOSING',
        'Verificación': 'VERIFYING',
        'Asumido': 'ACCEPTED',
        'Nuevo': 'NEW',
        'Remediar': 'IN PROGRESS'
    }
    list_fields = ['subscription', 'testType', 'findingType',
                   'actor', 'scenario', 'ambit', 'context', 'treatment']
    for field in list_fields:
        if finding.get(field):
            finding[field] = cast_finding_field.get(
                finding.get(field).encode('utf-8'), finding.get(field))
    return finding
