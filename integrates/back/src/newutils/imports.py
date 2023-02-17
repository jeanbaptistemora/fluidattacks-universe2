import importlib
import os


def generate_all(path: str, package: str) -> list[str]:
    """Util to generate __all__ dynamically"""
    modules = []

    for file in os.listdir(os.path.dirname(path)):
        if file.endswith(".py") and not file.startswith("_"):
            module_name = os.path.basename(file)[:-3]
            importlib.import_module(f".{module_name}", package)
            modules.append(module_name)

    return modules
