
# Import necessary modules
from helpers.db_helper import SessionLocal
from models.db_model import Employees, User
from models.route_model import EmpData, EmpUpdate

from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy import asc, desc 
import logging

from dotenv import load_dotenv
load_dotenv()


def create_employees(empData: EmpData):
    session = SessionLocal()
    try:
        user_record = session.query(User).filter(User.id == empData.user_id).first()
        if user_record:
            employees = Employees(user_id=int(empData.user_id), emp_code=empData.emp_code, name=empData.name, designation=empData.designation)
            session.add(employees)
            session.commit()
            return True, employees.id
        else:
            return False, 'User not found'
    except IntegrityError as e:
        # Handle the IntegrityError here
        session.rollback()
        logging.error(f"Integrity Error: {e}")
        return False, 'Duplicate employee code'
    except Exception as e:
        session.rollback()
        logging.error(f"Exception: {e}")
        return False, f"Exception: {e}"


def update_profile_image(pid: int, profile: any):
    session = SessionLocal()
    try:
        emp_record = session.query(Employees).filter(Employees.id == pid).first()
        if emp_record:
            emp_record.profile=profile
            session.commit()
            return True
    except Exception as e:
        session.rollback()
        logging.error(f"Exception: {e}")
        return False

def update_employee_data(emp: EmpUpdate):
    session = SessionLocal()
    try:

        emp_record = session.query(Employees).filter(Employees.id == emp.emp_id).first()
        if emp_record:
            emp_record.name=emp.name
            emp_record.designation=emp.designation

            session.commit()
            return True
    except Exception as e:
        session.rollback()
        logging.error(f"Exception: {e}")
        return False


def delete_employee(emp_id: int):
    session = SessionLocal()
    try:

        emp_record = session.query(Employees).filter(Employees.id == emp_id).first()
        if emp_record:
            session.delete(emp_record)
            session.commit()
            return True
    except Exception as e:
        session.rollback()
        logging.error(f"Exception: {e}")
        return False

def count_employees():
    session = SessionLocal()

    empCount = session.query(Employees).count()
    return empCount

def get_employee_by_code(emp_code: str):
    session = SessionLocal()

    emp_record = session.query(Employees).filter(Employees.emp_code == emp_code).first()
    if not emp_record:
        return None
    
    pDict = emp_record.__dict__
    del pDict['_sa_instance_state']
    return pDict

def get_employee(emp_id: int):
    session = SessionLocal()

    emp_record = session.query(Employees).filter(Employees.id == emp_id).first()
    if not emp_record:
        return None
    
    pDict = emp_record.__dict__
    del pDict['_sa_instance_state']
    return pDict

def list_employees(user_id: int, offset: int = 0, limit: int = 10, order_by: str = None, order_direction: str = None, search_term: str = None):
    session = SessionLocal()

    emp_res = session.query(Employees).filter(Employees.user_id == user_id)

    if search_term:
        like_filter = or_(Employees.name.like(f'%{search_term}%'), Employees.designation.like(f'%{search_term}%'))
        emp_res = emp_res.filter(like_filter)

    total_count = emp_res.count()

    if order_direction == 'asc':
        emp_res = emp_res.order_by(asc(order_by))
    else:
        emp_res = emp_res.order_by(desc(order_by))

    emp_res = emp_res.offset(offset).limit(limit)
    emp_res = emp_res.all()
    return total_count, [{"id": emp.id, "code": emp.emp_code, "name": emp.name, "designation": emp.designation, "profile_image": emp.profile, "created_date": emp.created} for emp in emp_res]
