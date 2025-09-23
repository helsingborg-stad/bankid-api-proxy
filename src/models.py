from pydantic import BaseModel, Field

from src.collect import CollectModel


class AuthSignModel(BaseModel):
    order_ref: str = Field(serialization_alias="orderRef")
    auto_start_token: str = Field(serialization_alias="autoStartToken")
    qr_start_token: str = Field(serialization_alias="qrStartToken")
    qr_start_secret: str = Field(serialization_alias="qrStartSecret")


class Data[T](BaseModel):
    type: str
    attributes: T


class ResponseModel[T](BaseModel):
    data: Data[T]


AuthSignResponseModel = ResponseModel[AuthSignModel]
CollectResponseModel = ResponseModel[CollectModel]
