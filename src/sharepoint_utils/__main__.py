"""Entry point para `python -m sharepoint_utils` (login manual).

Uso:
    python -m sharepoint_utils [URL_INICIO]

Precedencia: argumento > SHAREPOINT_URL_INICIO > error con mensaje.
"""

import argparse
import os
from pathlib import Path


def renovar_autenticacion(argumentos: list[str] | None = None) -> None:
    """Resuelve la URL, configura logs y corre el login interactivo standalone."""
    from log_utils import configurar_log
    from sharepoint_utils.cliente import login_manual

    analizador = argparse.ArgumentParser(description="Login manual de SharePoint (MFA).")
    analizador.add_argument(
        "url_inicio",
        nargs="?",
        default=None,
        help="URL de inicio para validar la sesion (opcional si hay SHAREPOINT_URL_INICIO).",
    )
    opciones = analizador.parse_args(argumentos)

    url_inicio = opciones.url_inicio or os.environ.get("SHAREPOINT_URL_INICIO")
    if not url_inicio:
        raise SystemExit(
            "Falta la URL de inicio: pasala como argumento (`python -m sharepoint_utils <URL>`) "
            "o define SHAREPOINT_URL_INICIO en el .env (ver .env.example)."
        )
    configurar_log(
        nombre="sharepoint_utils",
        carpeta_logs=Path(__file__).resolve().parents[2] / "logs",
        nivel_archivo=os.environ.get("SHAREPOINT_NIVEL_LOG"),
        nivel_consola=os.environ.get("SHAREPOINT_NIVEL_LOG"),
        prefijo="sharepoint_utils-",
    )
    login_manual(url_inicio)


if __name__ == "__main__":
    renovar_autenticacion()
