from sqlalchemy.orm import Session
from v1.schemas.jajanken import Duelist, DuelCreate, Player, Match
import models
from sqlalchemy.future import select
from sqlalchemy import update


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
        duels = await db.execute(select(models.Duel))
        return duels.scalars().all()

    @classmethod
    async def post_duelist(cls, db: Session, duelist: Duelist):
        duelist_ = await cls.get_duelist(db=db, discord_user_id=duelist.discord_user_id)
        if duelist_:
            duelist_update = (
                update(models.Duelist).where(models.Duelist.discord_user_id == duelist.discord_user_id).values(**duelist.dict())
            ).execution_options(synchronize_session="fetch")
            await db.execute(duelist_update)
            await db.commit()
            return duelist_
        else:
            duelist = await cls.insert_duelist(db=db,duelist=duelist)
            return duelist


class TournamentDao:

    @staticmethod
    async def get_player(db: Session, discord_user_id: int):
        player = await db.execute(
            select(models.Player).where(models.Player.discord_user_id == discord_user_id)
        )
        return player.scalars().first()

    @staticmethod
    async def get_players(db: Session):
        players = await db.execute(select(models.Player))
        return players.scalars().all()

    @staticmethod
    async def insert_player(db: Session, player: Player):
        player = models.Duelist(**player.dict())
        db.add(player)
        await db.commit()
        await db.refresh(player)
        return player

    @classmethod
    async def post_match(cls, db: Session, match: Match):
        player_1: Player = await cls.get_player(db=db, discord_user_id=match.player_1_discord_id)
        player_2: Player = await cls.get_player(db=db, discord_user_id=match.player_2_discord_id)
        if match.is_draw:
            player_1.n_draw += 1
            player_2.n_draw += 1
        elif match.winner_discord_id == match.player_1_discord_id:
            player_1.n_win += 1
            player_2.n_loss += 1
        else:
            player_1.n_loss += 1
            player_2.n_win += 1
        player_1.choices = match.player_1_choices
        player_2.choices = match.player_2_choices
        player_1.get_pinged = match.player_1_get_pinged
        player_2.get_pinged = match.player_2_get_pinged
        player_1.n_revision = match.player_1_revisions
        player_2.n_revision = match.player_2_revisions
        await db.commit()
        return match

