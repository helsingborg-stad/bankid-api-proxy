import asyncio
from pydantic import BaseModel, Field

from src.lib.post import Endpoint, post


class CancelRequestModel(BaseModel):
    order_ref: str = Field(validation_alias="orderRef")


def _cancel_sync(model: CancelRequestModel) -> bool:
    return True if post(payload={"orderRef": model.order_ref}, endpoint=Endpoint.CANCEL) else False


async def cancel(model: CancelRequestModel) -> bool:
    return await asyncio.to_thread(_cancel_sync, model)
