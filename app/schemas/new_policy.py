from pydantic import BaseModel, constr, field_validator, EmailStr
from datetime import date

class PolicyData(BaseModel):
    customer_id:str
    customer_name:str
    email:EmailStr
    policy_type:constr(min_length=3) # type: ignore
    provider:constr(min_length=3) # type: ignore
    premium_amount:float
    premium_frequency:constr(min_length=3) # type: ignore
    sum_assured:float
    payment_mode:constr(min_length=3) # type: ignore
    start_date: date
    end_date:date
    renewal_date:date
    status:constr(min_length=3) # type: ignore
    nominee_name:constr(min_length=3) # type: ignore
    nominee_relationship:constr(min_length=3) # type: ignore
    nominee_phone:constr(pattern="^([6-9][0-9]{9})$") # type: ignore
    customer_notes:constr(min_length=3) # type: ignore

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
        
class PolicyResponse(PolicyData):
    policy_number : str
