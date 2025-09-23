from typing import Annotated
from dotenv import load_dotenv
from fastapi import Body, FastAPI, HTTPException


def create_app() -> FastAPI:
    load_dotenv()

    from src.auth import AuthRequestModel, auth
    from src.collect import CollectRequestModel, collect
    from src.cancel import CancelRequestModel, cancel
    from src.models import AuthSignResponseModel, CollectResponseModel
    from src.sign import SignRequestModel, sign

    app = FastAPI(title="BankID API")

    @app.post("/auth", response_model=AuthSignResponseModel)
    async def auth_endpoint(model: Annotated[AuthRequestModel, Body(embed=False)]) -> AuthSignResponseModel:
        try:
            auth_data = await auth(model)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        return AuthSignResponseModel(data={"attributes": auth_data, "type": "bankIdAuth"})

    @app.post("/sign", response_model=AuthSignResponseModel)
    async def sign_endpoint(model: Annotated[SignRequestModel, Body(embed=False)]) -> AuthSignResponseModel:
        try:
            sign_data = await sign(model)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        return AuthSignResponseModel(data={"attributes": sign_data, "type": "bankIdSign"})

    @app.post("/collect", response_model=CollectResponseModel)
    async def collect_endpoint(model: Annotated[CollectRequestModel, Body(embed=False)]) -> CollectResponseModel:
        try:
            collect_data = await collect(model)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        return CollectResponseModel(data={"attributes": collect_data, "type": "bankIdCollect"})

    @app.post("/cancel")
    async def cancel_endpoint(model: Annotated[CancelRequestModel, Body(embed=False)]) -> None:
        try:
            await cancel(model)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    return app
