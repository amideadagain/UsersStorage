from sqlalchemy import Column, Integer, String, Date, Table
from datetime import date
from asyncpg.exceptions import UniqueViolationError

from src.db import db, metadata
from src.schema import UserInput, UserPatch
from src.utils.hashing import bcrypt


users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String, unique=True),
    Column("email", String, unique=True),
    Column("password", String),
    Column("register_date", Date),
)


class User:
    # @classmethod
    # async def username_exists(cls, username: str) -> bool:
    #     query = users.select().where(users.c.username == username)
    #     user = await db.fetch_one(query)
    #     if user:
    #         return True
    #     else:
    #         return False
    #
    # @classmethod
    # async def email_exists(cls, email: str) -> bool:
    #     query = users.select().where(users.c.email == email)
    #     user = await db.fetch_one(query)
    #     if user:
    #         return True
    #     else:
    #         return False

    @classmethod
    async def get(cls, user_id: int):
        query = users.select().where(users.c.id == user_id)
        user = await db.fetch_one(query)
        return user

    @classmethod
    async def create(cls, user: UserInput) -> dict:
        query = users.insert().values(
            username=user.username,
            email=user.email,
            password=bcrypt(user.password),
            register_date=date.today()
        )
        try:
            await db.execute(query)
        except UniqueViolationError:
            return {"message": "username or email already exists"}
        return {"message": "user created successfully"}

    @classmethod
    async def update(cls, user_id: int, user: UserPatch) -> dict:
        query = users.update().where(users.c.id == user_id).values(
            username=user.username,
            email=user.email,
            password=bcrypt(user.password),
            register_date=user.register_date
        )
        try:
            await db.execute(query)
        except UniqueViolationError:
            return {"message": "username or email already exists"}
        return {"message": "user data updated successfully"}

    @classmethod
    async def partial_update(cls, user_id: int, user: UserPatch) -> dict:
        to_update = user.dict(exclude_unset=True)
        if to_update.get('password'):
            to_update['password'] = bcrypt(user.password)
        # if to_update.get('username'):
        #     username_exists = await cls.username_exists(to_update['username'])
        #     if username_exists:
        #         return {"message": "username already exists"}
        # if to_update.get('email'):
        #     email_exists = await cls.email_exists(to_update['email'])
        #     if email_exists:
        #         return {"message": "email already exists"}

        query = users.update().where(users.c.id == user_id).values(**to_update)
        try:
            await db.execute(query)
        except UniqueViolationError:
            return {"message": "username or email already exists"}
        return {"message": "user data updated successfully"}

    @classmethod
    async def delete(cls, user_id: int) -> dict:
        query = users.select().where(users.c.id == user_id)
        user_ex = await db.fetch_one(query)
        if not user_ex:
            return {"message": "user doesn't exist, deletion aborted"}
        query = users.delete().where(users.c.id == user_id)
        await db.execute(query)
        return {"message": "user data deleted successfully"}

    @classmethod
    async def get_all(cls):
        query = users.select()
        user_list = await db.fetch_all(query)
        return user_list
