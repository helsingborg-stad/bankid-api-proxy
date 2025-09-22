import asyncio
from typing import Any
from pydantic import BaseModel, Field

from src.lib.post import Endpoint, post


class CollectModel(BaseModel):
    order_ref: str = Field(serialization_alias="orderRef")
    status: str
    completion_data: dict[str, Any] | None = Field(default=None, serialization_alias="completionData")


class CollectRequestModel(BaseModel):
    order_ref: str = Field(validation_alias="orderRef")


def _collect_sync(model: CollectRequestModel) -> CollectModel:
    data = post(payload={"orderRef": model.order_ref}, endpoint=Endpoint.COLLECT)
    return CollectModel(
        order_ref=data["orderRef"],
        status=data["status"],
        completion_data=data["completionData"] if "completionData" in data else None,
    )


async def collect(model: CollectRequestModel) -> CollectModel:
    return await asyncio.to_thread(_collect_sync, model)
