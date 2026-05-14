from pydantic import BaseModel, constr, field_validator, EmailStr, PositiveFloat
from datetime import date
import re

class PolicyData(BaseModel):
    customer_id:str
    customer_name:str
    email:EmailStr
    policy_type:str
    provider:str
    premium_amount:PositiveFloat
    premium_frequency:str
    sum_assured:PositiveFloat
    payment_mode:str
    start_date: date
    end_date:date
    renewal_date:date
    status:str
    nominee_name:str
    nominee_relationship:str
    nominee_phone:str
    customer_notes:str

    @field_validator("policy_type", "provider", "nominee_name", "nominee_relationship", "customer_notes")
    def validate_str(cls, value):
        if len(value)<3:
            raise ValueError("Should Contain atleast 3 characters")
        return value

    @field_validator("end_date")
    def validate_end_date(cls, value, info):
        start_date = info.data.get("start_date")
        if start_date and value <= start_date :
            raise ValueError("End date should be after start date")
        return value
    
    @field_validator("renewal_date")
    def validate_renewal_date(cls, value, info):
        start_date = info.data.get("start_date")
        end_date = info.data.get("end_date")
        if start_date and value < start_date:
            raise ValueError("Renewal date should be after start date")
        if end_date and value > end_date:
            raise ValueError("Renewal date should be before end date")
        return value
    
    @field_validator("nominee_phone")
    @classmethod
    def phone_validate(cls, value):
        if not re.fullmatch("[6-9][0-9]{9}", value):
            raise ValueError("Phone Number must be valid 10 digits")
        return value
        
class PolicyResponse(PolicyData):
    policy_number : str
