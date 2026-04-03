from pydantic import BaseModel, Field
from typing import Optional
import argparse


class WeatherInput(BaseModel):
    """
    Input schema for the weather tool.
    """
    location: str = Field(description="City name or coordinates")
