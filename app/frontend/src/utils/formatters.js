export const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes';

  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));

  return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
};

export const getFileExtension = (filename) => {
  return filename.slice(((filename.lastIndexOf('.') - 1) >>> 0) + 2);
};

export const getFileIcon = (filename) => {
  const ext = getFileExtension(filename).toLowerCase();

  const iconMap = {
    pdf: '📄',
    txt: '📝',
    doc: '📘',
    docx: '📘',
    csv: '📊',
    md: '📋',
    html: '🌐',
    htm: '🌐',
  };

  return iconMap[ext] || '📄';
};
