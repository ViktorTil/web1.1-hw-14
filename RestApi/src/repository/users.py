from typing import Union

from libgravatar import Gravatar
from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel


async def get_user_by_email(email: str, db: Session) -> User | None:
    """
    Retrieves a single user with the specified Email.
    
    :param email: The Email of the user to retrieve.
    :type email: str
    :param db: The database session.
    :type db: Session
    :return: The user with the specified Email, or None if it does not exist.
    :rtype: User | None
    """
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: Session) -> User:
    """
    Creates a new note for a specific user.

    :param body: The data for the user to create.
    :type body: UserModel
    :param db: The database session.
    :type db: Session
    :return: The newly created user.
    :rtype: User
    """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = User(**body.model_dump(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: Union[str, None], db: Session) -> None:
    """
    Update token for user.

    :param user: The user to update the token for.
    :type user: User
    :param token: New token for user
    :type token: Union[str, None]
    :param db: The database session.
    :type db: Session
    :return: The token was update, or None if it does not exist.
    :rtype: None
    """
    user.refresh_token = token
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:
    """
    Confirmed Email in database.
    
    :param email: The Email of the user to confirm.
    :type email: str
    :param db: The database session.
    :type db: Session
    :return: The Email was confirmed, or None if it does not exist.
    :rtype: None
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar(email: str, url: str, db: Session) -> User | None:
    """
    The update_avatar function updates the avatar of a single user with the specified Email.
    
    :param email: str: Specify the email of the user to update
    :param url: str: Specify the url of avatar to update
    :param db: Session: Pass the database session into the function
    :return: The updated user, or none if it does not exist
    :doc-author: Trelent
    """
    """
    Updates the avatar of a single user with the specified Email.

    :param email: The Email of the user to update avatar.
    :type email: str
    :param url: The URL of avatar to update.
    :type url str
    :param db: The database session.
    :type db: Session
    :return: The updated user, or None if it does not exist.
    :rtype: User | None
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user
