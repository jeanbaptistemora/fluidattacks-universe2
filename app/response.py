import json


def object(data, message, error):
    response_data = {}
    response_data['data'] = data
    response_data['message'] = message
    response_data['error'] = error
    return response_data