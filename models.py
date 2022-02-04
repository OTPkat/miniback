from sqlalchemy import Column, Integer, String, Boolean, DateTime, BigInteger
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Duelist(Base):
    __tablename__ = "duelists"
    discord_user_id = Column(BigInteger, primary_key=True, index=True)
    availability = Column(Boolean)
    name = Column(String)
    message_id = Column(BigInteger, nullable=True)
    n_win = Column(Integer)
    n_loss = Column(Integer)
    n_draw = Column(Integer)


class Duel(Base):
    __tablename__ = "duels"
    id = Column(Integer, primary_key=True, index=True)
    defier_id = Column(BigInteger)
    challenged_id = Column(BigInteger)
    n_choices = Column(Integer)
    defier_choices = Column(String, nullable=True)
    defier_get_pinged = Column(Boolean, nullable=True)
    challenged_choices = Column(String, nullable=True)
    challenged_get_pinged = Column(Boolean, nullable=True)
    done = Column(Boolean, nullable=True)
    winner_discord_id = Column(BigInteger, nullable=True)
    is_draw = Column(Boolean, nullable=True)


class Player(Base):
    __tablename__ = "players"
    discord_user_id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String)
    n_win = Column(Integer)
    n_loss = Column(Integer)
    n_draw = Column(Integer)
    n_revision = Column(Integer, nullable=True)
    get_pinged = Column(Boolean, nullable=True)
    choices = Column(String, nullable=True)
