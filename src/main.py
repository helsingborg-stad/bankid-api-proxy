from typing import Annotated
from dotenv import load_dotenv
from fastapi import Body, FastAPI, HTTPException


def create_app() -> FastAPI:
    load_dotenv()

    from src.auth import AuthRequestModel, auth
    from src.collect import CollectModel, CollectRequestModel, collect
    from src.cancel import CancelRequestModel, cancel
    from src.models import ResponseModel, AuthSignModel
    from src.sign import SignRequestModel, sign

    app = FastAPI(title="BankID API")

    @app.post("/auth", response_model=ResponseModel)
    async def auth_endpoint(model: Annotated[AuthRequestModel, Body(embed=False)]) -> ResponseModel[AuthSignModel]:
        try:
            auth_data = await auth(model)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        return ResponseModel[AuthSignModel](data=ResponseModel.Data(attributes=auth_data, type="bankIdAuth"))

    @app.post("/sign", response_model=ResponseModel)
    async def auth_endpoint(model: Annotated[SignRequestModel, Body(embed=False)]) -> ResponseModel[AuthSignModel]:
        try:
            sign_data = await sign(model)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        return ResponseModel[AuthSignModel](data=ResponseModel.Data(attributes=sign_data, type="bankIdSign"))

    @app.post("/collect", response_model=ResponseModel)
    async def collect_endpoint(model: Annotated[CollectRequestModel, Body(embed=False)]) -> ResponseModel[
        CollectModel]:
        try:
            collect_data = await collect(model)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        return ResponseModel[CollectModel](data=ResponseModel.Data(attributes=collect_data, type="bankIdCollect"))

    @app.post("/cancel")
    async def cancel_endpoint(model: Annotated[CancelRequestModel, Body(embed=False)]) -> None:
        try:
            await cancel(model)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    return app
