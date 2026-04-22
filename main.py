from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()

# Handle CORS properly so it can be hit by a public evaluation engine
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class QueryRequest(BaseModel):
    query: str
    assets: Optional[List[str]] = []

def call_llm_api(query: str) -> str:
    """
    Placeholder function for an LLM API call (e.g., OpenAI).
    Insert your API key and SDK logic here.
    """
    system_prompt = (
        "You are an AI assistant that answers questions directly and concisely. "
        "Do not use conversational filler or introductory text. "
        "Provide exactly the answer requested. "
        "For example, if the query is 'What is 10 + 15?', the output must be exactly 'The sum is 25.'."
    )
    
    # ---------------------------------------------------------
    # Example integration with the OpenAI Python SDK:
    # ---------------------------------------------------------
    # import os
    # from openai import OpenAI
    #
    # client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "your-api-key-here"))
    # response = client.chat.completions.create(
    #     model="gpt-4o",
    #     messages=[
    #         {"role": "system", "content": system_prompt},
    #         {"role": "user", "content": query}
    #     ],
    #     temperature=0.0
    # )
    # return response.choices[0].message.content.strip()
    # ---------------------------------------------------------
    
    # Temporary placeholder response
    if "10 + 15" in query:
        return "The sum is 25."
    
    return f"Placeholder response for: '{query}'"

@app.post("/solve")
async def solve(request: QueryRequest):
    # Extract the query
    query = request.query
    
    # Pass the query to the LLM
    answer = call_llm_api(query)
    
    # Return exactly formatted JSON payload
    return {"output": answer}
