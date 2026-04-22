from fastapi import FastAPI
from pydantic import BaseModel
import re

app = FastAPI()

class QueryRequest(BaseModel):
    query: str
    assets: list[str] = []

@app.post("/solve")
def solve(request: QueryRequest):
    import re

    query = request.query.lower().strip()

    # Extract numbers (handles integers and decimals)
    numbers = list(map(float, re.findall(r'-?\d+\.?\d*', query)))

    if len(numbers) < 2:
        return {"output": "I don't understand"}

    a, b = numbers[0], numbers[1]

    # ---------------- ADDITION ----------------
    if any(word in query for word in ["add", "sum", "+", "plus"]):
        result = a + b
        return {"output": f"The sum is {int(result) if result.is_integer() else result}."}

    # ---------------- SUBTRACTION ----------------
    if any(word in query for word in ["subtract", "difference", "-", "minus"]):
        if "from" in query:
            result = b - a  # reverse order
        elif "between" in query:
            result = abs(a - b)
        else:
            result = a - b

        return {"output": f"The difference is {int(result) if result.is_integer() else result}."}

    # ---------------- MULTIPLICATION ----------------
    if any(word in query for word in ["multiply", "product", "*", "times", "into"]):
        result = a * b
        return {"output": f"The product is {int(result) if result.is_integer() else result}."}

    # ---------------- DIVISION ----------------
    if any(word in query for word in ["divide", "/", "by"]):
        if b == 0:
            return {"output": "Cannot divide by zero."}

        if "by" in query:
            result = a / b
        else:
            result = a / b

        return {"output": f"The result is {int(result) if result.is_integer() else result}."}

    return {"output": "I don't understand"}
