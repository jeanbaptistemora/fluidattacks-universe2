"""Singer tap for the https://www.currencyconverterapi.com/ API.
"""

import json
import datetime
import urllib.request

from typing import Tuple, Any

# Type aliases that improve clarity
JSON = Any


def get_exchange_rates(currenciea: str, currencieb: str) -> JSON:
    """Make the request and returns a json object with the response.
    """

    resource: str = "https://free.currencyconverterapi.com/api/v6/convert"
    resource += f"?q={currenciea}_{currencieb},{currencieb}_{currenciea}"
    resource += "&compact=ultra"
    request = urllib.request.Request(resource)
    response = urllib.request.urlopen(request).read().decode('utf-8')
    json_obj: JSON = json.loads(response)
    return json_obj


def get_schemas(pairs: Tuple[str, str]) -> JSON:
    """Yield schemas.
    """

    schema: JSON = {
        "type": "SCHEMA",
        "stream": "currencies",
        "key_properties": ["at"],
        "schema": {
            "properties": {
                "at": {
                    "type": "string"
                },
                "date": {
                    "type": "string",
                    "format": "date-time"
                }
            }
        }
    }

    for currenciea, currencieb in pairs:
        schema["schema"]["properties"][f"{currenciea}_{currencieb}"] = {
            "type": "number"
        }
        schema["schema"]["properties"][f"{currencieb}_{currenciea}"] = {
            "type": "number"
        }

    yield schema


def get_records(pairs: Tuple[str, str]) -> JSON:
    """Yields RECORD messages.
    """

    date = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    record: JSON = {
        "type": "RECORD",
        "stream": "currencies",
        "record": {
            "at": "last sync",
            "date": date
        }
    }

    for currenciea, currencieb in pairs:
        json_obj: JSON = get_exchange_rates(currenciea, currencieb)

        pair1: str = f"{currenciea}_{currencieb}"
        pair2: str = f"{currencieb}_{currenciea}"

        record["record"][pair1] = float(json_obj[pair1])
        record["record"][pair2] = float(json_obj[pair2])

    yield record


def main():
    """Usual entry point.
    """

    pairs: Tuple[Tuple[str, str]] = (
        ("COP", "USD"),
        ("COP", "CAD"),
        ("COP", "AUD"),
        ("COP", "NZD"),
        ("COP", "EUR"),
        ("COP", "GBP"),
        ("COP", "JPY"),
        ("COP", "CHF"),
    )

    for schema in get_schemas(pairs):
        print(json.dumps(schema))

    for record in get_records(pairs):
        print(json.dumps(record))


if __name__ == "__main__":
    main()
