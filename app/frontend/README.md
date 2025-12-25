# RAG Document Chat - Frontend

A modern, production-ready React frontend for the RAG Document Chat application. Built with Vite, React, and Tailwind CSS.

## Features

- Clean, intuitive chat interface
- Drag-and-drop document upload
- Document management (upload, list, delete)
- Real-time chat with AI responses
- Markdown rendering for AI answers
- Collapsible source context display
- Light/Dark mode toggle
- Fully responsive design
- Smooth animations and transitions
- Upload progress indicator
- Error handling with user-friendly messages

## Tech Stack

- **React 18** - UI framework
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Styling
- **Axios** - HTTP client
- **React Markdown** - Markdown rendering

## Prerequisites

- Node.js 16+ and npm
- Backend server running on http://localhost:8000

## Installation

1. Navigate to the frontend directory:
```bash
cd app/frontend
```

2. Install dependencies:
```bash
npm install
```

3. Configure environment variables:
```bash
cp .env.example .env
```

Edit `.env` if your backend runs on a different URL:
```env
VITE_API_BASE_URL=http://localhost:8000
```

## Running the Application

Start the development server:
```bash
npm run dev
```

The app will be available at http://localhost:3000

## Building for Production

Build the production bundle:
```bash
npm run build
```

Preview the production build:
```bash
npm run preview
```

## Project Structure

```
app/frontend/
├── src/
│   ├── components/         # React components
│   │   ├── ChatArea.jsx   # Main chat interface
│   │   ├── Sidebar.jsx    # Document management sidebar
│   │   ├── Message.jsx    # Chat message component
│   │   ├── FileUpload.jsx # Drag-and-drop upload
│   │   ├── DocumentList.jsx
│   │   └── ThemeToggle.jsx
│   ├── services/          # API integration
│   │   └── api.js         # Backend API calls
│   ├── utils/             # Utility functions
│   │   ├── theme.js       # Theme management
│   │   └── formatters.js  # File formatting helpers
│   ├── App.jsx            # Main app component
│   ├── main.jsx           # App entry point
│   └── index.css          # Global styles
├── index.html
├── package.json
├── vite.config.js
├── tailwind.config.js
└── postcss.config.js
```

## Features Guide

### Document Upload
- Click the upload area or drag and drop files
- Supported formats: PDF, TXT, CSV, DOC, DOCX, MD, HTML
- Progress indicator during upload
- Automatic document list refresh

### Chat Interface
- Type questions in the input box
- Press Enter to send (Shift+Enter for new line)
- AI responses rendered in Markdown
- Click "Show sources" to view document references

### Theme Toggle
- Click sun/moon icon in top right
- Automatic system theme detection
- Preference saved to localStorage

### Document Management
- View all uploaded documents in sidebar
- Hover over document to see delete button
- Confirmation required before deletion

## API Integration

The frontend communicates with the backend via these endpoints:

- `GET /ask?q={question}` - Ask questions
- `POST /upload` - Upload documents
- `GET /documents` - List documents
- `DELETE /documents/{filename}` - Delete documents

## Customization

### Colors
Edit `tailwind.config.js` to customize the color scheme:
```js
theme: {
  extend: {
    colors: {
      primary: {
        // Your custom colors
      }
    }
  }
}
```

### API URL
Update `.env` to point to a different backend:
```env
VITE_API_BASE_URL=https://your-api.com
```

## Troubleshooting

### CORS Errors
Ensure the backend has CORS enabled for your frontend URL.

### Connection Refused
Verify the backend is running on the URL specified in `.env`.

### Upload Fails
Check file size limits and supported file formats.

## Browser Support

- Chrome/Edge (latest 2 versions)
- Firefox (latest 2 versions)
- Safari (latest 2 versions)

## License

MIT
