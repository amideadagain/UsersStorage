from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from src.models.user.crud import User as UserCrud
from src.models.user.schema import UserInput, UserView, UserPatch

router = APIRouter()


@router.post("/user/")
async def create_user(user: UserInput):
    user = await UserCrud.post(user)
    if user:
        return JSONResponse(content={"message": "user created successfully"},
                            status_code=status.HTTP_201_CREATED)
    else:
        return JSONResponse(content={"message": "username or email already taken"},
                            status_code=status.HTTP_409_CONFLICT)


@router.get("/user/{user_id}")
async def get_user(user_id: int):
    user = await UserCrud.get(user_id)
    if user:
        return UserView(**user).dict()
    else:
        return JSONResponse(content={"message": "user not found"},
                            status_code=status.HTTP_404_NOT_FOUND)


@router.put("/user/{user_id}")
async def update_user(user_id: int, user: UserPatch):
    user_exists = await UserCrud.get(user_id)
    if not user_exists:
        return JSONResponse(content={"message": "user not found"},
                            status_code=status.HTTP_404_NOT_FOUND)
    response = await UserCrud.put(user_id, user)
    if response:
        return {"message": "user data updated successfully"}
    return JSONResponse(content={"message": "username or email already taken"},
                        status_code=status.HTTP_409_CONFLICT)


@router.patch("/user/{user_id}")
async def partially_update_user(user_id: int, user: UserPatch):
    user_exists = await UserCrud.get(user_id)
    if not user_exists:
        return JSONResponse(content={"message": "user not found"},
                            status_code=status.HTTP_404_NOT_FOUND)
    response = await UserCrud.patch(user_id, user)
    if response:
        return {"message": "user data updated successfully"}
    return JSONResponse(content={"message": "username or email already taken"},
                        status_code=status.HTTP_409_CONFLICT)


@router.delete("/user/{user_id}")
async def delete_user(user_id: int):
    user_exists = await UserCrud.get(user_id)
    if not user_exists:
        return JSONResponse(content={"message": "user not found"},
                            status_code=status.HTTP_404_NOT_FOUND)
    await UserCrud.delete(user_id)
    return {"message": "user data deleted successfully"}


@router.get("/user-list/")
async def get_user_list():
    user_list = await UserCrud.get_list()
    return user_list
