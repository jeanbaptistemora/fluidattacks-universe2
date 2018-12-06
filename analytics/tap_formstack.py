#!/usr/bin/python3

"""
Singer tap for Formstack:
  Formstack > singer > *
            ^
            | this script
"""

import API_formstack
import sys

# Long term goal:
#   singer tap to crawl the formstack forms
#     configurable
#     error resistant
#     historical and incremental
# Current state:
#   lists all the forms in the account and its IDs
#   allows me to download all the form submissions in pretty format given an ID
# Short term goal:
#   write the tap Output engine
#     write the RECORD Message
#       record. A JSON map containing a streamed data point
#       stream. The string name of the stream
#     write the SCHEMA Message
#     write the STATE  Message
# Medium term goal:
#   write support for the Config  input
#   write support for the State   input
#   write support for the Catalog input


def parse_form_submissions(user_token, form_id):
  json_obj = API_formstack.get_form_submissions(user_token, form_id)
  for submissions in json_obj["submissions"]:
    for key_s in submissions:
      val_s = submissions[key_s]
      if key_s == "id":
        print("id: " + val_s)
      if key_s == "timestamp":
        print("  timestamp: " + val_s)
      if key_s == "data":
        data = val_s
        print("  data:")
        for key_d in data:
          field = data[key_d]
          for key_f in field:
            val_f = field[key_f]
            if key_f == "field":
              print("    field: " + val_f)
            if key_f == "type":
              print("      type: " + val_f)
            if key_f == "value":
              print("      value: " + val_f)


def print_available_forms(user_token, current=0, page=1):
  json_obj = API_formstack.get_all_forms(user_token, str(page), "10")
  for form in json_obj["forms"]:
    print(form["name"] + " " + form["id"])
    current += 1
  if current < int(json_obj["total"]):
    print_available_forms(user_token, current, page + 1)


def main():
  # arguments
  user_token = ""

  # catch them
  try:
    user_token = str(sys.argv[1])
  except:
    print("Use: python3 tap_formstack.py user_token")
    sys.exit(1)

  # list all forms and its IDs
  print_available_forms(user_token)

  # print to console all the "test" forms submitted
  parse_form_submissions(user_token, "2962425")


main()
