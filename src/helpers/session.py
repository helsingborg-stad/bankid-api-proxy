import os
import requests
import pathlib

_CERT_PATH = pathlib.Path(__file__).parent.parent.parent / "cert" / os.getenv("CERT_PEM")
_KEY_PATH = pathlib.Path(__file__).parent.parent.parent / "cert" / os.getenv("KEY_PEM")
_SERVER_CERT_PATH = pathlib.Path(__file__).parent.parent.parent / "cert" / os.getenv("SERVER_CERT_PEM")
_P12_PASSWORD = os.getenv("PASSWORD")

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
