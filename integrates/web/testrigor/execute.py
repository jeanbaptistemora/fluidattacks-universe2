from context import (
    CI_COMMIT_REF_NAME,
    CI_COMMIT_SHA,
    TESTRIGOR_AUTH_TOKEN,
    TESTRIGOR_SUITE_ID,
)
import glob
import os
import requests
from session import (
    append_session,
)
from time import (
    sleep,
)


def _append_variables(test_content: str) -> str:
    return test_content.replace("{CI_COMMIT_REF_NAME}", CI_COMMIT_REF_NAME)


def _get_test_content(test_content: str) -> str:
    with_variables = _append_variables(test_content)
    with_session = append_session(with_variables)
    return with_session


def _get_tests() -> list[dict[str, str]]:
    tests = []
    for file in glob.glob("./tests/*.txt"):
        with open(file, "r") as test_file:
            tests.append(
                {
                    "customSteps": _get_test_content(test_file.read()),
                    "description": os.path.basename(test_file.name),
                }
            )
    return tests


def _execute_tests() -> None:
    response = requests.post(
        f"https://api.testrigor.com/api/v1/apps/{TESTRIGOR_SUITE_ID}/retest",
        headers={
            "auth-token": TESTRIGOR_AUTH_TOKEN,
            "content-type": "application/json",
        },
        json={
            "baselineMutations": _get_tests(),
            "branch": {
                "commit": CI_COMMIT_SHA,
                "name": CI_COMMIT_REF_NAME,
            },
            "explicitMutations": True,
            "forceCancelPreviousTesting": True,
            "url": f"https://{CI_COMMIT_REF_NAME}.app.fluidattacks.com/",
        },
    )
    if response.status_code != 200:
        raise Exception("Couldn't execute tests")


def _check_completion() -> None:
    while True:
        response = requests.get(
            f"https://api.testrigor.com/api/v1/apps/{TESTRIGOR_SUITE_ID}/status",
            headers={
                "accept": "application/json",
                "auth-token": TESTRIGOR_AUTH_TOKEN,
                "content-type": "application/json",
            },
            params={"branchName": CI_COMMIT_REF_NAME},
        )
        if response.status_code == 200:
            print("Test finished successfully")
            break
        elif response.status_code in [227, 228]:
            print("Test is not finished yet")
        elif response.status_code == 230:
            print(response)
            print("Test finished but failed")
            break
        elif response.status_code > 400:
            raise Exception("Error calling testRigor API")
        else:
            print(response)
            raise Exception("Unknown status")
        sleep(10)


def main() -> None:
    _execute_tests()
    _check_completion()


if __name__ == "__main__":
    main()
