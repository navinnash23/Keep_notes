'use client';

import { useEditor, EditorContent } from '@tiptap/react';
import StarterKit from '@tiptap/starter-kit';
import { Note } from '@/lib/store';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { useState } from 'react';

interface NoteEditorProps {
  note: Note;
  onClose: () => void;
}

export default function NoteEditor({ note, onClose }: NoteEditorProps) {
  const [title, setTitle] = useState(note.title);

  const editor = useEditor({
    extensions: [StarterKit],
    content: note.content,
    editorProps: {
      attributes: {
        class: 'prose prose-sm sm:prose lg:prose-lg xl:prose-2xl mx-auto focus:outline-none',
      },
    },
  });

  const handleSave = async () => {
    if (editor) {
      try {
        const token = localStorage.getItem('access_token');
        const response = await fetch(`http://localhost:8000/api/v1/notes/${note.id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
          body: JSON.stringify({
            title,
            content: editor.getHTML(),
            updatedAt: new Date().toISOString(),
          }),
        });

        if (response.ok) {
          const updatedNote = await response.json();
          // You can optionally update the local state if needed, or simply close the editor
          onClose();
        } else {
          console.error('Failed to update note');
        }
      } catch (error) {
        console.error('Error updating note:', error);
      }
    }
  };

  return (
    <div className="space-y-4">
      <Input
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="Note title"
        className="text-lg font-semibold"
      />
      <EditorContent editor={editor} className="min-h-[300px] border rounded-md p-4" />
      <div className="flex justify-end space-x-2">
        <Button variant="outline" onClick={onClose}>
          Cancel
        </Button>
        <Button onClick={handleSave}>Save</Button>
      </div>
    </div>
  );
}
