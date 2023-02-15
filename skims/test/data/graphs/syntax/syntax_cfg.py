from itertools import (
    accumulate,
    chain,
)
import json
import os

FIELDS_BY_LANGUAGE: dict[str, tuple[str, ...]] = {}


class InsufficientAmount(Exception):
    pass


class Wallet(dict[str, int]):
    def __init__(self, initial_amount: int = 0) -> None:
        self.balance = initial_amount

    def spend_cash(self, amount: int) -> None:
        if self.balance < amount:
            raise InsufficientAmount(f"Not enough available to spend {amount}")
        self.balance -= amount

    def add_cash(self, amount: int) -> None:
        self.balance += amount


def main() -> None:
    number = 100
    modulus = number % 2
    if modulus == 0:
        print("The number is Even.")
    else:
        print("The number is Odd.")

    sum_var = 0
    count = 10
    for i in range(count):
        sum_var = sum_var + i
    avg = sum_var / count
    print("The average is: ", avg)

    count = 0
    mult_var = 1
    while count < 10:
        count = count + 1
        mult_var *= number


def comprehensions() -> None:
    input_list = [1, 2, 3, 4, 4, 5, 6, 7, 7]
    list_using_comp = [var for var in input_list if var % 2 == 0]
    print(list_using_comp)
    set_using_comp = {var for var in input_list if var % 2 == 0}
    print(set_using_comp)
    dict_using_comp = {var: var**3 for var in input_list if var % 2 != 0}
    print(dict_using_comp)

    state = ["Gujarat", "Maharashtra", "Rajasthan"]
    capital = ["Gandhinagar", "Mumbai", "Jaipur"]
    output_dict = {}
    for (key, value) in zip(state, capital):
        output_dict[key] = value

    try:
        my_numbers = [1, 2, 3]
        accumulate(my_numbers)
        chain(my_numbers)
        print(my_numbers[10])
    except IndexError as err:
        if str(err) == "Error":
            print("Error")


def get_artifact(env_var: str) -> str:
    if value := env_var:
        return value
    raise ValueError(f"Expected environment variable: {env_var}")


TREE_SITTER_PARSERS = get_artifact("SKIMS_TREE_SITTER_PARSERS")


def get_fields_by_language() -> None:
    for lang in ["spanish", "english"]:
        if len(lang) < 3:
            continue

        path: str = os.path.join(TREE_SITTER_PARSERS, f"{lang}-fields.json")
        with open(path, encoding="utf-8") as file:
            FIELDS_BY_LANGUAGE[lang] = json.load(file)


def capital_case(country_name: str) -> str:
    return country_name.capitalize()


def test_capital_case() -> None:
    assert capital_case("semaphore") == "Semaphore"
