"""
This module contains the FastAPI application with endpoints for 
status, greeting, and summing numbers
"""

from fastapi import FastAPI
from pydantic import BaseModel
from pathlib import Path

app = FastAPI(
    title="Simple FastAPI Server",
    description="A FastAPI server with status and greeting endpoints.",
    version="1.0.0"
)

@app.get("/status")
def get_status() -> dict:
    """Returns the server status."""
    return {"status": "OK"}

@app.get("/sayhi/{name}")
def say_hi(name: str) -> dict:
    """Greets the user with their provided name."""
    return {"message": f"Hi, {name}!"}

class SumRequest(BaseModel):
    """Request model for summing two numbers."""
    a: int
    b: int

@app.post("/sum")
def sum_numbers(data: SumRequest) -> dict:
    """Returns the sum of two numbers using a POST request."""
    return {"sum": data.a + data.b}

# Run as `fastapi run app.py`
@app.post("/write_sum")
def write_sum(data: SumRequest) -> dict:
    """Sums two numbers and writes the result to a file inside /app/data"""
    result = data.a + data.b
    output_path = Path("/app/data/output.txt")
    output_path.write_text(f"The sum of {data.a} and {data.b} is {result}\n")
    return {"message": "Sum written to output.txt", "sum": result}
