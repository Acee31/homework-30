from sqlalchemy import Column, Integer, String

from app.database import Base


class Recipe(Base):
    __tablename__ = "Recipes"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    cooking_time = Column(Integer, nullable=False)
    views = Column(Integer, default=0)
