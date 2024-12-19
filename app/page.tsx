/* eslint-disable react-hooks/exhaustive-deps */
'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/lib/store';
import { Button } from '@/components/ui/button';
import { PlusCircle } from 'lucide-react';
import NotesList from '@/components/notes-list';
import { useNotes } from '@/lib/store';

export default function Home() {
  const router = useRouter();
  const { user } = useAuth();
  const { notes, addNote } = useNotes();

  useEffect(() => {
    if (!user) {
      router.push('/sign-in');
    } else {
      fetchNotes(); // Fetch notes on load
    }
  }, [user, router]);

  const fetchNotes = async () => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch('http://localhost:8000/api/v1/notes', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        addNote(data); // Add notes from API response
      } else {
        console.error('Failed to fetch notes');
      }
    } catch (error) {
      console.error('Error fetching notes:', error);
    }
  };

  const handleCreateNote = async () => {
    const newNote = {
      title: 'Untitled Note',
      content: '',
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
        addNote(createdNote); // Add the newly created note to the state
      } else {
        console.error('Failed to create note');
      }
    } catch (error) {
      console.error('Error creating note:', error);
    }
  };

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
        <NotesList
          notes={notes}
        />
      </main>
    </div>
  );
}
