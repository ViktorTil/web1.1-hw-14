from fastapi import APIRouter, Depends, status, UploadFile, File
from sqlalchemy.orm import Session
import cloudinary
import cloudinary.uploader

from src.database.db import get_db
from src.database.models import User
from src.repository import users as repository_users
from src.services.auth import auth_service
from src.conf.config import settings
from src.schemas import UserDb

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me/", response_model=UserDb)
async def read_users_me(current_user: User = Depends(auth_service.get_current_user)):
    """
    The read_users_me function is a GET request that returns the current user's information.
        The function takes in a parameter of the current_user, which is obtained from auth_service.get_current_user().
        This function will return an error if there is no logged in user.
    
    :param current_user: User: Get the current user from the database
    :return: The current user
    :doc-author: Trelent
    """
    return current_user


@router.patch('/avatar', response_model=UserDb)
async def update_avatar_user(file: UploadFile = File(), current_user: User = Depends(auth_service.get_current_user),
                             db: Session = Depends(get_db)):
    """
    The update_avatar_user function takes in a file, current_user, and db.
    It then uploads the file to cloudinary with the public id of Contacts/username.
    The function then returns a user object.
    
    :param file: UploadFile: Get the file from the request
    :param current_user: User: Get the current user from the database
    :param db: Session: Get the database session from the dependency
    :return: A user object, which is the updated user
    :doc-author: Trelent
    """
    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True
    )

    r = cloudinary.uploader.upload(
        file.file, public_id=f'Contacts/{current_user.username}', overwrite=True)
    src_url = cloudinary.CloudinaryImage(f'Contacts/{current_user.username}')\
                        .build_url(width=250, height=250, crop='fill', version=r.get('version'))
    user = await repository_users.update_avatar(current_user.email, src_url, db)
    return user
