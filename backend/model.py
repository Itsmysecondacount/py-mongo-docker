from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class Timbre(BaseModel):
    mesage: str
    hora: Optional[datetime]
