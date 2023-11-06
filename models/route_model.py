
from typing import Literal, Optional
from pydantic import BaseModel, Field
from flask_openapi3 import FileStorage


class UserCreate(BaseModel):
    fullname: str
    username: str
    password: str # sha256 hash
    email: str
    mobile: str

class UserLogin(BaseModel):
    username: str
    password: str 

class UserModel(BaseModel):
    user_id: str

class UpdateProfile(BaseModel):
    user_id: str
    profile_id: str
    fullname: str
    mobile: str
    status: int = Field(0, description='0 for inactive, 1 for active')


# === Employee Related ====================
class EmpIdModel(BaseModel):
    emp_id: str
    user_id: str

class UploadModel(BaseModel):
    user_id: str
    emp_id: str
    file: FileStorage

class EmpCreate(BaseModel):
    user_id: str
    name: str
    designation: str

class EmpData(BaseModel):
    user_id: str
    emp_code: str
    name: str
    designation: str

class EmpUpdate(BaseModel):
    emp_id: str
    user_id: str
    name: str
    designation: str

class BasicQueryString(BaseModel):
    offset: int = Field(0, description='row offset')
    limit: int = Field(10, description='nos of rows to return')
    order_by: str = Field('id')
    order_direction: Literal['asc', 'desc'] = Field('desc')
    search_term: Optional[str] = Field(None)
    role: Optional[Literal["all","users","admin"]]
    status: Optional[Literal["all","activated","deactivated"]]