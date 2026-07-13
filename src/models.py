from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=True)
    name: Mapped[str] = mapped_column(String(80), nullable=True)
    last_name: Mapped[str] = mapped_column(String(80), nullable=True)
    subscription_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    favorites: Mapped[List["Favorite"]] = relationship(back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "last_name": self.last_name,
            "subscription_date": self.subscription_date,
           
        }


class Planet(db.Model):
    __tablename__ = "planet"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    climate: Mapped[str] = mapped_column(String(120), nullable=True)
    terrain: Mapped[str] = mapped_column(String(120), nullable=True)
    population: Mapped[int] = mapped_column(nullable=True)

    
    favorites: Mapped[List["Favorite"]] = relationship(back_populates="planet")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "terrain": self.terrain,
            "population": self.population,
        }


class Character(db.Model):
    __tablename__ = "character"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    height: Mapped[str] = mapped_column(String(20), nullable=True)
    birth_year: Mapped[str] = mapped_column(String(20), nullable=True)
    gender: Mapped[str] = mapped_column(String(20), nullable=True)

    
    favorites: Mapped[List["Favorite"]] = relationship(back_populates="character")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "birth_year": self.birth_year,
            "gender": self.gender,
        }


class Favorite(db.Model):
    
    __tablename__ = "favorite"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    planet_id: Mapped[Optional[int]] = mapped_column(ForeignKey("planet.id"), nullable=True)
    character_id: Mapped[Optional[int]] = mapped_column(ForeignKey("character.id"), nullable=True)

    user: Mapped["User"] = relationship(back_populates="favorites")
    planet: Mapped[Optional["Planet"]] = relationship(back_populates="favorites")
    character: Mapped[Optional["Character"]] = relationship(back_populates="favorites")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet": self.planet.serialize() if self.planet else None,
            "character": self.character.serialize() if self.character else None,
        }