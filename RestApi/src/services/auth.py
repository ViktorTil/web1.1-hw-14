from datetime import datetime, timedelta
from typing import Optional

import redis
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.repository import users as repository_users
from src.conf.config import settings

class Auth:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SECRET_KEY = settings.secret_key
    #settings.secret_key
    ALGORITHM = settings.algorithm
    #"secret_key"
    #ALGORITHM = "HS256"
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
    r = redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0)

    def verify_password(self, plain_password, hashed_password):
        """
        The verify_password function takes a plain-text password and hashes it
        using the same salt that was used to hash the original password. If the two
        hashes match, then we know that the user entered in their correct password.
        
        :param self: Represent the instance of the class
        :param plain_password: Get the password from the user
        :param hashed_password: Check if the password is correct
        :return: A boolean value
        :doc-author: Trelent
        """
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str):
        """
        The get_password_hash function takes a password and returns the hashed version of it.
        The hashing algorithm is defined in the settings file.
        
        :param self: Represent the instance of the class
        :param password: str: Pass in the password that is to be hashed
        :return: A hashed password
        :doc-author: Trelent
        """
        return self.pwd_context.hash(password)

    # define a function to generate a new access token
    async def create_access_token(self, data: dict, expires_delta: Optional[float] = None):
        """
        The create_access_token function creates a new access token.
            The function takes in the data to be encoded, and an optional expires_delta parameter.
            If no expires_delta is provided, the default value of 150 minutes will be used.
        
        :param self: Refer to the current instance of a class
        :param data: dict: Pass in the data that will be encoded into the jwt
        :param expires_delta: Optional[float]: Set the expiration time of the token
        :return: A jwt token
        :doc-author: Trelent
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(minutes=150)
        to_encode.update(
            {"iat": datetime.utcnow(), "exp": expire, "scope": "access_token"})
        encoded_access_token = jwt.encode(
            to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_access_token

    # define a function to generate a new refresh token
    async def create_refresh_token(self, data: dict, expires_delta: Optional[float] = None):
        """
        The create_refresh_token function creates a refresh token for the user.
            The function takes in two arguments: data and expires_delta. Data is a dictionary containing the user's id, username, email address, and password hash. Expires_delta is an optional argument that sets how long the refresh token will be valid for (defaults to 7 days).
            The function then encodes this information into JSON Web Tokens using PyJWT.
        
        :param self: Represent the instance of a class
        :param data: dict: Pass the user's id to the function
        :param expires_delta: Optional[float]: Set the expiration time for the refresh token
        :return: A jwt token that is encoded with the user's data and an expiration date
        :doc-author: Trelent
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update(
            {"iat": datetime.utcnow(), "exp": expire, "scope": "refresh_token"})
        encoded_refresh_token = jwt.encode(
            to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_refresh_token

    async def decode_refresh_token(self, refresh_token: str):
        """
        The decode_refresh_token function is used to decode the refresh token.
            The function takes in a refresh_token as an argument and returns the email of the user if successful.
            If not, it raises an HTTPException with status code 401 (Unauthorized) and detail 'Invalid scope for token'.
        
        
        :param self: Represent the instance of the class
        :param refresh_token: str: Pass the refresh token to the function
        :return: The email of the user, which is stored in the sub claim
        :doc-author: Trelent
        """
        try:
            payload = jwt.decode(
                refresh_token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload['scope'] == 'refresh_token':
                email = payload['sub']
                return email
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid scope for token')
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate credentials')

    async def get_current_user(self, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
        """
        The get_current_user function is a dependency that will be used in the
            protected endpoints. It takes a token as an argument and returns the user
            if it's valid, or raises an exception otherwise.
        
        :param self: Access the class variables
        :param token: str: Get the token from the request header
        :param db: Session: Get the database session
        :return: A user object
        :doc-author: Trelent
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            # Decode JWT
            payload = jwt.decode(token, self.SECRET_KEY,
                                 algorithms=[self.ALGORITHM])
            if payload['scope'] == 'access_token':
                email = payload["sub"]
                if email is None:
                    raise credentials_exception
            else:
                raise credentials_exception
        except JWTError as e:
            raise credentials_exception

        user = await repository_users.get_user_by_email(email, db)
        if user is None:
            raise credentials_exception
        return user

    def create_email_token(self, data: dict):
        """
        The create_email_token function creates a token that is used to verify the user's email address.
        The token contains the following information:
            - iat (issued at): The time when the token was created.
            - exp (expiration): The time when this token will expire, which is 7 days from now.
            - scope: This indicates what type of action can be performed with this particular JWT.
        
        :param self: Make the function a method of the user class
        :param data: dict: Pass the data that will be encoded in the token
        :return: A token that is used to verify the user's email address
        :doc-author: Trelent
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update(
            {"iat": datetime.utcnow(), "exp": expire, "scope": "email_token"})
        token = jwt.encode(to_encode, self.SECRET_KEY,
                           algorithm=self.ALGORITHM)
        return token

    def get_email_from_token(self, token: str):
        """
        The get_email_from_token function takes a token as an argument and returns the email address associated with that token.
        The function first tries to decode the JWT using the SECRET_KEY and ALGORITHM defined in settings.py, then checks if 
        the scope of this payload is 'email_token'. If it is, it returns the email address associated with this payload.
        
        :param self: Represent the instance of the class
        :param token: str: Pass in the token that was sent to the user's email
        :return: The email address of the user who requested the password reset
        :doc-author: Trelent
        """
        try:
            payload = jwt.decode(token, self.SECRET_KEY,
                                 algorithms=[self.ALGORITHM])

            if payload['scope'] == 'email_token':
                email = payload["sub"]
                return email
        except JWTError as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail="Invalid token for email verification")
auth_service = Auth()
