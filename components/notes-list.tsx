'use client';

import { Note } from '@/lib/store';
import NoteCard from './note-card';

interface NotesListProps {
  notes: Note[];
}

export default function NotesList({
  notes,
}: NotesListProps) {
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
          key={note.id}
          note={note}
        />
      ))}
    </div>
  );
}
