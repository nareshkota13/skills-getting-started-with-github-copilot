"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Basketball": {
        "description": "Team sport focused on skill development and competitive play",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["james@mergington.edu"]
        },
        "Tennis Club": {
        "description": "Individual and doubles tennis training",
        "schedule": "Tuesdays and Thursdays, 3:45 PM - 5:00 PM",
        "max_participants": 10,
        "participants": ["sarah@mergington.edu"]
        },
        "Art Studio": {
        "description": "Painting, drawing, and sculpture techniques",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["isabella@mergington.edu", "lucas@mergington.edu"]
        },
        "Music Band": {
        "description": "Learn instruments and perform in school concerts",
        "schedule": "Thursdays, 3:30 PM - 4:45 PM",
        "max_participants": 25,
        "participants": ["noah@mergington.edu"]
        },
        "Debate Team": {
        "description": "Develop argumentation and public speaking skills",
        "schedule": "Mondays and Fridays, 3:45 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["ava@mergington.edu", "ethan@mergington.edu"]
        },
        "Science Club": {
        "description": "Hands-on experiments and STEM exploration",
        "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["mia@mergington.edu"]
        },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Add student
    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up for this activity")
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


# New endpoint to remove a participant from an activity
from fastapi import Body, Request

from fastapi import Body, Request, Form

@app.post("/activities/{activity_name}/unregister")
async def unregister_from_activity(activity_name: str, request: Request):
    """Unregister a student from an activity"""
    email = None
    # Try to get email from JSON body
    try:
        data = await request.json()
        email = data.get("email")
    except Exception:
        pass
    # If not JSON, try form
    if not email:
        form = await request.form() if request.headers.get("content-type", "").startswith("application/x-www-form-urlencoded") else None
        if form:
            email = form.get("email")
    # If still not found, try query param
    if not email:
        email = request.query_params.get("email")
    if not email:
        raise HTTPException(status_code=422, detail="Email is required")
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    activity = activities[activity_name]
    if email not in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student not registered for this activity")
    activity["participants"].remove(email)
    return {"message": f"Unregistered {email} from {activity_name}"}
