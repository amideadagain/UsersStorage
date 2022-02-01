from datetime import date
from asyncpg.exceptions import UniqueViolationError

from src.models.user.models import users
from src.db import db
from src.models.user.schema import UserInput, UserPatch
from src.utils.hashing import bcrypt


class User:
    @classmethod
    async def get(cls, user_id: int):
        """
        Find user in db by id
        :param user_id: user id in db
        :return: id of created user, if not found return None
        """
        query = users.select().where(users.c.id == user_id)
        created_user_id = await db.fetch_one(query)
        return created_user_id

    @classmethod
    async def post(cls, user: UserInput) -> bool:
        """
        Create user in db
        :param user: User schema for input
        :return: if created return True, if username or email already exists False
        """
        query = users.insert().values(
            username=user.username,
            email=user.email,
            password=bcrypt(user.password),
            register_date=date.today()
        )
        try:
            await db.execute(query)
        except UniqueViolationError:
            return False
        return True

    @classmethod
    async def put(cls, user_id: int, user: UserPatch) -> bool:
        """
        Update user in db (PUT) by id
        :param user_id: user id in db
        :param user: User schema for update
        :return: if updated return True, if username or email already exists False
        !!! Does nothing if id is incorrect and returns True
        """
        query = users.update().where(users.c.id == user_id).values(
            username=user.username,
            email=user.email,
            password=bcrypt(user.password),
            register_date=user.register_date
        )
        try:
            await db.execute(query)
        except UniqueViolationError:
            return False
        return True

    @classmethod
    async def patch(cls, user_id: int, user: UserPatch) -> bool:
        """
        Update user in db with optional parameters (PATCH) by id
        :param user_id: user id in db
        :param user: User schema for update
        :return: if updated return True, if username or email already exists False
        !!! Does nothing if id is incorrect and returns True
        """
        to_update = user.dict(exclude_unset=True)
        if to_update.get('password'):
            to_update['password'] = bcrypt(user.password)

        query = users.update().where(users.c.id == user_id).values(**to_update)
        try:
            await db.execute(query)
        except UniqueViolationError:
            return False
        return True

    @classmethod
    async def delete(cls, user_id: int) -> bool:
        """
        Delete user from db by id
        :param user_id: user id in db
        :return: returns True
        !!! Does nothing if id is incorrect and returns True
        """
        query = users.delete().where(users.c.id == user_id)
        await db.execute(query)
        return True

    @classmethod
    async def get_list(cls):
        query = users.select()
        user_list = await db.fetch_all(query)
        return user_list
