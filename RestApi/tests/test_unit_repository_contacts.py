from datetime import datetime

import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session
from sqlalchemy import and_

from src.database.models import Contact, User
from src.schemas import ContactModel
from src.repository.contacts import (
    get_contacts,
    get_contact_by_id,
    get_contact_by_email,
    get_contact_first_name,
    get_contact_last_name,
    create,
    remove,
    update,
)


class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)
        self.contact = Contact(
            first_name = "first",
            last_name = "last",
            email =  "test@example.com",
            phone = "12345678901",
            birthday = datetime.now().date(),
            id = 1
                  )
        self.body = ContactModel(
            first_name="first1",
            last_name="last1",
            email="test1@example.com",
            phone="123456789012",
            birthday=datetime(year=2000, month=1, day=1).date()
        )

        
    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query(Contact).filter(user=self.user).all.return_value = contacts
        result = await get_contacts(user=self.user, db=self.session)
        self.assertEqual(result, contacts)
    
    async def test_get_contact_id(self):
        self.session.query(Contact).filter_by(id=self.contact.id).first.return_value = self.contact
        result = await get_contact_by_id(self.contact.id, self.user, self.session)
        self.assertEqual(result, self.contact)
        
    async def test_get_contact_email(self):
        self.session.query(Contact).filter(and_(
            Contact.email == self.contact.email, Contact.user_id == self.user.id)).first.return_value = self.contact
        result = await get_contact_by_email(self.contact.email, self.user, self.session)
        self.assertEqual(result, self.contact)
    
    async def test_get_contact_first_name(self):

        self.session.query(Contact).filter_by(Contact.first_name == self.contact.first_name).first.return_value = self.contact
        result = await get_contact_first_name(self.contact.first_name, self.user, self.session)
        self.assertEqual(result, self.contact)
        
    async def test_get_contact_last_name(self):
        self.session.query(Contact).filter_by(
            Contact.last_name == self.contact.last_name).first.return_value = self.contact
        result = await get_contact_last_name(self.contact.last_name, self.user, self.session)
        self.assertEqual(result, self.contact)
        
    async def test_create(self):
        result = await create(self.body, self.user, self.session)
        self.assertEqual(result.first_name, self.body.first_name)
        self.assertEqual(result.phone, self.body.phone)
        self.assertTrue(hasattr(result, 'id'))
        
    async def test_update(self):

        self.session.query().filter_by().first.return_value = self.contact

        await update(self.contact.id, self.body, self.user, self.session)

        self.assertEqual(self.body.first_name, self.contact.first_name)
        self.assertEqual(self.body.last_name, self.contact.last_name)
        self.assertEqual(self.body.phone, self.contact.phone)
        self.assertEqual(self.body.email, self.contact.email)
        self.assertEqual(self.body.birthday, self.contact.birthday)
        
    async def test_remove(self):
        self.session.query(Contact).filter_by(
            id=self.contact.id).first.return_value = self.contact
        result = await remove(self.contact.id, self.user, self.session) 
        self.assertEqual(result, self.contact)
 
