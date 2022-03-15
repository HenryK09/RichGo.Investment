import sqlalchemy
import pandas as pd
import hashlib
from sqlalchemy.pool import SingletonThreadPool
from sqlalchemy.orm import sessionmaker
import contextlib

__all__ = [
    'DBConn'
]


class _FetchResult:
    def __init__(self, columns, data):
        self.columns = columns
        self.data = data

    def df(self):
        return pd.DataFrame(columns=self.columns, data=self.data)

    def at(self, index=0):
        return self.data[0][index]

    def list(self):
        return list(*zip(*self.data))


class DBConn:
    _instance = {}
    _engine = None
    _session = None
    _trans = None

    def __new__(cls, uri, *args, **kwargs):
        key = hashlib.md5(uri.encode('ascii')).hexdigest()
        if key not in cls._instance:
            instance = super(DBConn, cls).__new__(cls)
            instance._uri = uri
            instance._create_engine()
            cls._instance[key] = instance
        else:
            instance = cls._instance[key]

        return instance

    @property
    def engine(self):
        return self._engine or self._create_engine()

    def _create_engine(self):
        self._engine = sqlalchemy.create_engine(self._uri,
                                                poolclass=SingletonThreadPool,
                                                pool_recycle=3600,
                                                pool_size=10)
        self._Session = sessionmaker(bind=self._engine)
        return self._engine

    def fetch(self, query, *args, **kwargs) -> _FetchResult:
        def _fetch(_sess):
            _result = _sess.execute(sqlalchemy.text(query), *args, **kwargs)
            _fetch_data = _result.fetchall()
            _keys = _result.keys()
            _result.close()
            return _keys, _fetch_data

        if self._session is not None:
            keys, fetch_data = _fetch(self._session)
        else:
            with self._Session() as session:
                keys, fetch_data = _fetch(session)

        return _FetchResult(keys, fetch_data)

    def update(self, query, *args, **kwargs):
        assert self._session
        self._session.execute(sqlalchemy.text(query), *args, **kwargs)

    @contextlib.contextmanager
    def transaction(self):
        if self._session is not None:
            yield
            return

        with self._Session() as session:
            with session.begin() as trans:
                self._session = session
                self._trans = trans

                try:
                    yield
                    self._trans.commit()

                except Exception as e:
                    if trans.is_active:
                        trans.rollback()
                    raise e

                finally:
                    self._trans = None
                    self._session = None

    def dispose(self):
        if self._trans:
            self._trans.rollback()
            self._trans = None

        if self._session:
            self._session.close()
            self._session = None

        if self._engine:
            self._engine.dispose()
            self._engine = None
