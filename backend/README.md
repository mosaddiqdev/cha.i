# Character AI Chat Backend

Backend API for a character-based AI chat application using Python, FastAPI, SQLite, and Google Gemini 2.5 Flash.

## Features

- 🤖 **5 Unique AI Characters** - Each with distinct personalities and expertise
- 💬 **Persistent Conversations** - SQLite database stores all chat history
- 🧠 **Smart Memory Management** - Context-aware responses using conversation history
- 🚀 **FastAPI** - Modern, fast, auto-documented API
- 🔥 **Gemini 2.5 Flash** - Leverages 1M token context window for rich conversations

## Characters

- **Mira** - The Emotional Companion (empathetic, caring, emotional support)
- **Ethan** - The Life Coach (motivational, disciplined, goal-oriented)
- **Kai** - The Tech Wizard (nerdy, helpful, programming expert)
- **Ivy** - The Creative Writing Partner (artistic, imaginative, creative)
- **Marcus** - The Fitness Coach (intense, disciplined, fitness-focused)

## Setup

### Prerequisites

- Python 3.11 or higher
- Google Gemini API key

### Installation

1. **Create virtual environment**

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Configure environment**

```bash
# Copy example env file
cp .env.example .env

# Edit .env and add your Gemini API key
# GEMINI_API_KEY=your_api_key_here
```

4. **Initialize database**

```bash
python data/seeds/seed_characters.py
```

### Running the Server

```bash
python run.py
```

Server will start on `http://localhost:8000`

- API Documentation: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/api/health`

## API Endpoints

### Characters

- `GET /api/characters` - List all characters
- `GET /api/characters/{id}` - Get character details

### Chat

- `POST /api/chat` - Send message to character
- `GET /api/conversations/{id}` - Get conversation history
- `GET /api/health` - Health check
- `GET /api/info` - API information

### Example Chat Request

```json
POST /api/chat
{
  "character_id": "mira",
  "message": "I've been feeling stressed lately",
  "conversation_id": null,
  "user_id": "user123"
}
```

## Project Structure

```
backend/
├── app/
│   ├── api/              # API routes
│   ├── characters/       # Character definitions
│   ├── core/             # Database & utilities
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic schemas
│   ├── services/         # Business logic
│   ├── config.py         # Configuration
│   └── main.py           # FastAPI app
├── data/                 # Database & seeds
├── tests/                # Test suite
├── requirements.txt      # Dependencies
└── run.py               # Dev server
```

## Development

### Database Migrations

Database is created automatically on first run. To reset:

```bash
# Delete database
rm data/chat.db

# Reinitialize
python data/seeds/seed_characters.py
```

### Adding New Characters

1. Create character profile in `app/characters/new_character.py`
2. Add to `ALL_CHARACTERS` dict in `app/characters/__init__.py`
3. Run seed script to update database

## Technologies

- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **Pydantic** - Data validation
- **Google Gemini** - AI model for character responses
- **SQLite** - Lightweight database
- **Uvicorn** - ASGI server

## License

MIT
