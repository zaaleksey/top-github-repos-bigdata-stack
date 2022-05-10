import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from .base import Base
from .top import Top


class GitHubTopicDB:
    FILE_PATH = "db/github-topic.db"

    def __init__(self, clear_data: bool = False):
        if clear_data:
            GitHubTopicDB.remove_db_file()

        self.engine = create_engine(f"sqlite:///{GitHubTopicDB.FILE_PATH}")
        Base.metadata.create_all(self.engine)
        self.session = Session(bind=self.engine)

    def add(self, instance: Top) -> None:
        self.session.add(instance)
        self.session.commit()

    def add_all(self, instances: list[Top]) -> None:
        self.session.add_all(instances)
        self.session.commit()

    def get_all_top(self) -> list[Top]:
        return self.session.query(Top).all()

    def get_top_size(self) -> int:
        return self.session.query(Top).count()

    @classmethod
    def remove_db_file(cls) -> None:
        if os.path.exists(cls.FILE_PATH):
            os.remove(cls.FILE_PATH)
