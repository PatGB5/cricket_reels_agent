import React, { useState, useRef } from 'react';
import { Upload, Video, X, CheckCircle } from 'lucide-react';

interface VideoUploadProps {
  onUpload: (file: File) => void;
  isLoading: boolean;
}

const VideoUpload: React.FC<VideoUploadProps> = ({ onUpload, isLoading }) => {
  const [dragOver, setDragOver] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      const file = files[0];
      if (file.type.startsWith('video/')) {
        setSelectedFile(file);
      }
    }
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      setSelectedFile(files[0]);
    }
  };

  const handleUpload = () => {
    if (selectedFile && !isLoading) {
      onUpload(selectedFile);
    }
  };

  const removeFile = () => {
    setSelectedFile(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <div className="bg-white rounded-2xl shadow-xl p-8 max-w-2xl mx-auto">
      <div className="text-center mb-6">
        <Video className="w-12 h-12 mx-auto mb-4 text-emerald-500" />
        <h2 className="text-2xl font-bold text-gray-800">Upload Your Video</h2>
        <p className="text-gray-600 mt-2">Upload the video you created using the generated script</p>
      </div>

      {!selectedFile ? (
        <div
          className={`
            border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-all duration-200
            ${dragOver ? 'border-emerald-400 bg-emerald-50' : 'border-gray-300 hover:border-emerald-400 hover:bg-emerald-50'}
          `}
          onDrop={handleDrop}
          onDragOver={(e) => {
            e.preventDefault();
            setDragOver(true);
          }}
          onDragLeave={() => setDragOver(false)}
          onClick={() => fileInputRef.current?.click()}
        >
          <Upload className={`w-12 h-12 mx-auto mb-4 ${dragOver ? 'text-emerald-500' : 'text-gray-400'}`} />
          <p className="text-lg font-medium text-gray-700 mb-2">
            Drop your video here or click to browse
          </p>
          <p className="text-sm text-gray-500">
            Supports MP4, MOV, AVI files up to 100MB
          </p>
        </div>
      ) : (
        <div className="bg-gradient-to-br from-emerald-50 to-blue-50 rounded-xl p-6 border border-emerald-200">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-3">
              <CheckCircle className="w-6 h-6 text-emerald-500" />
              <div>
                <p className="font-medium text-gray-800">{selectedFile.name}</p>
                <p className="text-sm text-gray-600">{formatFileSize(selectedFile.size)}</p>
              </div>
            </div>
            <button
              onClick={removeFile}
              className="p-2 text-gray-500 hover:text-red-500 transition-colors duration-200"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>
      )}

      <input
        ref={fileInputRef}
        type="file"
        accept="video/*"
        onChange={handleFileSelect}
        className="hidden"
      />

      {selectedFile && (
        <div className="mt-6">
          <button
            onClick={handleUpload}
            disabled={isLoading}
            className="w-full bg-gradient-to-r from-emerald-500 to-emerald-600 text-white py-4 px-6 rounded-xl font-semibold hover:from-emerald-600 hover:to-emerald-700 focus:ring-4 focus:ring-emerald-200 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-3"
          >
            {isLoading ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent"></div>
                Processing Video...
              </>
            ) : (
              <>
                <Upload className="w-5 h-5" />
                Upload & Process Video
              </>
            )}
          </button>
        </div>
      )}
    </div>
  );
};

export default VideoUpload;