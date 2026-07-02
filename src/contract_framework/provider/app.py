"""Sample FastAPI provider whose compatibility is verified by Pact."""

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr

from contract_framework.provider import repository

app = FastAPI(title="User Provider", version="1.0.0")


class CreateUserRequest(BaseModel):
    name: str
    email: EmailStr


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_on: str


@app.get("/health", status_code=status.HTTP_200_OK)
def health() -> dict[str, str]:
    return {"status": "UP"}


@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int) -> dict[str, object]:
    user = repository.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(request: CreateUserRequest) -> dict[str, object]:
    return repository.create_user(name=request.name, email=str(request.email))
