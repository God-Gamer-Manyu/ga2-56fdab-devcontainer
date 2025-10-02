from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import csv

app = FastAPI(title="Student Class API")

# Enable CORS for GET requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load CSV data into memory (runs once at startup)
students = []
with open("q-fastapi.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        students.append({
            "studentId": int(row["studentId"]),
            "class": row["class"]
        })

@app.get("/api")
def get_students(classes: Optional[List[str]] = Query(None, alias='class')):
    """
    Get all students or filter by class(es).
    - If no 'class' query params, returns all.
    - Supports multiple: ?class=1A&class=1B
    - Preserves original CSV order.
    """
    print(classes)
    if classes is None or len(classes) == 0:
        return {"students": students}
    else:
        filtered = [student for student in students if student["class"] in classes]
        return {"students": filtered}