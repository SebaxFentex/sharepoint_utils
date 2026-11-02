"""Excepciones de sharepoint_utils y sus codigos de salida.

| Excepcion | codigo_salida | Cuando se lanza |
|---|---|---|
| ExcepcionSharepoint (base) | 1 | Fallo generico de la libreria. |
| ExcepcionCarpetaNoEncontrada | 2 | La carpeta de SharePoint no existe (404). |
| ExcepcionNoAutenticado | 3 | La sesion de Microsoft expiro o no esta autenticada. |
| ExcepcionArchivoNoEncontrado | 4 | El archivo compartido no existe en SharePoint. |
"""


class ExcepcionSharepoint(Exception):
    """Base de las excepciones de la libreria (codigo_salida = 1)."""

    codigo_salida = 1


class ExcepcionNoAutenticado(ExcepcionSharepoint):
    """Se lanza cuando la sesion de Microsoft ha expirado o no esta autenticada."""

    codigo_salida = 3


class ExcepcionCarpetaNoEncontrada(ExcepcionSharepoint):
    """Se lanza cuando la carpeta de SharePoint no existe (404)."""

    codigo_salida = 2


class ExcepcionArchivoNoEncontrado(ExcepcionSharepoint):
    """Se lanza cuando el archivo compartido no existe en SharePoint."""

    codigo_salida = 4
