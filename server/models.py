from pydantic import BaseModel, Field
from typing import Optional


class ResponseFormat:
    """"""
    message: str = Field(description="")
    tool: Optional[str] = Field(description="")


class UserInfo:
    def __init__(self, user_id=0, name=""):
        self.user_id = user_id
        self.name = name


class WeatherInput(BaseModel):
    location: str = Field(description="City name or coordinates")
