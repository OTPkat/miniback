from pydantic import BaseModel
from typing import Optional


class Duelist(BaseModel):
    discord_user_id: int
    availability: bool
    name: str
    message_id: Optional[str]
    n_win: Optional[int] = 0
    n_loss: Optional[int] = 0
    n_draw: Optional[int] = 0

    class Config:
        orm_mode = True


class DuelCreate(BaseModel):
    defier_id: int
    challenged_id: int
    n_choices: int
    defier_choices: Optional[str]
    defier_get_pinged: Optional[bool]
    challenged_choices: Optional[str]
    challenged_get_pinged: Optional[bool]
    done: Optional[bool]
    winner_discord_id: Optional[int]
    is_draw: Optional[bool]


class Duel(DuelCreate):
    id: int

    class Config:
        orm_mode = True
