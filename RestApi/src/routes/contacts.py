from typing import List
from sqlalchemy.orm import Session

from fastapi import Depends, HTTPException, Path, status, APIRouter
from fastapi_limiter.depends import RateLimiter
from src.database.db import get_db
from src.repository import contacts as repository_contacts
from src.database.models import Contact, User
from src.schemas import ContactModel, ContactResponse
from src.services.utils import next_seven_days
from src.services.auth import auth_service
from src.repository import contacts as repository_contacts

router = APIRouter(prefix="/contacts", tags= ["contacts"])


@router.get("/", response_model=List[ContactResponse],
            dependencies=[Depends(RateLimiter(times=3, seconds=10))])
async def read_contacts(db: Session = Depends(get_db),
                     current_user: User = Depends(auth_service.get_current_user)):
    """
    The read_contacts function returns a list of contacts for the current user.
    
    
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user from the database
    :return: A list of contacts
    :doc-author: Trelent
    """
    contacts = await repository_contacts.get_contacts(current_user, db)
    return contacts


@router.get("/birthday", response_model=List[ContactResponse], dependencies=[Depends(RateLimiter(times=3, seconds=10))], name="List of contacts")
async def get_contacts(db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_contacts function returns a list of contacts for the current user.
    
    :param db: Session: Get the database session
    :param current_user: User: Get the current user from the database
    :return: A list of contacts that are due in the next seven days
    :doc-author: Trelent
    """
    contacts = await repository_contacts.get_contacts(current_user, db)
    return next_seven_days(contacts)


@router.get("/{contact_id}", response_model=ContactResponse, dependencies=[Depends(RateLimiter(times=3, seconds=10))])
async def get_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_contact function returns a contact by id.
    
    :param contact_id: int: Get the contact id from the url
    :param db: Session: Access the database
    :param current_user: User: Get the user who is currently logged in
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await repository_contacts.get_contact_by_id(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")     
    return contact


@router.get("/first_name/{first_name}", response_model=ContactResponse, dependencies=[Depends(RateLimiter(times=3, seconds=10))])
async def get_contact_by_first_name(first_name: str, db: Session = Depends(get_db),
                                    current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_contact_by_first_name function returns a contact by first name.
        The function takes in the following parameters:
            - first_name: str, the first name of the contact to be returned.
            - db: Session = Depends(get_db), an instance of a database session that is used to query for contacts.  This parameter is optional and defaults to None if not provided when calling this function.  If no value is provided, then get_contact_by_first_name will use its own default value (Depends(get-db)).  
    
    :param first_name: str: Pass the first name of the contact to be searched
    :param db: Session: Get the database session
    :param current_user: User: Get the current user from the auth_service
    :return: A list of contacts that match the first name
    :doc-author: Trelent
    """
    contact = await repository_contacts.get_contact_first_name(first_name, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")     
    return contact


@router.get("/last_name/{last_name}", response_model=ContactResponse, dependencies=[Depends(RateLimiter(times=3, seconds=10))])
async def get_contact_by_last_name(last_name: str, db: Session = Depends(get_db),
                                   current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_contact_by_last_name function returns a contact by last name.
        The function takes in the last_name parameter and uses it to query the database for a contact with that last name.
        If no such contact exists, an HTTPException is raised indicating that no such resource was found.
    
    :param last_name: str: Specify the last name of the contact to be retrieved
    :param db: Session: Pass the database connection to the function
    :param current_user: User: Get the current user
    :return: The contact with the last name that is passed in as a parameter
    :doc-author: Trelent
    """
    contact = await repository_contacts.get_contact_last_name(last_name, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")     
    return contact


@router.get("/email/{email}", response_model=ContactResponse, dependencies=[Depends(RateLimiter(times=3, seconds=10))])
async def get_contact_by_email(email: str , db: Session = Depends(get_db), 
                               current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_contact_by_email function returns a contact by email.
        If the contact is not found, it raises an HTTPException with status code 404.
    
    
    :param email: str: Pass the email of the contact to be fetched
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user from the database
    :return: A contact by email
    :doc-author: Trelent
    """
    contact = await repository_contacts.get_contact_by_email(email, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")     
    return contact

@router.post("/", response_model=ContactResponse, dependencies=[Depends(RateLimiter(times=3, seconds=10))], status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactModel, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The create_contact function creates a new contact in the database.
    
    :param body: ContactModel: Get the data from the request body
    :param db: Session: Pass the database session to the repository layer
    :param current_user: User: Get the current user from the database
    :return: A contactmodel object
    :doc-author: Trelent
    """
    contact = await repository_contacts.get_contact_by_email(body.email, current_user, db)
    if contact:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail = 'Email is exist!')
    contact = await repository_contacts.create(body, current_user, db)
    return contact


@router.put("/{contact_id}", response_model=ContactResponse, dependencies=[Depends(RateLimiter(times=3, seconds=10))])
async def update_contact(body: ContactModel,contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The update_contact function updates a contact in the database.
        The function takes an id of the contact to be updated, and a body containing the new information for that contact.
        It returns an object with all of the information about that user.
    
    :param body: ContactModel: Get the data from the request body
    :param contact_id: int: Get the contact id from the url
    :param db: Session: Get a database session
    :param current_user: User: Get the current user and to check if they are authorized to delete a contact
    :return: A contactmodel object
    :doc-author: Trelent
    """
    contact = await repository_contacts.update(contact_id, body, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(RateLimiter(times=3, seconds=10))])
async def remove_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The remove_contact function removes a contact from the database.
        The function takes in an integer, which is the id of the contact to be removed.
        It also takes in a Session object and a User object as parameters, but these are not required by default.
    
    :param contact_id: int: Specify the path parameter
    :param db: Session: Access the database
    :param current_user: User: Get the user from the database
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await repository_contacts.remove(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contact