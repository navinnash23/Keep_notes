from datetime import datetime
from typing import List, Optional
from bson import ObjectId

from backend.app.models.user import PyObjectId
from .base import BaseRepository
from ...models.note import Note, NoteInDB, NoteCreate, NoteUpdate

class NotesRepository(BaseRepository[NoteInDB]):
    def __init__(self, db, collection_name: str = "notes"):
        super().__init__(db, NoteInDB, collection_name)

    async def get_user_notes(self, user_id: str) -> List[Note]:
        return await self.find_many({"user_id": user_id})

    async def create_note(self, note: NoteCreate, user_id: str) -> NoteCreate:
        note_data = note.model_dump()
        note_data.update({
            "user_id": user_id,  # Store as ObjectId in database
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        })
        # The base repository's create method will handle the model conversion
        return await self.create(note_data)

    async def update_note(self, note_id: str, note: NoteUpdate, user_id: str):
        update_data = note.model_dump(exclude_unset=True)
        update_data["updated_at"] = datetime.utcnow()
        
        existing_note = await self.find_one({
            "note_id": note_id,
            "user_id": user_id
        })
        
        if not existing_note:
            return None
            
        return await self.update(note_id, update_data)