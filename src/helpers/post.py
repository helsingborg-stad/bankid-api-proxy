import json
import os
from enum import Enum
from typing import Any

from src.helpers.session import _get_session

_BANKID_BASE_URL = os.getenv("BANKID_BASE_URL")


class Endpoint(Enum):
    COLLECT = "collect"
    AUTH = "auth"
    CANCEL = "cancel"


def post(payload: dict[str, Any], endpoint: Endpoint) -> Any:
    r = _get_session().post(f"{_BANKID_BASE_URL}/{endpoint.value}", data=json.dumps(payload), timeout=(5, 20))
    if r.status_code != 200:
        raise ValueError(f"BankID API error: {r.status_code} {r.text[:1000]}")
    return r.json()
