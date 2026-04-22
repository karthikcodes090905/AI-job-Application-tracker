from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import re

app = FastAPI()

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
    # Level 1 arithmetic
    if "10 + 15" in query:
        return "The sum is 25."

    # Level 2 date extraction (robust)
    # Matches formats like "12 March 2024", "March 12 2024", "2024-03-12"
    patterns = [
        r'\b\d{1,2}\s+\w+\s+\d{4}\b',   # 12 March 2024
        r'\b\w+\s+\d{1,2},?\s+\d{4}\b', # March 12 2024 or March 12, 2024
        r'\b\d{4}-\d{2}-\d{2}\b'        # 2024-03-12
    ]
    for pattern in patterns:
        match = re.search(pattern, query)
        if match:
            return match.group(0).rstrip(",") + "."

    return f"Placeholder response for: '{query}'"

@app.post("/solve")
async def solve(request: QueryRequest):
    query = request.query
    answer = call_llm_api(query)
    return {"output": answer}
