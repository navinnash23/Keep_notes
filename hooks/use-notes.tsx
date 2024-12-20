import { createContext, useContext, useState } from 'react';

// Define Note type
export interface Note {
  note_id: string;
  title: string;
  content: string;
  updatedAt: string;
}

// Notes context
const NotesContext = createContext<{
  notes: Note[];
  updateNote: (updatedNote: Note) => void;
  deleteNote: (noteId: string) => void;
}>({
  notes: [],
  updateNote: () => {},
  deleteNote: () => {},
});

// Provider component
export function NotesProvider({ children }: { children: React.ReactNode }) {
  const [notes, setNotes] = useState<Note[]>([]);

  // Function to update a note
  const updateNote = (updatedNote: Note) => {
    setNotes((prevNotes) =>
      prevNotes.map((note) =>
        note.note_id === updatedNote.note_id ? updatedNote : note
      )
    );
  };

  // Function to delete a note
  const deleteNote = (noteId: string) => {
    setNotes((prevNotes) =>
      prevNotes.filter((note) => note.note_id !== noteId)
    );
  };

  return (
    <NotesContext.Provider value={{ notes, updateNote, deleteNote }}>
      {children}
    </NotesContext.Provider>
  );
}

// Custom hook
export const useNotes = () => useContext(NotesContext);
