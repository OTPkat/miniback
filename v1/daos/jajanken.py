from sqlalchemy.orm import Session
from v1.schemas.jajanken import Duelist, DuelCreate, Duel
import models
from sqlalchemy.future import select


class DuelistDao:
    @staticmethod
    async def get_duelist(db: Session, discord_user_id: int):
        duelist = await db.execute(
            select(models.Duelist).where(models.Duelist.discord_user_id == discord_user_id)
        )
        return duelist.scalars().first()

    @staticmethod
    async def get_duelists(db: Session):
        duelists = await db.execute(select(models.Duelist))
        return duelists.scalars().all()

    @staticmethod
    async def get_duelist_by_message_id(db: Session, message_id: int):
        duelist = await db.execute(
            select(models.Duelist).where(models.Duelist.message_id == message_id)
        )
        return duelist.scalars().first()

    @staticmethod
    async def insert_duelist(db: Session, duelist: Duelist):
        duelist = models.Duelist(**duelist.dict())
        db.add(duelist)
        await db.commit()
        await db.refresh(duelist)
        return duelist

    @staticmethod
    async def clear_duelists(db: Session):
        nfts = await db.execute(select(models.Duelist))
        for nft in nfts.scalars().all():
            await db.delete(nft)
        await db.commit()

    @classmethod
    async def insert_duel(cls, db: Session, duel: DuelCreate):
        duel = models.Duel(**duel.dict())
        defier_duelist: Duelist = await cls.get_duelist(db=db, discord_user_id=duel.defier_id)
        challenged_duelist: Duelist = await cls.get_duelist(db=db, discord_user_id=duel.challenged_id)
        if duel.is_draw:
            defier_duelist.n_draw += 1
            challenged_duelist.n_draw += 1
        elif duel.winner_discord_id == duel.defier_id:
            defier_duelist.n_win += 1
            challenged_duelist.n_loss += 1
        else:
            defier_duelist.n_loss += 1
            challenged_duelist.n_win += 1
        db.add(duel)
        await db.commit()
        await db.refresh(duel)
        return duel

    @staticmethod
    async def get_duels(db: Session):
        duels = await db.execute(select(models.Duels))
        return duels.scalars().all()

