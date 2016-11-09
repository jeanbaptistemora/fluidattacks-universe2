"""
    Configuracion de logs para Integrates
"""
import logging

logging.basicConfig(
    filename='logs/error.err',
    format='%(levelname)s: %(asctime)s %(message)s',
    level=logging.DEBUG
)
