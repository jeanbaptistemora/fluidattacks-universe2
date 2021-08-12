import configparser
import os
import sys


def main():
    root_path = sys.argv[1]
    config_path = sys.argv[2]
    check_missing = sys.argv[3].lower() == "true"
    ignore = (
        "__init__.py",
        "py.typed",
        ".cfg",
        "__pycache__",
        "gitlab-ci.yml",
    )
    expected_layers = set(
        module.replace(".py", "")
        for module in os.listdir(root_path)
        if not module.endswith(ignore)
    )

    config = configparser.ConfigParser()
    with open(config_path) as config_handle:
        config.read_string(config_handle.read())

    layers = {
        layer.strip()
        for layer in config["importlinter:contract:dag"]["layers"].splitlines()
        if layer
    }

    if layers == expected_layers:
        sys.exit(0)
    elif check_missing:
        print("[ERROR] Please specify all layers")
        print("[INFO] Missing layers:")
        for layer in sorted(expected_layers - layers):
            print(f"    {layer}")
        print("[INFO] Extra layers:")
        for layer in sorted(layers - expected_layers):
            print(f"    {layer}")
        sys.exit(1)


if __name__ == "__main__":
    main()
