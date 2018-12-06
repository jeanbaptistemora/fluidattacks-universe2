#!/usr/bin/python3

"""
Formstack API wrapper
"""

import urllib.request
import json


def get_request_response(user_token, resource):
  """ make a request and grab the response """
  response = urllib.request.urlopen(urllib.request.Request(
    resource,
    headers={"Accept": "application/json",
             "Content-Type": "application/json",
             "Authorization": "Bearer " + user_token})).read()
  json_str = response
  json_obj = json.loads(json_str)
  return json_obj


def get_all_forms(user_token, page="1", per_page="50"):
  """ get all forms in the account """
  resource = "https://www.formstack.com/api/v2/form.json"
  resource += "?page=" + page
  resource += "&per_page=" + per_page
  response = get_request_response(user_token, resource)
  return response


def get_form_submissions(
  user_token, form_id,
  page="1", per_page="100",
  min_time="0000-01-01", max_time="2100-12-31"
):
  """ get all submissions made for the specified form """
  resource = "https://www.formstack.com/api/v2/form/"
  resource += form_id
  resource += "/submission.json"
  resource += "?min_time=" + min_time
  resource += "&max_time=" + max_time
  resource += "&page=" + page
  resource += "&per_page=" + per_page
  resource += "&sort=DESC"
  resource += "&data=0"
  # resource += "&expand_data=0"
  response = get_request_response(user_token, resource)
  return response


def get_form_by_id(user_token, form_id):
  """ get the details of the specified form """
  resource = "https://www.formstack.com/api/v2/form/"
  resource += form_id + ".json"
  response = get_request_response(user_token, resource)
  return response


def get_all_fields_on_form(user_token, form_id):
  """ get all fields for the specified form """
  resource = "https://www.formstack.com/api/v2/form/"
  resource += form_id + "/"
  resource += "field.json"
  response = get_request_response(user_token, resource)
  return response


def get_fields_by_id(user_token, field_id):
  """ get the details of the specified form """
  resource = "https://www.formstack.com/api/v2/field/"
  resource += field_id + ".json"
  response = get_request_response(user_token, resource)
  return response


def get_all_folders(user_token, page="1", per_page="50"):
  """ get all folders on the account and their subfolders """
  resource = "https://www.formstack.com/api/v2/folder.json"
  resource += "?page=" + page
  resource += "&per_page=" + per_page
  response = get_request_response(user_token, resource)
  return response


def get_folder_by_id(user_token, folder_id):
  """ get details for the specified folder or subfolder """
  resource = "https://www.formstack.com/api/v2/folder/"
  resource += folder_id + ".json"
  response = get_request_response(user_token, resource)
  return response
