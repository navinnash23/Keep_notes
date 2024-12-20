'use client';

import { Note } from '@/lib/store';
import NoteCard from './note-card';

interface NotesListProps {
  notes: Note[];  // Accept notes as a prop
  handleUpdateNote: (updatedNote: Note) => void;  // Accept the update function as a prop
}

export default function NotesList({ notes, handleUpdateNote }: NotesListProps) {
  if (notes.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-muted-foreground">No notes yet. Create your first note!</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {notes.map((note) => (
        <NoteCard
          key={note.note_id}  // Use note.note_id as the unique key for each note
          note={note}  // Pass the entire note object, which includes note_id
          handleUpdateNote={handleUpdateNote}  // Pass the handleUpdateNote function
        />
      ))}
    </div>
  );
}
