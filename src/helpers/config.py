from os import getenv
from dotenv import load_dotenv

load_dotenv()


def get_config() -> dict[str, str | bool]:
    def str_to_bool(s: str) -> bool:
        return s.lower() in ("yes", "true", "t", "1")

    return {
        "API_KEY": getenv("API_KEY", ""),
        "BANKID_BASE_URL": getenv("BANKID_BASE_URL", ""),
        "DEBUG": str_to_bool(getenv("DEBUG", "False")),
        "CERT_PEM": getenv("CERT_PEM", ""),
        "KEY_PEM": getenv("KEY_PEM", ""),
        "SERVER_CERT_PEM": getenv("SERVER_CERT_PEM", ""),
        "PASSWORD": getenv("PASSWORD", ""),
    }


CONFIG = get_config()
