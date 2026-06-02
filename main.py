from fastapi import FastAPI

app=FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"} 

@app.get("/name")
def read_name(name: str):
    return f"Hello, {name}!"  
# now using pydantic Models 

from pydantic import BaseModel,EmailStr
from typing import List

class User(BaseModel):
    id: int
    name: str
    age: int
    email: EmailStr
    interest: List[str]

class UserRecommendations(BaseModel):
    user_id: int
    recommendations: List[str]
    user: User

@app.post("/recommendations")
def get_recommendations(user: User):
    # Dummy recommendation logic based on user interests but save the data in the database
    recommendations = []
    if "technology" in user.interest:
        recommendations.append("Latest Tech Gadgets")
    if "sports" in user.interest:
        recommendations.append("Upcoming Sports Events")
    if "music" in user.interest:
        recommendations.append("Top Music Albums")
    print("User data received:", user)
    user_recommendations = UserRecommendations(
        user_id=user.id,
        recommendations=recommendations,
        user=user
    )
    return user_recommendations



    
