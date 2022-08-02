import os

try:
    CRITERIA_VULNERABILITIES: str = os.environ[
        "CHARTS_CRITERIA_VULNERABILITIES"
    ]
except KeyError as exe:
    print("Environment variable " + exe.args[0] + " doesn't exist")
    raise
