"""
Fluid ETL script
"""

## python3 -m pylint (default configuration)
# Your code has been rated at 10.00/10

import sys

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
    # get the available forms in the account
    AVAILABLE_FORMS = tap_formstack.get_available_forms(FORMSTACK_TOKEN)

    # first download everything, it won't download encrypted forms
    for form_name, form_id in AVAILABLE_FORMS.items():
        tap_formstack.write_queries(FORMSTACK_TOKEN, form_name, form_id)

    # now write schema and records for each form except encrypted forms
    for form_name, form_id in AVAILABLE_FORMS.items():
        try:
            form_schema = tap_formstack.write_schema(form_name)
            tap_formstack.write_records(form_name, form_schema)
        # Given an encrypted form is not downloaded
        # Then the file doesn't exist
        except FileNotFoundError:
            pass
