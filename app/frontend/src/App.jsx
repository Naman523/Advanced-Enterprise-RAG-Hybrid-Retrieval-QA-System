import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import ChatArea from './components/ChatArea';
import ThemeToggle from './components/ThemeToggle';
import { getInitialTheme, applyTheme } from './utils/theme';
import {
  askQuestion,
  uploadDocument,
  getDocuments,
  deleteDocument,
} from './services/api';

function App() {
  const [theme, setTheme] = useState(getInitialTheme());
  const [documents, setDocuments] = useState([]);
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [isDeleting, setIsDeleting] = useState(false);
  const [isMobileOpen, setIsMobileOpen] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    applyTheme(theme);
  }, [theme]);

  useEffect(() => {
    fetchDocuments();
  }, []);

  const toggleTheme = () => {
    setTheme((prev) => (prev === 'light' ? 'dark' : 'light'));
  };

  const fetchDocuments = async () => {
    try {
      const docs = await getDocuments();
      setDocuments(docs);
    } catch (err) {
      console.error('Failed to fetch documents:', err);
      showError('Failed to load documents');
    }
  };

  const handleUpload = async (file) => {
    setIsUploading(true);
    setUploadProgress(0);
    setError(null);

    try {
      await uploadDocument(file, (progress) => {
        setUploadProgress(progress);
      });

      await fetchDocuments();
      setUploadProgress(0);
    } catch (err) {
      console.error('Upload failed:', err);
      showError(
        err.response?.data?.detail || 'Failed to upload document. Please try again.'
      );
    } finally {
      setIsUploading(false);
    }
  };

  const handleDelete = async (filename) => {
    if (!confirm(`Delete "${filename}"?`)) return;

    setIsDeleting(true);
    setError(null);

    try {
      await deleteDocument(filename);
      await fetchDocuments();
    } catch (err) {
      console.error('Delete failed:', err);
      showError('Failed to delete document');
    } finally {
      setIsDeleting(false);
    }
  };

  const handleSendMessage = async (content) => {
    const userMessage = { role: 'user', content };
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);

    try {
      const response = await askQuestion(content);

      const aiMessage = {
        role: 'assistant',
        content: response.answer,
        sources: response.sources || [],
      };

      setMessages((prev) => [...prev, aiMessage]);
    } catch (err) {
      console.error('Question failed:', err);
      const errorMessage = {
        role: 'assistant',
        content:
          'Sorry, I encountered an error while processing your question. Please try again.',
        sources: [],
      };
      setMessages((prev) => [...prev, errorMessage]);
      showError('Failed to get answer');
    } finally {
      setIsLoading(false);
    }
  };

  const showError = (message) => {
    setError(message);
    setTimeout(() => setError(null), 5000);
  };

  return (
    <div className="flex h-screen overflow-hidden bg-gray-50 dark:bg-gray-900">
      <Sidebar
        documents={documents}
        onUpload={handleUpload}
        onDelete={handleDelete}
        isUploading={isUploading}
        uploadProgress={uploadProgress}
        isDeleting={isDeleting}
        isMobileOpen={isMobileOpen}
        onMobileClose={() => setIsMobileOpen(false)}
      />

      <div className="flex-1 flex flex-col">
        <header className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-4 py-3 flex items-center justify-between">
          <button
            onClick={() => setIsMobileOpen(true)}
            className="lg:hidden p-2 text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg"
          >
            <svg
              className="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M4 6h16M4 12h16M4 18h16"
              />
            </svg>
          </button>

          <div className="flex-1" />

          <ThemeToggle theme={theme} onToggle={toggleTheme} />
        </header>

        {error && (
          <div className="bg-red-50 dark:bg-red-900/20 border-l-4 border-red-500 px-4 py-3 mx-4 mt-4 rounded animate-slide-up">
            <div className="flex items-center gap-2">
              <svg
                className="w-5 h-5 text-red-500"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
              <p className="text-sm text-red-700 dark:text-red-300">{error}</p>
            </div>
          </div>
        )}

        <ChatArea
          messages={messages}
          onSendMessage={handleSendMessage}
          isLoading={isLoading}
          hasDocuments={documents.length > 0}
        />
      </div>
    </div>
  );
}

export default App;
