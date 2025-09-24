import asyncio
from pydantic import BaseModel, Field

from src.helpers.validators import validate_swedish_personal_number
from src.helpers.post import Endpoint, post
from src.models import AuthSignModel


class AuthRequestModel(BaseModel):
    end_user_ip: str = Field(validation_alias="endUserIp")
    personal_number: str | None = Field(default=None, validation_alias="personalNumber", min_length=10, max_length=12)


def _auth_sync(model: AuthRequestModel) -> AuthSignModel:
    if model.personal_number and not validate_swedish_personal_number(model.personal_number):
        raise ValueError("Invalid personal number")

    data = post(payload={
        "endUserIp": model.end_user_ip,
        **({"requirement": {
            "personalNumber": model.personal_number,
        }} if model.personal_number else {})
    }, endpoint=Endpoint.AUTH)

    return AuthSignModel(
        order_ref=data["orderRef"],
        auto_start_token=data["autoStartToken"],
        qr_start_token=data["qrStartToken"],
        qr_start_secret=data["qrStartSecret"],
    )


async def auth(model: AuthRequestModel) -> AuthSignModel:
    return await asyncio.to_thread(_auth_sync, model)
