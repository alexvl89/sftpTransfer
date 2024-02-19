import datetime
from email.headerregistry import Address

from sqlalchemy import create_engine
import sqlalchemy as sa
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)


class LogEntry(Base):
    __tablename__ = "log_entries"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    timestamp = Column(sa.DateTime(timezone=True),
                       default=datetime.datetime.utcnow)
    message = Column(String)


class SqlProvider:
    def __init__(self, db_path):
        self.engine = create_engine(f"sqlite:///{db_path}")
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()

    @staticmethod
    def create_database(name: str) -> None:
        """
        Создание базы данных
        """
        engine = create_engine(f"sqlite:///{name}.sqlite")

        # Создание всех таблиц, определенных в Base
        Base.metadata.create_all(engine)

    def add_log_entry(self, user_id: int, message: str, time_stamp=datetime.datetime.utcnow()) -> None:
        """
        Добавление лога
        """
        new_entry = LogEntry(
            user_id=user_id, message=message, timestamp=time_stamp)
        self.session.add(new_entry)
        self.session.commit()

    def close(self):
        """
        Закрытие сессии
        """
        self.session.close()
