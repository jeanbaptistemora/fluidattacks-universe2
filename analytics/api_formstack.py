"""
Formstack API wrapper
"""

## python3 -m pylint (default configuration)
# Your code has been rated at 10.00/10

import urllib.request
import json

def get_request_response(user_token, resource):
    """ make a request for 'resource' and returns a json object with the response """
    headers = {"Accept": "application/json",
               "Content-Type": "application/json",
               "Authorization": "Bearer " + user_token}
    request = urllib.request.Request(resource, headers=headers)
    response = urllib.request.urlopen(request).read()
    json_obj = json.loads(response)
    return json_obj

def get_all_forms(user_token, params):
    """ get all forms in the account """
    resource = "https://www.formstack.com/api/v2/form.json"
    resource += "?page=" + params["page"]
    resource += "&per_page=100"
    json_obj = get_request_response(user_token, resource)
    return json_obj

def get_form_submissions(user_token, form_id, params):
    """ get all submissions made for the specified form_id """
    resource = "https://www.formstack.com/api/v2/form/"
    resource += form_id
    resource += "/submission.json"
    resource += "?min_time=0000-01-01"
    resource += "&max_time=2100-12-31"
    resource += "&page=" + params["page"]
    resource += "&per_page=100"
    resource += "&sort=DESC"
    resource += "&data=0"
    resource += "&expand_data=0"
    json_obj = get_request_response(user_token, resource)
    return json_obj

def get_form_by_id(user_token, form_id):
    """ get the details of the specified form """
    resource = "https://www.formstack.com/api/v2/form/"
    resource += form_id + ".json"
    json_obj = get_request_response(user_token, resource)
    return json_obj

def get_all_fields_on_form(user_token, form_id):
    """ get all fields for the specified form """
    resource = "https://www.formstack.com/api/v2/form/"
    resource += form_id + "/field.json"
    json_obj = get_request_response(user_token, resource)
    return json_obj

def get_fields_by_id(user_token, field_id):
    """ get the details of the specified form """
    resource = "https://www.formstack.com/api/v2/field/"
    resource += field_id + ".json"
    json_obj = get_request_response(user_token, resource)
    return json_obj

def get_all_folders(user_token, params):
    """ get all folders on the account and their subfolders """
    resource = "https://www.formstack.com/api/v2/folder.json"
    resource += "?page=" + params["page"]
    resource += "&per_page=" + params["per_page"]
    json_obj = get_request_response(user_token, resource)
    return json_obj

def get_folder_by_id(user_token, folder_id):
    """ get details for the specified folder or subfolder """
    resource = "https://www.formstack.com/api/v2/folder/"
    resource += folder_id + ".json"
    json_obj = get_request_response(user_token, resource)
    return json_obj
