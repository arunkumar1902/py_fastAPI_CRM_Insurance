from pathlib import Path
import json
import aiofiles
from fastapi.encoders import jsonable_encoder

BASE_PATH = Path(__file__).resolve().parent.parent/"db"

async def read_data(file_name: str):
    file_path = BASE_PATH / file_name

    if not file_path.exists():
        return []

    async with aiofiles.open(file_path, "r") as file:
        content = await file.read()
        if not content.strip():
            return []
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return []

async def write_data(file_name:str, data):
    file_path = BASE_PATH / file_name

    json_compatible_data = jsonable_encoder(data)

    async with aiofiles.open(file_path,"w") as file:
        content = json.dumps(json_compatible_data, indent = 4)
        await file.write(content)
