
# Import necessary modules
from datetime import datetime, timedelta
from helpers.db_helper import SessionLocal
from models.route_model import UpdateProfile, UserCreate, UserLogin
import bcrypt

from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy import asc, desc 
import logging

import jwt

import os
from dotenv import load_dotenv
load_dotenv()

from models.db_model import User


# eaxmple of register new user
def register(userData: UserCreate, role: str = "users"):
    session = SessionLocal()
    try:
        hashed_password = bcrypt.hashpw(userData.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        user = User(fullname=userData.fullname, 
                    username=userData.username, 
                    password=hashed_password, 
                    email=userData.email, 
                    mobile=userData.mobile, 
                    role=role,
                    agree=1)
        session.add(user)
        session.commit()
        return True, user.id
    except IntegrityError as e:
        # Handle the IntegrityError here
        session.rollback()
        logging.error(f"Integrity Error: {e}")
        return False, 'Duplicate username'
    except Exception as e:
        session.rollback()
        logging.error(f"Exception: {e}")
        return False, 'Insertion failed'

# example of login user and create login token
def login(user: UserLogin):
    session = SessionLocal()

    user_record = session.query(User).filter((User.username == user.username) & (User.agree == 1)).first()
    if user_record is not None and bcrypt.checkpw(user.password.encode('utf-8'), user_record.password.encode('utf-8')):
        uDict = user_record.__dict__
        del uDict['password']
        del uDict['_sa_instance_state']

        token = jwt.encode({'public_id' : str(uDict['id']), 'exp' : datetime.utcnow() + timedelta(minutes=1440)}, os.getenv('APP_SECRET_KEY'), algorithm="HS256")
        if token is not None:
            uDict['login_token'] = token.decode('utf-8')
            uDict['login_token_date'] = datetime.utcnow()
            res = update_token(uDict['id'], uDict['login_token'], uDict['login_token_date'])
            if res > 0:
                return uDict
            
        return None
    else:
        return None
    
# example of read user data by user id
def getUser(user_id: int):
    try:
        session = SessionLocal()

        user_record = session.query(User).filter(User.id == user_id).first()
        uDict = user_record.__dict__
        del uDict['password']
        if 'login_token' in uDict:
            del uDict['login_token']
        if 'login_token_date' in uDict:
            del uDict['login_token_date']
        del uDict['_sa_instance_state']
        return uDict
    except Exception as e:
        logging.error(f"Exception: {e}")
        return None


# example of read user data by user id and role
def validate_user(id: int, role: str = "users"):
    try:
        session = SessionLocal()

        user_record = session.query(User).filter((User.id == id) & (User.role == role) & (User.agree == 1)).first()
        # add required logic to validate user
        return user_record is not None
    except Exception as e:
        logging.error(f"Exception: {e}")
        return False

# function to validate user token
def validateUserToken(user_id: int, token: str):

    session = SessionLocal()
    user_record = session.query(User).filter(User.id == user_id).first()
    
    if user_record is None:
        return False
    
    if user_record.login_token != token:
        return False
    
    current_time = datetime.utcnow()
    time_difference = current_time - user_record.login_token_date

    if time_difference < timedelta(minutes=1440):
        return True
    
    return False

# function to update user login token
def update_token(user_id: int, token: str, login_token_date: datetime):
    session = SessionLocal()
    try:
        user_record = session.query(User).filter(User.id == user_id).first()
        if user_record:
            user_record.login_token=token
            user_record.login_token_date=login_token_date
            session.commit()
            return True
    except Exception as e:
        session.rollback()
        logging.error(f"Exception: {e}")
        return False

# example of update user details
def update_details(userData: UpdateProfile):
    session = SessionLocal()
    try:
        user_record = session.query(User).filter(User.id == userData.profile_id).first()
        if user_record:
            user_record.fullname=userData.fullname, 
            user_record.mobile=userData.mobile, 
            user_record.agree=userData.status
            session.commit()
            return True, 'User record updated'
    except Exception as e:
        session.rollback()
        logging.error(f"Exception: {e}")
        return False, 'User record update failed'

# example of list all users with pagination
def list_users(role: str, status="all", offset: int = 0, limit: int = 10, order_by: str = None, order_direction: str = None, search_term: str = None):
    session = SessionLocal()

    p_res = session.query(User)

    if status is not None and status== "activated":
        p_res = p_res.filter(User.agree == 1)
    elif status is not None and status== "deactivated":
        p_res = p_res.filter(User.agree == 0)

    if role is not None and role!= "all":
        p_res = p_res.filter(User.role == role)

    if search_term:
        like_filter = or_(User.fullname.like(f'%{search_term}%'), User.username.like(f'%{search_term}%'), User.email.like(f'%{search_term}%'), User.mobile.like(f'%{search_term}%'))
        p_res = p_res.filter(like_filter)

    total_count = p_res.count()

    if order_direction == 'asc':
        p_res = p_res.order_by(asc(order_by))
    else:
        p_res = p_res.order_by(desc(order_by))

    p_res = p_res.offset(offset).limit(limit)
    p_res = p_res.all()
    return total_count, [{"id": usr.id, "fullname": usr.fullname, "username": usr.username, "email": usr.email, "mobile": usr.mobile, "created_date": usr.created, "agree": usr.agree} for usr in p_res]
