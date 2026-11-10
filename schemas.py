from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
class RegisterIn(BaseModel):
    full_name: str = Field(min_length=2, max_length=150)
    email: str = Field(min_length=5, max_length=255)
    password: str = Field(min_length=8, max_length=128)
class LoginIn(BaseModel):
    email: str
    password: str
class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    full_name: str
    email: str
    role: str
    is_active: bool
class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut
class DocumentIn(BaseModel):
    title: str = Field(min_length=1, max_length=250)
    author: str = ""
    category: str = ""
    description: str = ""
    file_url: str = ""
    available_copies: int = Field(default=1, ge=0)
class DocumentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    author: str
    category: str
    description: str
    file_url: str
    available_copies: int
    created_at: datetime
class BorrowOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    document_id: int
    status: str
    requested_at: datetime
class BorrowStatusIn(BaseModel):
    status: str = Field(pattern="^(pending|approved|rejected|returned)$")
