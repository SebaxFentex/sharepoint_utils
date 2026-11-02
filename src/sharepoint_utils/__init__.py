import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())

from sharepoint_utils._excepciones import (
    ExcepcionArchivoNoEncontrado,
    ExcepcionCarpetaNoEncontrada,
    ExcepcionNoAutenticado,
)
from sharepoint_utils.cliente import ClienteSharepoint

# Nota: login_manual NO se re-exporta aqui a proposito para mantener la
# superficie publica minima (cliente + excepciones). Canonico:
# from sharepoint_utils.cliente import login_manual
__all__ = [
    "ClienteSharepoint",
    "ExcepcionArchivoNoEncontrado",
    "ExcepcionCarpetaNoEncontrada",
    "ExcepcionNoAutenticado",
]
