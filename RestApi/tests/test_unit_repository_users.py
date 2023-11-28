from datetime import datetime

import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session
from sqlalchemy import and_

from src.database.models import User
from src.schemas import UserModel
from src.repository.users import (
    get_user_by_email,
    create_user,
    update_token,
    confirmed_email,
    update_avatar
    )

class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.body = UserModel(
            username = "username",
            email = "example@mail.com", # EmailStr
            password = "password",
        )
        
        self.user = User(
            id = 1,
            username = "USERNAME",
            email = "test@example.com",
            password = "qwertyui",
            avatar = "string_avatar",
            refresh_token = "1234567890",
            confirmed = False,
        )
        self.new_avatar = "new_avatar"   
        self.new_token = "new_token"    
            
    async def test_create(self):
        result = await create_user(self.body, self.session)
        self.assertEqual(result.username, self.body.username)
        self.assertEqual(result.email, self.body.email)
        self.assertEqual(result.password, self.body.password)
        self.assertTrue(hasattr(result, 'id'))
        
    async def test_get_user_by_email(self):
        self.session.query(User).filter(User.email == self.user.email).first.return_value = self.user
        result = await get_user_by_email(self.user.email, self.session)
        self.assertEqual(result, self.user)

    async def test_confirm_email(self):
        self.session.query(User).filter(
            User.email == self.user.email).first.return_value = self.user
        await confirmed_email(self.user.email, self.session)
        self.assertTrue(self.user.confirmed)

    async def test_update_avatar(self):
        self.session.query(User).filter(
            User.email == self.user.email).first.return_value = self.user
        await update_avatar(email=self.user.email, url=self.new_avatar, db=self.session)
        self.assertEqual(self.user.avatar, self.new_avatar)


    async def test_update_token(self):
        self.session.query(User).filter(
            User.email == self.user.email).first.return_value = self.user
        await update_token(user=self.user, token=self.new_token, db=self.session)
        self.assertEqual(self.user.refresh_token, self.new_token)
        