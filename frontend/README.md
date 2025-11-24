# cha.i Frontend

Modern React frontend for cha.i - an AI character chat application with personality-driven conversations.

## ✨ Features

- 🎭 **5 Unique AI Characters** - Each with distinct personalities and visual design
- 💬 **Real-time Chat Interface** - Smooth, responsive messaging experience
- 🎨 **Premium Dark UI** - Minimalist design with glassmorphic elements
- 📱 **Fully Responsive** - Seamless experience across all devices
- 🔄 **Infinite Scroll** - Swipeable character carousel on homepage
- 🎯 **Scroll Indicators** - Minimal visual feedback for navigation
- 🔐 **Authentication** - Secure user login and registration

## 🚀 Tech Stack

- **React 19** - Latest React with modern hooks
- **Vite** - Lightning-fast build tool and dev server
- **React Router** - Client-side routing
- **Lucide React** - Beautiful icon library
- **React Markdown** - Markdown rendering for AI responses
- **CSS Variables** - Consistent design system

## 📋 Prerequisites

- Node.js 18+ or higher
- npm or yarn package manager
- Backend API running (see [backend README](../backend/README.md))

## 🛠️ Installation

1. **Navigate to frontend directory**

```bash
cd frontend
```

2. **Install dependencies**

```bash
npm install
```

3. **Configure environment**

```bash
# Copy example env file
cp .env.example .env

# Edit .env and set your backend API URL
# VITE_API_URL=http://localhost:8000
```

4. **Start development server**

```bash
npm run dev
```

Frontend will start on `http://localhost:5173`

## 📦 Available Scripts

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run ESLint
npm run lint
```

## 🏗️ Project Structure

```
frontend/
├── public/
│   ├── portraits/          # Character portrait images
│   └── showcase.jpeg       # App showcase image
├── src/
│   ├── components/         # Reusable React components
│   │   ├── ChatInterface.jsx
│   │   ├── ScrollIndicator.jsx
│   │   ├── Logo.jsx
│   │   └── ...
│   ├── context/           # React Context providers
│   │   └── AuthContext.jsx
│   ├── pages/             # Page components
│   │   ├── Home.jsx
│   │   ├── ChatInterface.jsx
│   │   └── AuthPage.jsx
│   ├── services/          # API service layer
│   │   └── api.js
│   ├── data/              # Static data
│   │   └── characters.js
│   ├── App.jsx            # Main app component
│   ├── main.jsx           # Entry point
│   └── index.css          # Global styles & design tokens
├── index.html
├── package.json
└── vite.config.js
```

## 🎨 Design System

The app uses CSS custom properties for consistent theming:

```css
/* Colors */
--color-bg-dark: #050505
--color-bg-card: #121212
--color-text-primary: #f5f5f5
--color-text-secondary: #737373
--color-accent-red: #ef4444

/* Spacing */
--spacing-xs to --spacing-2xl

/* Border Radius */
--radius-sm to --radius-full
```

## 🌐 Environment Variables

Create a `.env` file in the frontend directory:

```env
VITE_API_URL=http://localhost:8000
```

## 📱 Features Overview

### Character Carousel

- Horizontal scroll with snap points
- Infinite loop scrolling
- Minimal scroll indicators
- Smooth transitions

### Chat Interface

- Real-time messaging
- Markdown support for AI responses
- Syntax highlighting for code blocks
- Character-specific personalities
- Conversation persistence

### Authentication

- User registration and login
- Protected routes
- Session management
- Clean, minimal auth UI

## 🔗 API Integration

The frontend communicates with the backend API through the `services/api.js` module:

```javascript
import API from "./services/api";

// Get all characters
const characters = await API.characters.getAll();

// Send chat message
const response = await API.chat.send({
  character_id: "mira",
  message: "Hello!",
  user_id: "user123",
});
```

## 🚢 Deployment

### Build for Production

```bash
npm run build
```

The `dist/` folder will contain optimized production files.

### Deploy to Vercel

The project includes a `vercel.json` configuration:

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

MIT

---

Built with ❤️ using React and Vite
