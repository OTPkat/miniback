from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from v1.schemas.jajanken import Duel, Duelist, DuelCreate
from v1.daos.jajanken import DuelistDao
from typing import List
from database import get_db, engine
from models import Base


app = FastAPI(title="Miniback")


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@app.post("/duelists/", response_model=Duelist)
async def post_duelist(
    duelist: Duelist, db: Session = Depends(get_db)
):
    duelist = await DuelistDao.insert_duelist(db=db, duelist=duelist)
    return duelist


@app.get("/duelists/", response_model=List[Duelist])
async def get_duelists(
    db: Session = Depends(get_db)
):
    duelists = await DuelistDao.get_duelists(db=db)
    return duelists


@app.get("/duelists/{duelist_id}", response_model=Duelist)
async def get_duelist(
    discord_user_id: int, db: Session = Depends(get_db)
):
    duelists = await DuelistDao.get_duelist(db=db, discord_user_id=discord_user_id)
    return duelists


@app.get("/duelist_messages/{message_id}", response_model=Duelist)
async def get_duelist_by_message_id(
    message_id: int, db: Session = Depends(get_db),
):
    duelist = await DuelistDao.get_duelist_by_message_id(db=db, message_id=message_id)
    return duelist
