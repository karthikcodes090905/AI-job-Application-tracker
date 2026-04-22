from fastapi import FastAPI
from pydantic import BaseModel
import re

app = FastAPI()

class QueryRequest(BaseModel):
    query: str
    assets: list[str] = []

@app.post("/solve")
def solve(request: QueryRequest):
    query = request.query.lower().strip()
    numbers = list(map(float, re.findall(r'-?\d+\.?\d*', query)))

    if len(numbers) < 2:
        return {"output": "I don't understand"}

    a, b = numbers[0], numbers[1]

    # Addition
    if any(word in query for word in ["add", "plus", "sum", "total", "together"]):
        result = a + b
        return {"output": f"The sum is {int(result) if result.is_integer() else result}."}

    # Subtraction
    if any(word in query for word in ["subtract", "minus", "difference", "less"]):
        if "from" in query:
            result = b - a
        else:
            result = a - b
        return {"output": f"The difference is {int(result) if result.is_integer() else result}."}

    # Multiplication
    if any(word in query for word in ["multiply", "times", "product", "multiplied by"]):
        result = a * b
        return {"output": f"The product is {int(result) if result.is_integer() else result}."}

    # Division
    if any(word in query for word in ["divide", "divided by", "quotient"]):
        try:
            result = a / b
            if result.is_integer():
                result = int(result)
        except ZeroDivisionError:
            return {"output": "The result is undefined."}
        return {"output": f"The result is {result}."}

    # Operator symbol fallback
    if "+" in query:
        result = a + b
        return {"output": f"The sum is {int(result) if result.is_integer() else result}."}
    if "-" in query:
        result = a - b
        return {"output": f"The difference is {int(result) if result.is_integer() else result}."}
    if "*" in query or "x" in query:
        result = a * b
        return {"output": f"The product is {int(result) if result.is_integer() else result}."}
    if "/" in query:
        try:
            result = a / b
            if result.is_integer():
                result = int(result)
        except ZeroDivisionError:
            return {"output": "The result is undefined."}
        return {"output": f"The result is {result}."}

    return {"output": "I don't understand"}
