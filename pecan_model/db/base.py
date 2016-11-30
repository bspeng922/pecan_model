from pecan import conf

from sqlalchemy import create_engine
import sqlalchemy.orm

from pecan_model.model import user


_ENGINE = None
_SESSION_MAKER = None


def get_engine():
    global _ENGINE
    if _ENGINE is not None:
        return _ENGINE

    _ENGINE = create_engine(conf.sqlalchemy['url'])
    user.Base.metadata.create_all(_ENGINE)
    return _ENGINE


def get_session_maker(engine):
    global _SESSION_MAKER
    if _SESSION_MAKER is not None:
        return _SESSION_MAKER

    _SESSION_MAKER = sqlalchemy.orm.sessionmaker(bind=engine)
    return _SESSION_MAKER


def get_session():
    engine = get_engine()
    maker = get_session_maker(engine)
    session = maker()

    return session