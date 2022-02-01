from fastapi import APIRouter

from src.models.user.crud import User as ModelUser
from src.models.user.schema import UserInput, UserView, UserPatch

router = APIRouter()


@router.post("/user/")
async def create_user(user: UserInput):
    response = await ModelUser.create(user)
    return response


@router.get("/user/{user_id}")
async def get_user(user_id: int):
    user = await ModelUser.get(user_id)
    if user:
        return UserView(**user).dict()
    else:
        return {"message": "user not found"}


@router.put("/user/{user_id}")
async def update_user(user_id: int, user: UserPatch):
    response = await ModelUser.update(user_id, user)
    return response


@router.patch("/user/{user_id}")
async def partially_update_user(user_id: int, user: UserPatch):
    response = await ModelUser.partial_update(user_id, user)
    return response


@router.delete("/user/{user_id}")
async def delete_user(user_id: int):
    response = await ModelUser.delete(user_id)
    return response


@router.get("/user-list/")
async def get_user_list():
    user_list = await ModelUser.get_all()
    return user_list
