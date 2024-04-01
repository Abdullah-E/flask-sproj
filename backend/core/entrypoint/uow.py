"""unit of work"""
import os
from abc import ABC, abstractmethod

import psycopg2
from psycopg2.extensions import AsIs, adapt, register_adapter
from psycopg2.extras import DictCursor, Json
from psycopg2.extensions import cursor, connection
from dotenv import load_dotenv
from core.authentication.adapters import repository as auth_repo
from core.handyman.adapters import repository as handy_repo
from core.authentication.domain import model as auth_mdl
from core.handyman.domain import model as handy_mdl

load_dotenv()

class AbstractUnitOfWork(ABC):
    users: auth_repo.UserAbstractRepository
    handymen: handy_repo.HandymanAbstractRepository
    tasks: handy_repo.TaskAbstractRepository

    def __init__(self) -> None:
        self.connection: connection
        self.cursor: cursor
        self.dict_cursor: DictCursor

    def __enter__(self) -> "AbstractUnitOfWork":
        return self

    def __exit__(self, *args):
        pass

    def commit_close_connection(self):
        pass

    def close_connection(self):
        pass

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError


class FakeUnitOfWork(AbstractUnitOfWork):
    def __init__(self):
        self.users: auth_repo.FakeUserRepository = auth_repo.FakeUserRepository()
        self.handymen: handy_repo.FakeHandymanRepository = handy_repo.FakeHandymanRepository()
        self.tasks: handy_repo.FakeTaskRepository = handy_repo.FakeTaskRepository()

    def commit(self):
        pass

    def rollback(self):
        pass


class UnitOfWork(AbstractUnitOfWork):
    def __init__(self):
        db_host = os.environ.get("DB_HOST")
        db_name = os.environ.get("DB_NAME")
        db_user = os.environ.get("DB_USER")
        db_pass = os.environ.get("DB_PASSWORD")
        db_port = os.environ.get("DB_PORT")
        db_connect_timeout = os.environ.get("DB_CONNECT_TIMEOUT")

        self.connection = psycopg2.connect(
            host=db_host,
            dbname=db_name,
            user=db_user,
            password=db_pass,
            port=db_port,
            connect_timeout=db_connect_timeout,
        )

        self.cursor = self.connection.cursor()
        self.dict_cursor = self.connection.cursor(cursor_factory=DictCursor)

        self.users: auth_repo.UserRepository = auth_repo.UserRepository(self.connection)
        self.handymen: handy_repo.HandymanRepository = handy_repo.HandymanRepository(self.connection)
        self.tasks: handy_repo.TaskRepository = handy_repo.TaskRepository(self.connection)

    def __enter__(self, *args):
        super().__enter__(*args)

    def __exit__(self, *args):
        super().__exit__(*args)

    def commit_close_connection(self):
        self.commit()
        self.close_connection()

    def close_connection(self):
        self.connection.close()

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()
