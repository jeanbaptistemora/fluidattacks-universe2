import os
from __init__ import (
    FI_DEBUG,
)

DEBUG = FI_DEBUG == 'True'
TIME_ZONE = 'America/Bogota'

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname((os.path.abspath(__file__))))
)
