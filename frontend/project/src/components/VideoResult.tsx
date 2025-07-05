import React from 'react';
import { Download, Share2, RefreshCw } from 'lucide-react';

interface VideoResultProps {
  videoUrl: string;
  onStartOver: () => void;
}

const VideoResult: React.FC<VideoResultProps> = ({ videoUrl, onStartOver }) => {
  const handleDownload = () => {
    const link = document.createElement('a');
    link.href = videoUrl;
    link.download = 'cricket-facts-reel.mp4';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const handleShare = async () => {
    if (navigator.share) {
      try {
        await navigator.share({
          title: 'Cricket Facts Reel',
          text: 'Check out this amazing cricket facts reel!',
          url: videoUrl,
        });
      } catch (err) {
        console.error('Error sharing:', err);
      }
    }
  };

  return (
    <div className="bg-white rounded-2xl shadow-xl p-8 max-w-4xl mx-auto">
      <div className="text-center mb-6">
        <div className="bg-gradient-to-r from-emerald-400 to-blue-500 bg-clip-text text-transparent">
          <h2 className="text-3xl font-bold">🎉 Your Reel is Ready!</h2>
        </div>
        <p className="text-gray-600 mt-2">Your cricket facts reel has been processed and enhanced</p>
      </div>

      <div className="bg-gradient-to-br from-gray-50 to-gray-100 rounded-xl p-6 mb-8">
        <video
          controls
          className="w-full max-w-md mx-auto rounded-lg shadow-lg"
          poster="https://images.pexels.com/photos/274506/pexels-photo-274506.jpeg?auto=compress&cs=tinysrgb&w=400"
        >
          <source src={videoUrl} type="video/mp4" />
          Your browser does not support the video tag.
        </video>
      </div>

      <div className="flex flex-col sm:flex-row gap-4 justify-center">
        <button
          onClick={handleDownload}
          className="flex items-center justify-center gap-2 px-6 py-3 bg-gradient-to-r from-emerald-500 to-emerald-600 text-white rounded-xl hover:from-emerald-600 hover:to-emerald-700 transition-all duration-200 shadow-lg"
        >
          <Download className="w-5 h-5" />
          Download Video
        </button>
        
        {navigator.canShare && navigator.canShare({ url: videoUrl }) && (
          <button
            onClick={handleShare}
            className="flex items-center justify-center gap-2 px-6 py-3 bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-xl hover:from-blue-600 hover:to-blue-700 transition-all duration-200 shadow-lg"
          >
            <Share2 className="w-5 h-5" />
            Share Video
          </button>
        )}
        
        <button
          onClick={onStartOver}
          className="flex items-center justify-center gap-2 px-6 py-3 bg-gray-100 text-gray-700 rounded-xl hover:bg-gray-200 transition-all duration-200"
        >
          <RefreshCw className="w-5 h-5" />
          Create Another Reel
        </button>
      </div>
    </div>
  );
};

export default VideoResult;