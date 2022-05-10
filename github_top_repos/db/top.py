from sqlalchemy import Integer, String, Column

from .base import Base


class Top(Base):
    __tablename__ = "top"

    id = Column(Integer, primary_key=True)
    org_name = Column(String(100), nullable=False)
    repo_name = Column(String(100), nullable=False)
    stars_count = Column(Integer, nullable=False)
