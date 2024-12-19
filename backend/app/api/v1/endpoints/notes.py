from typing import List
from fastapi import APIRouter, Depends

from backend.app.db.mongodb import get_database
from ....core.exceptions import NotFoundError
from ....models.note import Note, NoteCreate, NoteUpdate
from ....models.user import User
from ....db.repositories.notes import NotesRepository
from ...deps import get_current_user

router = APIRouter()

async def get_notes_repository():
    return NotesRepository(get_database(), Note, "notes")

@router.get("/", response_model=List[Note])
async def get_notes(
    current_user: User = Depends(get_current_user),
    notes_repo: NotesRepository = Depends(get_notes_repository)
):
    return await notes_repo.get_user_notes(current_user.id)

@router.post("/", response_model=Note)
async def create_note(
    note_in: NoteCreate,
    current_user: User = Depends(get_current_user),
    notes_repo: NotesRepository = Depends(get_notes_repository)
):
    return await notes_repo.create_note(note_in, current_user.id)

@router.put("/{note_id}", response_model=Note)
async def update_note(
    note_id: str,
    note_in: NoteUpdate,
    current_user: User = Depends(get_current_user),
    notes_repo: NotesRepository = Depends(get_notes_repository)
):
    updated_note = await notes_repo.update_note(note_id, note_in, current_user.id)
    if not updated_note:
        raise NotFoundError("Note not found")
    return updated_note

@router.delete("/{note_id}")
async def delete_note(
    note_id: str,
    current_user: User = Depends(get_current_user),
    notes_repo: NotesRepository = Depends(get_notes_repository)
):
    if not await notes_repo.delete(note_id):
        raise NotFoundError("Note not found")
    return {"message": "Note deleted successfully"}