"use client"
import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/lib/store';
import { Button } from '@/components/ui/button';
import { PlusCircle } from 'lucide-react';
import NotesList from '@/components/notes-list';
import { v4 as uuidv4 } from 'uuid';
import { Note } from '@/lib/store'; // Import the Note type

export default function Home() {
  const router = useRouter();
  const { user } = useAuth();
  const [notes, setNotes] = useState<Note[]>([]); // Explicitly set the type of notes as Note[]
  const [isLoading, setIsLoading] = useState(true); // Loading state

  useEffect(() => {
    if (!user) {
      router.push('/sign-in');
    }
  }, [user, router]);

  useEffect(() => {
    const fetchNotes = async () => {
      try {
        const token = localStorage.getItem('access_token');
        if (!token) {
          console.error('No access token found');
          return;
        }

        const response = await fetch('http://localhost:8000/api/v1/notes', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        });

        if (response.ok) {
          const fetchedNotes = await response.json();
          setNotes(fetchedNotes); // Store the fetched notes in state
        } else {
          console.error('Failed to fetch notes');
        }
      } catch (error) {
        console.error('Error fetching notes:', error);
      } finally {
        setIsLoading(false); // Stop loading
      }
    };

    fetchNotes();
  }, [user]); // Runs once when the component mounts

  // Handle editing and updating a note
  const handleUpdateNote = async (updatedNote: Note) => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(`http://localhost:8000/api/v1/notes/${updatedNote.note_id}`, {
        method: 'PUT', // Using PUT to update the note
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(updatedNote),
      });

      if (response.ok) {
        const updatedNoteData = await response.json();
        // Update the note in state dynamically
        setNotes((prevNotes) =>
          prevNotes.map((note) =>
            note.note_id === updatedNoteData.note_id ? updatedNoteData : note
          )
        );
      } else {
        console.error('Failed to update note');
      }
    } catch (error) {
      console.error('Error updating note:', error);
    }
  };

  const handleCreateNote = async () => {
    const newNote: Note = {
      note_id: uuidv4(), // Generate a unique note_id
      title: 'Untitled Note',
      content: '',
      createdAt: new Date().toISOString(), // Set the created date to current timestamp
      updatedAt: new Date().toISOString(),
    };

    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch('http://localhost:8000/api/v1/notes', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(newNote),
      });

      if (response.ok) {
        const createdNote = await response.json();
        setNotes((prevNotes) => [...prevNotes, createdNote]); // Add the new note to the state
      } else {
        console.error('Failed to create note');
      }
    } catch (error) {
      console.error('Error creating note:', error);
    }
  };

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold">My Notes</h1>
          <Button onClick={handleCreateNote}>
            <PlusCircle className="mr-2 h-4 w-4" />
            New Note
          </Button>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        <NotesList notes={notes} handleUpdateNote={handleUpdateNote} /> {/* Pass notes and update function to NotesList */}
      </main>
    </div>
  );
}
