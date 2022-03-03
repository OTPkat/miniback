from pydantic import BaseModel
from typing import Optional


class Duelist(BaseModel):
    discord_user_id: int
    availability: bool
    name: str
    message_id: Optional[int]
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


class Player(BaseModel):
    discord_user_id: int
    name: str
    n_win: Optional[int] = 0
    n_loss: Optional[int] = 0
    n_draw: Optional[int] = 0
    get_pinged: Optional[bool] = False
    n_revision: Optional[int] = 0
    choices: Optional[str] = None

    class Config:
        orm_mode = True


class Match(BaseModel):
    player_1_discord_id: int
    player_2_discord_id: int
    player_1_choices: str
    player_2_choices: str
    player_1_get_pinged: bool
    player_2_get_pinged: bool
    is_draw: bool
    player_1_revisions: int
    player_2_revisions: int
    winner_discord_id: Optional[int]


class TournamentMatchCreate(BaseModel):
    discord_user_id: int
    bracket: int
    match_id: int
    get_pinged: Optional[bool] = False
    choices: Optional[str] = None
    is_winner: Optional[bool]


class TournamentMatch(TournamentMatchCreate):
    id: int

    class Config:
        orm_mode = True


class TournamentUpdate(BaseModel):
    discord_user_id: int
    bracket: int
    get_pinged: Optional[bool]
    choices: Optional[str]
    is_winner: Optional[bool]