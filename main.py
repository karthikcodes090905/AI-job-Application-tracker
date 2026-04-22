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
    numbers = list(map(int, re.findall(r'\d+', query)))

    if len(numbers) < 2:
        return {"output": "I don't understand"}

    # Addition
    if any(word in query for word in ["add", "plus", "sum", "total", "together"]):
        result = sum(numbers)
        return {"output": f"The sum is {result}."}

    # Subtraction
    if any(word in query for word in ["subtract", "minus", "difference", "less"]):
        if "from" in query:
            result = numbers[1] - numbers[0]
        else:
            result = numbers[0] - numbers[1]
        return {"output": f"The difference is {result}."}

    # Multiplication
    if any(word in query for word in ["multiply", "times", "product", "multiplied by"]):
        result = numbers[0] * numbers[1]
        return {"output": f"The product is {result}."}

    # Division
    if any(word in query for word in ["divide", "divided by", "quotient"]):
        try:
            result = numbers[0] / numbers[1]
            # Cast to int if result is whole number
            if result.is_integer():
                result = int(result)
        except ZeroDivisionError:
            return {"output": "The result is undefined."}
        return {"output": f"The result is {result}."}

    # Operator symbol fallback
    if "+" in query:
        result
