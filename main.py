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

    import re
    numbers = list(map(int, re.findall(r'\d+', query)))

    if len(numbers) < 2:
        return {"output": "I don't understand"}

    # Default values
    a, b = numbers[0], numbers[1]

    # ➕ Addition
    if "sum" in query or "+" in query or "add" in query:
        return {"output": f"The sum is {a + b}."}

    # ➖ Subtraction (IMPORTANT FIX)
    elif "subtract" in query or "difference" in query or "-" in query:
        if "from" in query:
            # e.g. "subtract 5 from 20" → 20 - 5
            return {"output": f"The difference is {b - a}."}
        else:
            return {"output": f"The difference is {a - b}."}

    # ✖ Multiplication
    elif "multiply" in query or "product" in query or "*" in query:
        return {"output": f"The product is {a * b}."}

    # ➗ Division
    elif "divide" in query or "/" in query:
        if b == 0:
            return {"output": "Cannot divide by zero."}
        if "by" in query:
            # e.g. "divide 10 by 2" → 10 / 2
            return {"output": f"The result is {a / b}."}
        else:
            return {"output": f"The result is {a / b}."}

    return {"output": "I don't understand"}
