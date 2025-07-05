import React, { useState } from 'react';
import { Send, Sparkles } from 'lucide-react';

interface PromptInputProps {
  onSubmit: (prompt: string) => void;
  isLoading: boolean;
}

const PromptInput: React.FC<PromptInputProps> = ({ onSubmit, isLoading }) => {
  const [prompt, setPrompt] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (prompt.trim() && !isLoading) {
      onSubmit(prompt.trim());
    }
  };

  const examples = [
    "Focus on T20 World Cup statistics",
    "Include facts about Indian cricket legends",
    "Emphasize recent IPL records",
    "Highlight women's cricket achievements"
  ];

  return (
    <div className="bg-white rounded-2xl shadow-xl p-8 max-w-2xl mx-auto">
      <div className="text-center mb-8">
        <div className="bg-gradient-to-r from-emerald-400 to-blue-500 bg-clip-text text-transparent">
          <Sparkles className="w-8 h-8 mx-auto mb-4 text-emerald-500" />
          <h2 className="text-2xl font-bold text-gray-800">Create Your Cricket Fact Reel</h2>
        </div>
        <p className="text-gray-600 mt-2">Add your preferences to personalize the daily cricket facts</p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label htmlFor="prompt" className="block text-sm font-medium text-gray-700 mb-3">
            Additional Prompt (Optional)
          </label>
          <textarea
            id="prompt"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="e.g., Include recent IPL statistics, focus on spin bowling records..."
            className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all duration-200 resize-none"
            rows={4}
          />
        </div>

        <div className="bg-gray-50 rounded-xl p-4">
          <p className="text-sm font-medium text-gray-700 mb-3">Quick Examples:</p>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
            {examples.map((example, index) => (
              <button
                key={index}
                type="button"
                onClick={() => setPrompt(example)}
                className="text-left p-3 bg-white rounded-lg border border-gray-200 hover:border-emerald-300 hover:bg-emerald-50 transition-all duration-200 text-sm"
              >
                {example}
              </button>
            ))}
          </div>
        </div>

        <button
          type="submit"
          disabled={isLoading}
          className="w-full bg-gradient-to-r from-emerald-500 to-emerald-600 text-white py-4 px-6 rounded-xl font-semibold hover:from-emerald-600 hover:to-emerald-700 focus:ring-4 focus:ring-emerald-200 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-3"
        >
          {isLoading ? (
            <>
              <div className="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent"></div>
              Generating Script...
            </>
          ) : (
            <>
              <Send className="w-5 h-5" />
              Generate Cricket Script
            </>
          )}
        </button>
      </form>
    </div>
  );
};

export default PromptInput;