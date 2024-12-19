from datetime import datetime
from typing import List
from bson import ObjectId
from .base import BaseRepository
from ...models.note import NoteInDB, NoteCreate, NoteUpdate

class NotesRepository(BaseRepository[NoteInDB]):
    async def get_user_notes(self, user_id: str) -> List[NoteInDB]:
        return await self.find_many({"user_id": ObjectId(user_id)})

    async def create_note(self, note: NoteCreate, user_id: str) -> NoteInDB:
        note_data = note.model_dump()
        note_data.update({
            "user_id": ObjectId(user_id),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        })
        return await self.create(note_data)

    async def update_note(self, note_id: str, note: NoteUpdate, user_id: str) -> NoteInDB:
        update_data = note.model_dump(exclude_unset=True)
        update_data["updated_at"] = datetime.utcnow()
        
        existing_note = await self.find_one({
            "_id": ObjectId(note_id),
            "user_id": ObjectId(user_id)
        })
        
        if not existing_note:
            return None
            
        return await self.update(note_id, update_data)