from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import re

app = FastAPI()

# Allow public evaluation engine to call your API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str
    assets: Optional[List[str]] = []

def call_llm_api(query: str) -> str:
    query_lower = query.lower()

    # ---------------------------------------------------------
    # Level 2: Date Extraction
    # ---------------------------------------------------------
    patterns = [
        r'\b\d{1,2}\s+[A-Za-z]+\s+\d{4}\b',   # 12 March 2024
        r'\b[A-Za-z]+\s+\d{1,2},?\s+\d{4}\b', # March 12 2024 / March 12, 2024
        r'\b\d{4}-\d{2}-\d{2}\b'              # 2024-03-12
    ]
    for pattern in patterns:
        match = re.search(pattern, query)
        if match:
            return match.group(0).rstrip(",") + "."

    # ---------------------------------------------------------
    # Level 1: Arithmetic
    # ---------------------------------------------------------
    numbers = list(map(int, re.findall(r'-?\d+', query)))
    if len(numbers) >= 2:
        a, b = numbers[0], numbers[1]
        if "sum" in query_lower or "+" in query_lower or "add" in query_lower:
            return f"The sum is {a + b}."
        elif "subtract" in query_lower or "difference" in query_lower or "-" in query_lower:
            if "from" in query_lower and query_lower.find(str(a)) > query_lower.find("from"):
                return f"The difference is {a - b}."
            elif "from" in query_lower:
                return f"The difference is {b - a}."
            else:
                return f"The difference is {a - b}."
        elif "multiply" in query_lower or "product" in query_lower or "*" in query_lower:
            return f"The product is {a * b}."
        elif "divide" in query_lower or "/" in query_lower:
            if b == 0:
                return "The result is undefined."
            result = a / b
            # Cast to int if whole number
            if result.is_integer():
                result = int(result)
            return f"The result is {result}."

    # ---------------------------------------------------------
    # Level 3: Number Properties (odd/even/prime)
    # ---------------------------------------------------------
    num_match = re.search(r'-?\d+', query_lower)
    if num_match:
        num = int(num_match.group(0))
        if "odd" in query_lower:
            return "YES." if num % 2 != 0 else "NO."
        elif "even" in query_lower:
            return "YES." if num % 2 == 0 else "NO."
        elif "prime" in query_lower:
            if num < 2:
                return "NO."
            is_prime = all(num % i for i in range(2, int(abs(num)**0.5) + 1))
            return "YES." if is_prime else "NO."

    # ---------------------------------------------------------
    # Fallback
    # ---------------------------------------------------------
    return "I don't understand the query."

@app.post("/solve")
async def solve(request: QueryRequest):
    query = request.query
    answer = call_llm_api(query)
    return {"output": answer}
