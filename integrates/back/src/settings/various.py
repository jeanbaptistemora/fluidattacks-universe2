from context import (
    FI_DEBUG,
)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEBUG = FI_DEBUG == "True"
TIME_ZONE = "America/Bogota"
