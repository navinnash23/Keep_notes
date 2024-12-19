# Notes App Frontend
This is the frontend of the application
## Setup
1.Install dependencies
```bash
npm install
```
2.Run the development server
```bash
npx next dev
```
The development server will start at 'http://localhost:3000'

# Notes App Backend

This is the backend service for the Notes application built with FastAPI and MongoDB.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows:
  ```bash
  .\venv\Scripts\activate
  ```
- Unix/MacOS:
  ```bash
  source venv/bin/activate
  ```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
- Copy `.env.example` to `.env`
- Update the MongoDB connection string and other variables

## Running the Server

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The server will start at `http://localhost:8000`

## API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Authentication
- POST `/api/v1/auth/register` - Register a new user
- POST `/api/v1/auth/login` - Login and get access token

### Notes
- GET `/api/v1/notes` - Get all notes for current user
- POST `/api/v1/notes` - Create a new note
- PUT `/api/v1/notes/{note_id}` - Update a note
- DELETE `/api/v1/notes/{note_id}` - Delete a note
