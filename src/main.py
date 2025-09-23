from typing import Annotated
from fastapi import Body, FastAPI, HTTPException, status
from fastapi.params import Depends
from fastapi.security import APIKeyHeader

from src.helpers.config import CONFIG

header_scheme = APIKeyHeader(name="X-API-Key")


def create_app() -> FastAPI:
    from src.auth import AuthRequestModel, auth
    from src.collect import CollectRequestModel, collect
    from src.cancel import CancelRequestModel, cancel
    from src.models import AuthSignResponseModel, CollectResponseModel
    from src.sign import SignRequestModel, sign

    app = FastAPI(title="BankID API")

    @app.post("/auth", response_model=AuthSignResponseModel)
    async def auth_endpoint(model: Annotated[AuthRequestModel, Body(embed=False)],
                            api_key: Annotated[str, Depends(header_scheme)]) -> AuthSignResponseModel:
        if api_key != CONFIG["API_KEY"]:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")

        try:
            auth_data = await auth(model)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

        return AuthSignResponseModel(data={"attributes": auth_data, "type": "bankIdAuth"})

    @app.post("/sign", response_model=AuthSignResponseModel)
    async def sign_endpoint(model: Annotated[SignRequestModel, Body(embed=False)],
                            api_key: Annotated[str, Depends(header_scheme)]) -> AuthSignResponseModel:
        if api_key != CONFIG["API_KEY"]:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")

        try:
            sign_data = await sign(model)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

        return AuthSignResponseModel(data={"attributes": sign_data, "type": "bankIdSign"})

    @app.post("/collect", response_model=CollectResponseModel)
    async def collect_endpoint(model: Annotated[CollectRequestModel, Body(embed=False)],
                               api_key: Annotated[str, Depends(header_scheme)]) -> CollectResponseModel:
        if api_key != CONFIG["API_KEY"]:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")

        try:
            collect_data = await collect(model)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

        return CollectResponseModel(data={"attributes": collect_data, "type": "bankIdCollect"})

    @app.post("/cancel")
    async def cancel_endpoint(model: Annotated[CancelRequestModel, Body(embed=False)],
                              api_key: Annotated[str, Depends(header_scheme)]) -> None:
        if api_key != CONFIG["API_KEY"]:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")

        try:
            await cancel(model)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return app
