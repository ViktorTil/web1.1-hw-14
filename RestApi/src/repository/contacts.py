from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import and_

from src.database.models import Contact, User
from src.schemas import ContactModel


async def get_contacts(user: User, db: Session) -> List[Contact]:
    """
    Retrieves a list of contacts for a specific user.
    :param user: The user to retrieve contacts for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: A list of contacts.
    :rtype: List[Contact]
    """
    return db.query(Contact).filter(Contact.user_id == user.id).all()

async def get_contact_by_id(contact_id: int, user: User, db: Session) -> Contact | None:
    """
    Retrieves a single contact with the specified ID for a specific user.
    :param contact_id: The ID of the contact to retrieve.
    :type contact_id: int
    :param user: The user to retrieve the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The contact with the specified ID, or None if it does not exist.
    :rtype: Contact | None
    """   
    contact = db.query(Contact).filter_by(id=contact_id).first()
    return contact


async def get_contact_by_email(contact_email: str, user: User, db: Session) -> Contact | None:
    """
    Retrieves a single contact with the specified Email for a specific user.
    :param contact_email: The Email of the contact to retrieve.
    :type contact_email: str
    :param user: The user to retrieve the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The contact with the specified Email, or None if it does not exist.
    :rtype: Contact | None
    """
    contact = db.query(Contact).filter(and_(Contact.email==contact_email, Contact.user_id == user.id)).first()
    return contact


async def get_contact_first_name(first_name: str, user: User, db: Session) -> Contact | None:
    """
    Retrieves a single contact with the specified First Name for a specific user.
    :param first_name: The First Name of the contact to retrieve.
    :type first_name: str
    :param user: The user to retrieve the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The contact with the specified First Name, or None if it does not exist.
    :rtype: Contact | None
    """


    contact = db.query(Contact).filter_by(first_name=first_name).first()
    return contact


async def get_contact_last_name(last_name: str, user: User, db: Session) -> Contact | None:
    """
    Retrieves a single contact with the specified Last Name for a specific user.
    :param last_name: The Last Name of the contact to retrieve.
    :type last_name: str
    :param user: The user to retrieve the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The contact with the specified Last Name, or None if it does not exist.
    :rtype: Contact | None
    """

    contact = db.query(Contact).filter_by(last_name=last_name).first()
    return contact


async def create(body: ContactModel, user: User, db: Session) -> Contact:
    """
    Creates a new note for a specific user.

    :param body: The data for the contact to create.
    :type body: ContactModel
    :param user: The user to create the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The newly created contact.
    :rtype: Contact
    """
    contact = Contact(**body.model_dump(), user=user)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update(contact_id: int, body: ContactModel, user: User, db: Session) -> Contact | None:
    """
    Updates a single contact with the specified ID for a specific user.

    :param contact_id: The ID of the contact to update.
    :type contact_id: int
    :param body: The updated data for the contact.
    :type body: ContactModel
    :param user: The user to update the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The updated contact, or None if it does not exist.
    :rtype: Contact | None
    """
    contact = await get_contact_by_id(contact_id, user, db)
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone = body.phone
        contact.birthday = body.birthday
        db.commit()
    return contact


async def remove(contact_id: int, user: User, db: Session) -> Contact | None:
    """
    Removes a single contact with the specified ID for a specific user.

    :param contact_id: The ID of the contact to remove.
    :type contact_id: int
    :param user: The user to remove the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The removed contact, or None if it does not exist.
    :rtype: Contact | None
    """
    contact = await get_contact_by_id(contact_id, user, db)
    if contact:
       db.delete(contact)
       db.commit()
    return contact