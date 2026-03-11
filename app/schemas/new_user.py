from pydantic import BaseModel, EmailStr, constr, field_validator
from datetime import date
import re

class PersonalDetails(BaseModel):
    customer_name : str
    gender: str
    date_of_birth : date
    email:EmailStr
    phone: str

    @field_validator("customer_name")
    @classmethod
    def name_validate(cls, value):
        if not isinstance(value, str):
            raise TypeError("Name must be in characters")
        if not re.fullmatch(r"[A-Za-z\s\-']{3,50}", value):
            raise ValueError("Name should contain at least 3 characters")
        return value

    @field_validator("date_of_birth")
    @classmethod
    def validate_dob(cls, value : date):
        if value > date.today():
            raise ValueError( "Invalid Date of birth")
        return value
    
    @field_validator("phone")
    @classmethod
    def phone_validate(cls, value):
        if not re.fullmatch("[6-9][0-9]{9}", value):
            raise ValueError("Phone Number must be valid 10 digits")
        return value
    
class Address(BaseModel):
    street: constr(min_length=2) # type: ignore
    city: str
    state: str
    pincode: str

    @field_validator("city", "state")
    @classmethod
    def address_validate(cls, value):
        if not re.fullmatch(r"[A-Za-z\s\-']{2,50}", value):
            raise ValueError("Should contains proper address details")
        return value

    @field_validator("pincode")
    @classmethod
    def pincode_validate(cls, value):
        if not re.fullmatch("[0-9]{6}", value):
            raise ValueError("Pincode should contain 6 digits")
        return value

class CustomerCreate(BaseModel):
    personal_details : PersonalDetails
    address: Address

class CustomerResponse(CustomerCreate):
    customer_id : str
    status : str
    account_created_on : date