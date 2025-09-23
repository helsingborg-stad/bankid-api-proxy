import requests
import pathlib

from src.helpers.config import CONFIG

_ROOT_PATH = pathlib.Path(__file__).parent.parent.parent
_CERT_PATH = _ROOT_PATH / "cert" / CONFIG["CERT_PEM"]
_KEY_PATH = _ROOT_PATH / "cert" / CONFIG["KEY_PEM"]
_SERVER_CERT_PATH = _ROOT_PATH / "cert" / CONFIG["SERVER_CERT_PEM"]
_P12_PASSWORD = CONFIG["PASSWORD"]

_SESSION: requests.Session | None = None


def _get_session() -> requests.Session:
    global _SESSION
    if _SESSION is not None:
        return _SESSION

    s = requests.Session()
    s.cert = (_CERT_PATH.as_posix(), _KEY_PATH.as_posix())
    s.verify = _SERVER_CERT_PATH.as_posix()
    s.headers.update({"Content-Type": "application/json", "Accept": "application/json"})
    _SESSION = s
    return s
