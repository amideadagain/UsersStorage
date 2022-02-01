from datetime import date
from asyncpg.exceptions import UniqueViolationError

from src.models.user.models import users
from src.db import db
from src.models.user.schema import UserInput, UserPatch
from src.utils.hashing import bcrypt


class User:
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
