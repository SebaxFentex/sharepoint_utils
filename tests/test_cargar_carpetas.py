import logging
import os
from pathlib import Path

from sharepoint_utils import ClienteSharepoint, ExcepcionNoAutenticado
from log_utils import configurar_log


def _requerir_env(nombre: str) -> str:
    valor = os.environ.get(nombre)
    if not valor:
        raise SystemExit(f"Define {nombre} en el .env local (ver .env.example)")
    return valor

URL_CARPETA_DESTINO = _requerir_env("SHAREPOINT_URL_CARPETA_PRUEBAS")
CORREO_USUARIO = _requerir_env("SHAREPOINT_CORREO_USUARIO")
URL_INICIO = _requerir_env("SHAREPOINT_URL_INICIO")
CARPETA_CARGA = Path(__file__).resolve().parent / "archivos" / "carga"

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


def _preparar_fixtures_carga() -> list[str]:
    """Genera los 10 .txt de carga/ y retorna las carpetas de primer nivel.

    Carpetas de primer nivel (carpeta_1, carpeta_2 con carpeta_21 anidada,
    carpeta_3 vacia, esta ultima se omite por estar vacia).
    """
    for relativo, contenido in ESTRUCTURA_CARGA.items():
        ruta = CARPETA_CARGA / relativo
        ruta.parent.mkdir(parents=True, exist_ok=True)
        ruta.write_text(contenido, encoding="utf-8")
    (CARPETA_CARGA / "carpeta_3").mkdir(parents=True, exist_ok=True)
    log.info("Fixtures de carga generados: %s", CARPETA_CARGA)
    return [str(p) for p in sorted(CARPETA_CARGA.iterdir()) if p.is_dir()]


log = logging.getLogger("sharepoint_utils")

def main() -> None:
    configurar_log(
        nombre="sharepoint_utils",
        carpeta_logs=Path(__file__).resolve().parent.parent / "logs",
        nivel_archivo=os.environ.get("SHAREPOINT_NIVEL_LOG"),
        nivel_consola=os.environ.get("SHAREPOINT_NIVEL_LOG"),
        prefijo="sharepoint_utils-",
    )
    carpetas_a_cargar = _preparar_fixtures_carga()
    try:
        with ClienteSharepoint(correo_usuario=CORREO_USUARIO, url_inicio=URL_INICIO, mostrar_navegador=True) as cargador:
            cargador.cargar_carpetas({URL_CARPETA_DESTINO: carpetas_a_cargar})
            log.info("OK: carga de carpetas completada")
    except ExcepcionNoAutenticado as exc:
        log.error("Fallo autenticacion: %s", exc)
        raise SystemExit(exc.codigo_salida) from exc

if __name__ == "__main__":
    main()
