import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';

const Message = ({ message }) => {
  const [showSources, setShowSources] = useState(false);
  const isUser = message.role === 'user';

  return (
    <div
      className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4 animate-fade-in`}
    >
      <div
        className={`max-w-3xl ${
          isUser
            ? 'bg-primary-600 text-white rounded-l-2xl rounded-tr-2xl'
            : 'bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 rounded-r-2xl rounded-tl-2xl shadow-md'
        } px-4 py-3`}
      >
        <div className="prose dark:prose-invert prose-sm max-w-none">
          {isUser ? (
            <p className="text-white m-0">{message.content}</p>
          ) : (
            <ReactMarkdown>{message.content}</ReactMarkdown>
          )}
        </div>

        {!isUser && message.sources && message.sources.length > 0 && (
          <div className="mt-3 pt-3 border-t border-gray-200 dark:border-gray-700">
            <button
              onClick={() => setShowSources(!showSources)}
              className="text-sm text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200 flex items-center gap-1"
            >
              <svg
                className={`w-4 h-4 transition-transform ${
                  showSources ? 'rotate-90' : ''
                }`}
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 5l7 7-7 7"
                />
              </svg>
              {showSources ? 'Hide' : 'Show'} sources ({message.sources.length})
            </button>

            {showSources && (
              <div className="mt-2 space-y-1 animate-slide-up">
                {message.sources.map((source, idx) => (
                  <div
                    key={idx}
                    className="text-xs text-gray-600 dark:text-gray-400 flex items-start gap-2"
                  >
                    <span className="text-primary-500 font-medium">
                      [{idx + 1}]
                    </span>
                    <span>
                      {source.source}
                      {source.page !== 'N/A' && `, page ${source.page}`}
                    </span>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default Message;
