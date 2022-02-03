from sqlalchemy.orm import Session
from v1.schemas.jajanken import Duelist, DuelCreate, Duel
import models
from sqlalchemy.future import select
from sqlalchemy import func


class DuelistDao:
    @staticmethod
    async def get_duelist(db: Session, discord_user_id: int):
        nft = await db.execute(
            select(models.Duelist).where(models.Duelist.discord_user_id == discord_user_id)
        )
        return nft.scalars().first()

    @staticmethod
    async def get_duelists(db: Session):
        nfts = await db.execute(select(models.Duelist))
        return nfts.scalars().all()

    @staticmethod
    async def get_duelist_by_message_id(db: Session, message_id: int):
        nft = await db.execute(
            select(models.Duelist).where(models.Duelist.message_id == message_id)
        )
        return nft.scalars().first()

    @staticmethod
    async def insert_duelist(db: Session, duelist: Duelist):
        nft = models.Duelist(**duelist.dict())
        db.add(nft)
        await db.commit()
        await db.refresh(nft)
        return nft

    @staticmethod
    async def clear_duelists(db: Session):
        nfts = await db.execute(select(models.Duelist))
        for nft in nfts.scalars().all():
            await db.delete(nft)
        await db.commit()

    @staticmethod
    async def process_duel(db: Session, duel: DuelCreate):
        # todo record duel + update two corresponding players
        pass
