from fastapi import FastAPI
from pydantic import BaseModel
import re

# ✅ Define app FIRST
app = FastAPI()

# ✅ Request schema
class QueryRequest(BaseModel):
    query: str
    assets: list[str] = []

# ✅ API endpoint
@app.post("/solve")
def solve(request: QueryRequest):
    query = request.query.lower()

    numbers = list(map(int, re.findall(r'\d+', query)))

    if "sum" in query or "+" in query:
        if len(numbers) >= 2:
            result = sum(numbers)
            return {"output": f"The sum is {result}."}

    return {"output": "I don't understand"}