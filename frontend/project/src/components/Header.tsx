import React from 'react';
import { Zap } from 'lucide-react';

const Header: React.FC = () => {
  return (
    <header className="w-full bg-gradient-to-r from-emerald-600 to-emerald-700 shadow-lg">
      <div className="max-w-4xl mx-auto px-6 py-8">
        <div className="flex items-center gap-3">
          <div className="bg-white/20 p-3 rounded-xl backdrop-blur-sm">
            <Zap className="w-8 h-8 text-white" />
          </div>
          <div>
            <h1 className="text-3xl font-bold text-white">Cricket Facts AI</h1>
            <p className="text-emerald-100 mt-1">Daily Reel Generator</p>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;