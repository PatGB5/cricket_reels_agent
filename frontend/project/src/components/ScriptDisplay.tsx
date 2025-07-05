import React from 'react';
import { Check, X, Copy, RefreshCw } from 'lucide-react';

interface ScriptDisplayProps {
  script: string;
  onAccept: () => void;
  onReject: () => void;
  isLoading?: boolean;
}

const ScriptDisplay: React.FC<ScriptDisplayProps> = ({ script, onAccept, onReject, isLoading = false }) => {
  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(script);
      // You could add a toast notification here
    } catch (err) {
      console.error('Failed to copy text: ', err);
    }
  };

  return (
    <div className="bg-white rounded-2xl shadow-xl p-8 max-w-4xl mx-auto">
      <div className="text-center mb-6">
        <h2 className="text-2xl font-bold text-gray-800">Generated Cricket Script</h2>
        <p className="text-gray-600 mt-2">Review your personalized cricket facts script</p>
      </div>

      <div className="bg-gradient-to-br from-gray-50 to-gray-100 rounded-xl p-6 mb-6 border border-gray-200">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-800">Your Script</h3>
          <button
            onClick={copyToClipboard}
            className="flex items-center gap-2 px-3 py-2 text-sm text-gray-600 hover:text-emerald-600 transition-colors duration-200"
          >
            <Copy className="w-4 h-4" />
            Copy
          </button>
        </div>
        <div className="prose prose-gray max-w-none">
          <p className="text-gray-700 leading-relaxed whitespace-pre-wrap font-medium">
            {script}
          </p>
        </div>
      </div>

      <div className="flex gap-4 justify-center">
        <button
          onClick={onReject}
          disabled={isLoading}
          className="flex items-center gap-2 px-6 py-3 bg-gray-100 text-gray-700 rounded-xl hover:bg-gray-200 transition-all duration-200 disabled:opacity-50"
        >
          <RefreshCw className="w-5 h-5" />
          Generate New Script
        </button>
        <button
          onClick={onAccept}
          disabled={isLoading}
          className="flex items-center gap-2 px-8 py-3 bg-gradient-to-r from-emerald-500 to-emerald-600 text-white rounded-xl hover:from-emerald-600 hover:to-emerald-700 transition-all duration-200 disabled:opacity-50 shadow-lg"
        >
          <Check className="w-5 h-5" />
          Accept & Continue
        </button>
      </div>
    </div>
  );
};

export default ScriptDisplay;