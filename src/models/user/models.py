from sqlalchemy import Column, Integer, String, Date, Table

from src.db import metadata


users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String, unique=True),
    Column("email", String, unique=True),
    Column("password", String),
    Column("register_date", Date),
)
