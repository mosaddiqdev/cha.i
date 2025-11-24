<div align="center">

# cha.i

**AI Character Chat Application**

_Have meaningful conversations with AI personalities tailored to your needs_

![cha.i Showcase](./frontend/public/showcase.jpeg)

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![React](https://img.shields.io/badge/React-19-blue.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688.svg)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB.svg)](https://www.python.org/)

[Live Demo](https://cha-i.vercel.app/) • [Documentation](https://github.com/mosaddiqdev/cha.i#readme) • [Report Bug](https://github.com/mosaddiqdev/cha.i/issues) • [Request Feature](https://github.com/mosaddiqdev/cha.i/issues)

</div>

---

## 📖 About The Project

**cha.i** is a modern AI chat application featuring 5 unique AI characters, each with distinct personalities and expertise. Whether you need emotional support, fitness coaching, coding help, creative writing assistance, or life motivation, cha.i provides engaging, context-aware conversations powered by Google's Gemini 2.5 Flash.

### ✨ Key Features

- 🎭 **5 Unique AI Characters** - Mira, Ethan, Kai, Ivy, and Marcus
- 💬 **Persistent Conversations** - All chat history saved and retrievable
- 🧠 **Context-Aware Responses** - Leverages 1M token context window
- 🎨 **Premium Dark UI** - Minimalist, glassmorphic design
- 📱 **Fully Responsive** - Seamless experience on all devices
- 🔐 **User Authentication** - Secure login and registration
- 🚀 **Fast & Modern** - Built with React 19 and FastAPI

## 🎭 Meet The Characters

| Character  | Role                         | Personality                      | Best For                    |
| ---------- | ---------------------------- | -------------------------------- | --------------------------- |
| **Mira**   | The Emotional Companion      | Warm, caring, empathetic         | Emotional support, comfort  |
| **Ethan**  | The Life Coach               | Energetic, inspiring, motivating | Goal-setting, productivity  |
| **Kai**    | The Tech Wizard              | Nerdy, helpful, smart            | Programming, tech support   |
| **Ivy**    | The Creative Writing Partner | Dreamy, artistic, imaginative    | Writing, creativity         |
| **Marcus** | The Fitness Coach            | Intense, disciplined, confident  | Fitness, health, discipline |

## 🚀 Quick Start

### Prerequisites

- **Node.js** 18+
- **Python** 3.11+
- **Google Gemini API Key** ([Get one here](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/mosaddiqdev/cha.i.git
cd cha.i
```

2. **Set up the backend**

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# Initialize database
python data/seeds/seed_characters.py

# Start backend server
python run.py
```

Backend runs on `http://localhost:8000`

3. **Set up the frontend**

```bash
cd ../frontend
npm install

# Configure environment
cp .env.example .env
# Edit .env and set VITE_API_URL=http://localhost:8000

# Start frontend dev server
npm run dev
```

Frontend runs on `http://localhost:5173`

4. **Open your browser**

Navigate to `http://localhost:5173` and start chatting!

## 🏗️ Project Structure

```
cha.i/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/         # API routes
│   │   ├── characters/  # Character definitions
│   │   ├── models/      # Database models
│   │   ├── services/    # Business logic
│   │   └── main.py      # FastAPI app
│   ├── data/            # Database & seeds
│   └── requirements.txt
│
├── frontend/            # React frontend
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── pages/       # Page components
│   │   ├── services/    # API integration
│   │   └── context/     # React Context
│   ├── public/          # Static assets
│   └── package.json
│
└── README.md           # This file
```

## 🛠️ Tech Stack

### Frontend

- React 19
- Vite
- React Router
- Lucide Icons
- React Markdown

### Backend

- FastAPI
- SQLAlchemy
- Google Gemini 2.5 Flash
- SQLite
- Pydantic

## 📚 Documentation

- [Frontend Documentation](./frontend/README.md)
- [Backend Documentation](./backend/README.md)
- [API Documentation](http://localhost:8000/docs) (when backend is running)

## 🌐 API Endpoints

### Characters

- `GET /api/characters` - List all characters
- `GET /api/characters/{id}` - Get character details

### Chat

- `POST /api/chat` - Send message to character
- `GET /api/conversations/{id}` - Get conversation history

### Health

- `GET /api/health` - Health check
- `GET /api/info` - API information

## 🎨 Design Philosophy

cha.i follows a **minimal, premium dark aesthetic**:

- **Dark Mode First** - Optimized for reduced eye strain
- **Glassmorphism** - Subtle transparency and blur effects
- **Smooth Animations** - Polished micro-interactions
- **Typography** - Geist font family for modern readability
- **Minimal UI** - Clean, distraction-free interface

## 🤝 Contributing

Contributions are what make the open source community amazing! Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

## 📧 Contact

Project Link: [https://github.com/mosaddiqdev/cha.i](https://github.com/mosaddiqdev/cha.i)

Live Demo: [https://cha-i.vercel.app/](https://cha-i.vercel.app/)

## 🙏 Acknowledgments

- [Google Gemini](https://deepmind.google/technologies/gemini/) - AI model powering character responses
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [React](https://reactjs.org/) - UI library
- [Lucide Icons](https://lucide.dev/) - Beautiful icon set
- [Vite](https://vitejs.dev/) - Next generation frontend tooling

---

<div align="center">

**Built with ❤️ by the <a href="https://github.com/mosaddiqdev">cha.i team</a>**

[⬆ Back to Top](#chai)

</div>
