from pydantic import BaseModel, Field


class ResponseModel[T](BaseModel):
    class Data(BaseModel):
        type: str
        attributes: T

    data: Data


class AuthSignModel(BaseModel):
    order_ref: str = Field(serialization_alias="orderRef")
    auto_start_token: str = Field(serialization_alias="autoStartToken")
    qr_start_token: str = Field(serialization_alias="qrStartToken")
    qr_start_secret: str = Field(serialization_alias="qrStartSecret")
