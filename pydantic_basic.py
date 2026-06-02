from pydantic import BaseModel,EmailStr

class User(BaseModel):
    id: int
    name: str
    email: EmailStr

val_user = User(id="1", name="sneha", email="john.doe@example.com")
print(val_user)