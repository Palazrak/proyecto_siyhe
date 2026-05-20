from pydantic import BaseModel, Field


class LoginPayload(BaseModel):
    usuario: str = Field(min_length=1, max_length=50)
    password: str = Field(min_length=1, max_length=128)


class PlacaPayload(BaseModel):
    usuario: str = Field(min_length=1, max_length=50)
    placa: str = Field(min_length=1, max_length=20)
