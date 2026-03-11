from fastapi import APIRouter
from app.schemas.new_user import CustomerCreate, CustomerResponse
from app.utils.db_connect import read_data, write_data
from datetime import date
import uuid

router = APIRouter(prefix=("/user_details"), tags=["New User"])


@router.get("/")
async def get_user_details():
    return await read_data("customerDetails.json")

@router.post("/", response_model = CustomerResponse)
async def post_user_details(data : CustomerCreate):
    user_data = await read_data("customerDetails.json")
    new_user = {
        "customer_id": f"CUST-{uuid.uuid4().hex[:8].upper()}",
        "status" : "Active",
        "account_created_on": date.today(),
        **data.model_dump()
    }
    user_data.append(new_user)
    await write_data("customerDetails.json", user_data) 
    return new_user
    

