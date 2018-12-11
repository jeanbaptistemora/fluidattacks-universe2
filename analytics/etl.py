"""
Fluid ETL script
"""

## pyhton3 -m pylint (default configuration)
# Your code has been rated at 10.00/10

import sys

import logs
import tap_formstack

# Long term goal:
#     ETL script:
#         Extract & Transform from:
#             Formstack
#             Timedoctor
#             Mailchimp
#             Salesforce
#         Load to:
#             Amazon Athena
#             Stitchdata
#             Google sheets


if __name__ == "__main__":
    # catch arguments
    try:
        FORMSTACK_TOKEN = str(sys.argv[1])
    except IndexError:
        print("Use: etl.py formstack_token")
        sys.exit(1)

    # ==== Formstack  ==========================================================
    # initialize log files
    logs.initialize_log("tap_formstack.stdout.json")
    logs.initialize_log("tap_formstack.stdout.pretty.json")

    # get the available forms in the account
    AVAILABLE_FORMS = tap_formstack.get_available_forms(FORMSTACK_TOKEN)

    # first download everything
    for form_name, form_id in AVAILABLE_FORMS.items():
        tap_formstack.write_queries(FORMSTACK_TOKEN, form_name, form_id)

    # now write schema and records for each form
    for form_name, form_id in AVAILABLE_FORMS.items():
        tap_formstack.write_schema(form_name)
        tap_formstack.write_records(form_name)
