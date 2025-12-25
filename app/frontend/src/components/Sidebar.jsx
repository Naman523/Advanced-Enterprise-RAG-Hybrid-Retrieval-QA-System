import React from 'react';
import FileUpload from './FileUpload';
import DocumentList from './DocumentList';

const Sidebar = ({
  documents,
  onUpload,
  onDelete,
  isUploading,
  uploadProgress,
  isDeleting,
  isMobileOpen,
  onMobileClose,
}) => {
  return (
    <>
      {isMobileOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
          onClick={onMobileClose}
        />
      )}

      <aside
        className={`
          fixed lg:static inset-y-0 left-0 z-50
          w-80 bg-gray-100 dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700
          flex flex-col h-screen transition-transform duration-300
          ${isMobileOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
        `}
      >
        <div className="p-6 border-b border-gray-200 dark:border-gray-700">
          <div className="flex items-center justify-between mb-1">
            <h1 className="text-xl font-bold text-gray-900 dark:text-white">
              RAG Document Chat
            </h1>
            <button
              onClick={onMobileClose}
              className="lg:hidden p-2 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
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
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>
          </div>
          <p className="text-sm text-gray-600 dark:text-gray-400">
            Upload documents and ask questions
          </p>
        </div>

        <div className="p-4">
          <FileUpload
            onUpload={onUpload}
            isUploading={isUploading}
            uploadProgress={uploadProgress}
          />
        </div>

        <div className="flex-1 overflow-y-auto scrollbar-thin px-4 pb-4">
          <h2 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3">
            Documents ({documents.length})
          </h2>
          <DocumentList
            documents={documents}
            onDelete={onDelete}
            isDeleting={isDeleting}
          />
        </div>
      </aside>
    </>
  );
};

export default Sidebar;
