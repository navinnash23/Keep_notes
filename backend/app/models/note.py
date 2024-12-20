from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from bson import ObjectId
from .user import PyObjectId

class NoteBase(BaseModel):
    title: str
    content: str
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )

class NoteCreate(NoteBase):
    pass
    note_id: str

class NoteUpdate(NoteBase):
    title: Optional[str] = None
    content: Optional[str] = None

class NoteInDB(NoteBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    note_id: str
    user_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )

    def to_response_model(self) -> 'Note':
        data = self.model_dump()
        # Fetch the user_id and save it as it is
        data['user_id'] = data['user_id']
        return Note(**data)

class Note(NoteBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    note_id: str
    user_id: str
    title: str
    content: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={ObjectId: str}
    )