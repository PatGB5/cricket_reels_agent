import React from 'react';
import { AlertCircle, RefreshCw } from 'lucide-react';

interface ErrorMessageProps {
  message: string;
  onRetry?: () => void;
}

const ErrorMessage: React.FC<ErrorMessageProps> = ({ message, onRetry }) => {
  return (
    <div className="bg-white rounded-2xl shadow-xl p-8 max-w-2xl mx-auto">
      <div className="text-center">
        <div className="bg-red-100 rounded-full p-4 w-16 h-16 mx-auto mb-4">
          <AlertCircle className="w-8 h-8 text-red-500 mx-auto" />
        </div>
        <h2 className="text-2xl font-bold text-gray-800 mb-2">Oops! Something went wrong</h2>
        <p className="text-gray-600 mb-6">{message}</p>
        {onRetry && (
          <button
            onClick={onRetry}
            className="flex items-center justify-center gap-2 mx-auto px-6 py-3 bg-gradient-to-r from-emerald-500 to-emerald-600 text-white rounded-xl hover:from-emerald-600 hover:to-emerald-700 transition-all duration-200"
          >
            <RefreshCw className="w-5 h-5" />
            Try Again
          </button>
        )}
      </div>
    </div>
  );
};

export default ErrorMessage;