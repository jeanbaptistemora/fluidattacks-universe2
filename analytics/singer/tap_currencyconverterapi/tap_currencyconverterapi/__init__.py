"""
Singer.io tap for the https://www.currencyconverterapi.com/ API
"""

## python3 -m pylint (default configuration)
# Your code has been rated at 10.00/10

import json
import datetime
import urllib.request

def get_exchange_rates():
    """ make the request and returns a json object with the response """
    resource = "https://free.currencyconverterapi.com/api/v6/convert"
    resource += "?q=USD_COP"
    resource += ",COP_USD"
    resource += "&compact=ultra"
    request = urllib.request.Request(resource)
    response = urllib.request.urlopen(request).read()
    json_obj = json.loads(response.decode('utf-8'))
    return json_obj

def write_schema():
    """ write the SCHEMA message to stdout """

    stdout_json_obj = {
        "type": "SCHEMA",
        "stream": "currencies",
        "key_properties": ["at"],
        "schema": {
            "properties": {
                "at": {
                    "type": "string"
                },
                "USD_COP": {
                    "type": "number"
                },
                "COP_USD": {
                    "type": "number"
                },
                "date": {
                    "type": "string",
                    "format": "date-time"
                },
            }
        }
    }

    print(json.dumps(stdout_json_obj))

def write_records(json_obj):
    """ write the RECORD message to stdout """

    date = datetime.datetime.utcnow().isoformat("T") + "Z"

    stdout_json_obj = {
        "type": "RECORD",
        "stream": "currencies",
        "record": {
            "at": "last sync",
            "USD_COP": float(json_obj["USD_COP"]),
            "COP_USD": float(json_obj["COP_USD"]),
            "date": str(date)
        }
    }

    print(json.dumps(stdout_json_obj))

def main():
    """ usual entry point """
    json_obj = get_exchange_rates()

    write_schema()
    write_records(json_obj)

if __name__ == "__main__":
    main()
