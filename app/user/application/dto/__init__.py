from pydantic import BaseModel, Field


class GetUserListResponseDTO(BaseModel):
    id: int = Field(..., description="ID")
    email: str = Field(..., description="Email")
    nickname: str = Field(..., description="Nickname")


class GetUserResponseDTO(BaseModel):
    id: int = Field(..., description="ID")
    email: str = Field(..., description="Email")
    nickname: str = Field(..., description="Nickname")
    events: list = Field(..., description="Event List")

class CreateUserRequestDTO(BaseModel):
    email: str = Field(..., description="Email")
    password1: str = Field(..., description="Password1")
    password2: str = Field(..., description="Password2")
    nickname: str = Field(..., description="Nickname")


class CreateUserResponseDTO(BaseModel):
    email: str = Field(..., description="Email")
    nickname: str = Field(..., description="Nickname")


class LoginResponseDTO(BaseModel):
    token: str = Field(..., description="Token")
    refresh_token: str = Field(..., description="Refresh token")


class AddEventResponseDTO(BaseModel):
    event_id: int = Field(..., description="Event ID")
    user_id: int = Field(..., description="User ID")
