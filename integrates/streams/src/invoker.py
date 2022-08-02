import importlib
import sys


def invoke_consumer(module_name: str) -> None:
    """Invokes the requested consumer"""
    consumer = importlib.import_module(f"{module_name}.consumer")
    consumer.consume()


if __name__ == "__main__":
    invoke_consumer(sys.argv[1])
