from datetime import datetime
from typing import List

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    gender: Mapped[str] = mapped_column(String(6))
    title: Mapped[str] = mapped_column(String(4))
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(30))
    uuid: Mapped[str] = mapped_column(String(36))
    username: Mapped[str] = mapped_column(String(30))
    password: Mapped[str] = mapped_column(String(30))
    salt: Mapped[str] = mapped_column(String(30))
    md5: Mapped[str] = mapped_column(String(32))
    sha1: Mapped[str] = mapped_column(String(40))
    sha256: Mapped[str] = mapped_column(String(64))
    date_of_birth: Mapped[datetime] = mapped_column(DateTime())
    registered: Mapped[datetime] = mapped_column(DateTime())
    phone: Mapped[str] = mapped_column(String(14))
    cell: Mapped[str] = mapped_column(String(14))
    id_type: Mapped[str] = mapped_column(String(30), nullable=True)
    id_value: Mapped[str] = mapped_column(String(30), nullable=True)
    nationality: Mapped[str] = mapped_column(String(2))

    locations: Mapped[List["Location"]] = relationship(back_populates="user")
    pictures: Mapped[List["Picture"]] = relationship(back_populates="user")


class Location(Base):
    __tablename__ = "location"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    number: Mapped[int] = mapped_column(Integer())
    street: Mapped[str] = mapped_column(String(30))
    city: Mapped[str] = mapped_column(String(30))
    state: Mapped[str] = mapped_column(String(30))
    country: Mapped[str] = mapped_column(String(30))
    postcode: Mapped[str] = mapped_column(String(30))
    latitude: Mapped[float] = mapped_column(Float(precision=7))
    longitude: Mapped[float] = mapped_column(Float(precision=7))
    tz_offset: Mapped[str] = mapped_column(String(5))
    tz_desc: Mapped[str] = mapped_column(String(30))

    user: Mapped["User"] = relationship(back_populates="locations")


class Picture(Base):
    __tablename__ = "picture"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    large: Mapped[str] = mapped_column(String(255))
    medium: Mapped[str] = mapped_column(String(255))
    thumbnail: Mapped[str] = mapped_column(String(255))

    user: Mapped["User"] = relationship(back_populates="pictures")
