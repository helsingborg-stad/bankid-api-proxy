import asyncio
import base64

from pydantic import BaseModel, Field

from src.lib.validators import validate_swedish_personal_number
from src.lib.post import Endpoint, post
from src.models import AuthSignModel


class SignRequestModel(BaseModel):
    end_user_ip: str = Field(validation_alias="endUserIp")
    personal_number: str = Field(validation_alias="personalNumber", min_length=10, max_length=12)


def _sign_sync(model: SignRequestModel) -> AuthSignModel:
    data = post(payload={
        "endUserIp": model.end_user_ip,
        "userVisibleData": base64.b64encode("Sign in to Helsingborg stad".encode("utf-8")).decode("ascii"),
        "requirement": {
            "personalNumber": model.personal_number,
        }
    }, endpoint=Endpoint.AUTH)

    return AuthSignModel(
        order_ref=data["orderRef"],
        auto_start_token=data["autoStartToken"],
        qr_start_token=data["qrStartToken"],
        qr_start_secret=data["qrStartSecret"],
    )


async def sign(model: SignRequestModel) -> AuthSignModel:
    if not validate_swedish_personal_number(model.personal_number):
        raise ValueError("Invalid personal number")

    return await asyncio.to_thread(_sign_sync, model)
