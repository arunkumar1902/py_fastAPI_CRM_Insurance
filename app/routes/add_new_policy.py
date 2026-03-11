from fastapi import APIRouter
from app.schemas.new_policy import PolicyData, PolicyResponse
from app.utils.db_connect import read_data, write_data
from datetime import datetime

router = APIRouter(prefix="/policy_details", tags=["New Policy"])

async def get_policy_number():
    policies = await read_data("policies.json")
    if policies:
        last_number = int(policies[-1]["policy_number"].split("-")[-1])
    else:
        last_number = 0

    new_number = last_number+1
    today = datetime.now().strftime("%Y%m%d")
    return f"POL-{today}-{new_number:04d}"


@router.get("/")
async def get_policy_details():
    return await read_data("policies.json")

@router.post("/", response_model = PolicyResponse)
async def post_policy_data(data : PolicyData):
    policy_data = data.model_dump()
    policy_data["policy_number"] = await get_policy_number()

    policies = await read_data("policies.json")
    policies.append(policy_data)
    
    await write_data("policies.json", policies)
    return policy_data