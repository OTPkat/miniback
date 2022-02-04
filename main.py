from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from v1.schemas.jajanken import Duel, Duelist, DuelCreate, Match, Player
from v1.daos.jajanken import DuelistDao, TournamentDao
from typing import List
from database import get_db, engine
from models import Base


app = FastAPI(title="Miniback")


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


############### DUELS ##################

@app.post("/duelists/", response_model=Duelist)
async def post_duelist(
    duelist: Duelist, db: Session = Depends(get_db)
):
    duelist = await DuelistDao.post_duelist(db=db, duelist=duelist)
    return duelist


@app.post("/clear_duelists/",)
async def clear_duelists(
    db: Session = Depends(get_db)
):
    await DuelistDao.clear(db=db)
    return 1


@app.get("/duelists/", response_model=List[Duelist])
async def get_duelists(
    db: Session = Depends(get_db)
):
    duelists = await DuelistDao.get_duelists(db=db)
    return duelists


@app.get("/duelist/{discord_user_id}", response_model=Duelist)
async def get_duelist(
    discord_user_id: int, db: Session = Depends(get_db)
):
    duelist = await DuelistDao.get_duelist(db=db, discord_user_id=discord_user_id)
    return duelist


@app.get("/duelist_messages/{message_id}", response_model=Duelist)
async def get_duelist_by_message_id(
    message_id: int, db: Session = Depends(get_db),
):
    duelist = await DuelistDao.get_duelist_by_message_id(db=db, message_id=message_id)
    return duelist


@app.post("/duels/", response_model=Duel)
async def post_duel(
    duel: DuelCreate, db: Session = Depends(get_db)
):
    duelist = await DuelistDao.insert_duel(db=db, duel=duel)
    return duelist


@app.get("/duels/", response_model=List[Duel])
async def get_duels(
    db: Session = Depends(get_db)
):
    duels = await DuelistDao.get_duels(db=db)
    return duels


# Tournament

@app.post("/matches/", response_model=Match)
async def post_match(
    match: Match, db: Session = Depends(get_db)
):
    match = await TournamentDao.post_match(db=db, match=match)
    return match


@app.post("/players/", response_model=Player)
async def post_player(
    player: Player, db: Session = Depends(get_db)
):
    player = await TournamentDao.insert_player(db=db, player=player)
    return player


@app.get("/players/", response_model=List[Player])
async def get_players(
    db: Session = Depends(get_db)
):
    players = await TournamentDao.get_players(db=db)
    return players


@app.get("/player/{discord_user_id}", response_model=Player)
async def get_player(
    discord_user_id: int, db: Session = Depends(get_db)
):
    player = await TournamentDao.get_player(db=db, discord_user_id=discord_user_id)
    return player


@app.post("/clear_players/",)
async def clear_players(
    db: Session = Depends(get_db)
):
    await TournamentDao.clear(db=db)
    return 1


