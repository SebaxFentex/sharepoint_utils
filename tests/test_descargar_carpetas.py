import logging
import os
import shutil
from pathlib import Path

from sharepoint_utils import (
    ClienteSharepoint,
    ExcepcionCarpetaNoEncontrada,
    ExcepcionNoAutenticado,
)
from log_utils import configurar_log

log = logging.getLogger("sharepoint_utils")

def _requerir_env(nombre: str) -> str:
    valor = os.environ.get(nombre)
    if not valor:
        raise SystemExit(f"Define {nombre} en el .env local (ver .env.example)")
    return valor

URL_CARPETA_BASE = _requerir_env("SHAREPOINT_URL_CARPETA_PRUEBAS")

# Carpetas cargadas por test_cargar_carpetas.py.
CARPETAS_A_DESCARGAR = ["carpeta_1", "carpeta_2", "carpeta_3"]
CARPETA_CARGA = Path(__file__).resolve().parent / "archivos" / "carga"
CARPETA_DESCARGA = Path(__file__).resolve().parent / "archivos" / "descarga"
CORREO_USUARIO = _requerir_env("SHAREPOINT_CORREO_USUARIO")
URL_INICIO = _requerir_env("SHAREPOINT_URL_INICIO")

# Fixtures autogenerados al arrancar (no versionados): 10 .txt con contenido
# deterministico sin salto final (md5 identicos a los versionados en v1.3.0).
ESTRUCTURA_CARGA = {
    "archivo_1.txt": "file_1",
    "archivo_2.txt": "file_2",
    "archivo_3.txt": "file_3",
    "carpeta_1/archivo_11.txt": "file_11",
    "carpeta_1/archivo_12.txt": "file_12",
    "carpeta_2/archivo_21.txt": "file_21",
    "carpeta_2/archivo_22.txt": "file_22",
    "carpeta_2/carpeta_21/archivo_211.txt": "file_211",
    "carpeta_2/carpeta_21/archivo_212.txt": "file_212",
    "carpeta_2/carpeta_21/archivo_213.txt": "file_213",
}


def _preparar_fixtures_carga() -> None:
    """Genera los 10 .txt de carga/ con contenido deterministico."""
    for relativo, contenido in ESTRUCTURA_CARGA.items():
        ruta = CARPETA_CARGA / relativo
        ruta.parent.mkdir(parents=True, exist_ok=True)
        ruta.write_text(contenido, encoding="utf-8")
    (CARPETA_CARGA / "carpeta_3").mkdir(parents=True, exist_ok=True)
    log.info("Fixtures de carga generados: %s", CARPETA_CARGA)


def _limpiar_carpeta_descarga() -> Path:
    """Borra el contenido previo de descarga/ y lo recrea vacio."""
    shutil.rmtree(CARPETA_DESCARGA, ignore_errors=True)
    CARPETA_DESCARGA.mkdir(parents=True, exist_ok=True)
    log.info("Carpeta de descarga limpia: %s", CARPETA_DESCARGA)
    return CARPETA_DESCARGA

def main() -> None:
    configurar_log(
        nombre="sharepoint_utils",
        carpeta_logs=Path(__file__).resolve().parent.parent / "logs",
        nivel_archivo=os.environ.get("SHAREPOINT_NIVEL_LOG"),
        nivel_consola=os.environ.get("SHAREPOINT_NIVEL_LOG"),
        prefijo="sharepoint_utils-",
    )
    _preparar_fixtures_carga()
    _limpiar_carpeta_descarga()
    try:
        with ClienteSharepoint(correo_usuario=CORREO_USUARIO, url_inicio=URL_INICIO, mostrar_navegador=True) as descargador:
            for nombre in CARPETAS_A_DESCARGAR:
                url_carpeta = f"{URL_CARPETA_BASE}/{nombre}"
                destino = CARPETA_DESCARGA
                descargador.descargar_carpeta(url_carpeta, str(destino))
                log.info("OK: %s descargada en: %s", nombre, destino)
    except ExcepcionCarpetaNoEncontrada as exc:
        log.error("Carpeta no encontrada: %s", exc)
        raise SystemExit(exc.codigo_salida) from exc
    except ExcepcionNoAutenticado as exc:
        log.error("Fallo autenticacion: %s", exc)
        raise SystemExit(exc.codigo_salida) from exc

if __name__ == "__main__":
    main()
