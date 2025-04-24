from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(120), unique=False, nullable=False)
    last_name: Mapped[str] = mapped_column(String(120), unique=False, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
   
    # relationship
    favorite: Mapped[List["Favorite"]] = relationship(back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Character(db.Model):
    __tablename__ = "character"
    id: Mapped[int] = mapped_column(primary_key=True)
    char_name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    birth_year: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    gender: Mapped[str] = mapped_column(String(12), unique=True, nullable=False)
    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"))

    # relationship 
    home_world: Mapped["Planet"] = relationship(back_populates="characters")
    favorite: Mapped[List["Favorite"]] = relationship(back_populates="char")


class Planet(db.Model):
    __tablename__ = "planet"
    id: Mapped[int] = mapped_column(primary_key=True)
    planet_name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    population: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    climate: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)

    # relationship
    characters: Mapped[List["Character"]] = relationship(back_populates="home_world")
    favorite: Mapped[List["Favorite"]] = relationship(back_populates="planet")
    

class Favorite(db.Model):
    __tablename__ = "favorite"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    char_id: Mapped[int] = mapped_column(ForeignKey("character.id"))
    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"))

      # relationship
    user: Mapped["User"] = relationship(back_populates="favorite")
    char: Mapped["Character"] = relationship(back_populates="favorite")
    planet: Mapped["Planet"] = relationship(back_populates="favorite")