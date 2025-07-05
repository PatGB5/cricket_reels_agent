import React, { useState, useEffect, useRef } from 'react';
import { Video, Loader, Check, X } from 'lucide-react';
import { createVideo, editVideo } from '../services/api';

interface VideoCreationProps {
  script: string;
  onComplete: (finalVideoUrl: string) => void;
  isLoading: boolean;
  onReject: () => void;
}

const VideoCreation: React.FC<VideoCreationProps> = ({ script, onComplete, isLoading, onReject }) => {
  const [currentPhase, setCurrentPhase] = useState<'create' | 'preview' | 'edit'>('create');
  const [previewVideoUrl, setPreviewVideoUrl] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const hasStartedCreation = useRef(false);

  // Auto-start video creation when component mounts - only once
  useEffect(() => {
    if (currentPhase === 'create' && script && !hasStartedCreation.current) {
      hasStartedCreation.current = true;
      handleCreateVideo();
    }
  }, [script, currentPhase]);

  const handleCreateVideo = async () => {
    setIsProcessing(true);
    setError(null);
    try {
      const response = await createVideo(script);
      
      if (response.status === "created") {
        setPreviewVideoUrl(response.download_url);
        setCurrentPhase('preview');
      } else {
        setError("Video creation failed");
      }
    } catch (err) {
      console.error('Video creation failed:', err);
      setError('Failed to create video. Please try again.');
    } finally {
      setIsProcessing(false);
    }
  };

  const handleAcceptVideo = async () => {
    setCurrentPhase('edit');
    setIsProcessing(true);
    setError(null);
  
    try {
      const videoUrl = await editVideo(script); // now receives a URL string
      onComplete(videoUrl);
    } catch (err) {
      console.error('Video editing failed:', err);
      setError('Failed to edit video. Please try again.');
      setIsProcessing(false);
    }
  };
  

  const handleRejectVideo = () => {
    setCurrentPhase('create');
    setPreviewVideoUrl('');
    setError(null);
    hasStartedCreation.current = false; // Reset the flag to allow recreation
  };

  if (error) {
    return (
      <div className="bg-white rounded-2xl shadow-xl p-8 max-w-2xl mx-auto">
        <div className="text-center">
          <div className="bg-red-100 rounded-full p-4 w-16 h-16 mx-auto mb-4">
            <X className="w-8 h-8 text-red-500 mx-auto" />
          </div>
          <h2 className="text-2xl font-bold text-gray-800 mb-2">Error</h2>
          <p className="text-gray-600 mb-6">{error}</p>
          <div className="flex gap-4 justify-center">
            <button
              onClick={onReject}
              className="flex items-center gap-2 px-6 py-3 bg-gray-100 text-gray-700 rounded-xl hover:bg-gray-200 transition-all duration-200"
            >
              <X className="w-5 h-5" />
              Back to Script
            </button>
            <button
              onClick={() => {
                setError(null);
                if (currentPhase === 'create') {
                  hasStartedCreation.current = false;
                  handleCreateVideo();
                } else if (currentPhase === 'preview') {
                  handleAcceptVideo();
                }
              }}
              className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-emerald-500 to-emerald-600 text-white rounded-xl hover:from-emerald-600 hover:to-emerald-700 transition-all duration-200"
            >
              <Loader className="w-5 h-5" />
              Try Again
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (currentPhase === 'create') {
    return (
      <div className="bg-white rounded-2xl shadow-xl p-8 max-w-2xl mx-auto">
        <div className="text-center mb-6">
          <Loader className="w-12 h-12 mx-auto mb-4 text-emerald-500 animate-spin" />
          <h2 className="text-2xl font-bold text-gray-800">Creating Your Video</h2>
          <p className="text-gray-600 mt-2">Generating video using AI with your approved script</p>
        </div>

        <div className="bg-gradient-to-br from-gray-50 to-gray-100 rounded-xl p-6 mb-6 border border-gray-200">
          <h3 className="text-lg font-semibold text-gray-800 mb-3">Script Preview</h3>
          <div className="prose prose-gray max-w-none">
            <p className="text-gray-700 leading-relaxed whitespace-pre-wrap text-sm">
              {script.length > 200 ? `${script.substring(0, 200)}...` : script}
            </p>
          </div>
        </div>

        <div className="bg-gradient-to-br from-emerald-50 to-blue-50 rounded-xl p-6 border border-emerald-200">
          <div className="flex items-center justify-center">
            <div className="animate-pulse text-center">
              <p className="text-gray-600 text-sm">
                Please wait while we generate your cricket facts video using AI...
              </p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (currentPhase === 'preview') {
    return (
      <div className="bg-white rounded-2xl shadow-xl p-8 max-w-4xl mx-auto">
        <div className="text-center mb-6">
          <Video className="w-12 h-12 mx-auto mb-4 text-emerald-500" />
          <h2 className="text-2xl font-bold text-gray-800">Preview Your Video</h2>
          <p className="text-gray-600 mt-2">Review the generated video before final editing</p>
        </div>

        <div className="bg-gradient-to-br from-gray-50 to-gray-100 rounded-xl p-6 mb-8">
          <video
            controls
            className="w-full max-w-md mx-auto rounded-lg shadow-lg"
            poster="https://images.pexels.com/photos/274506/pexels-photo-274506.jpeg?auto=compress&cs=tinysrgb&w=400"
          >
            <source src={previewVideoUrl} type="video/mp4" />
            Your browser does not support the video tag.
          </video>
        </div>

        <div className="flex gap-4 justify-center">
          <button
            onClick={handleRejectVideo}
            disabled={isProcessing}
            className="flex items-center gap-2 px-6 py-3 bg-gray-100 text-gray-700 rounded-xl hover:bg-gray-200 transition-all duration-200 disabled:opacity-50"
          >
            <X className="w-5 h-5" />
            Create New Video
          </button>
          
          <button
            onClick={handleAcceptVideo}
            disabled={isProcessing}
            className="flex items-center gap-2 px-8 py-3 bg-gradient-to-r from-emerald-500 to-emerald-600 text-white rounded-xl hover:from-emerald-600 hover:to-emerald-700 transition-all duration-200 disabled:opacity-50 shadow-lg"
          >
            {isProcessing ? (
              <>
                <Loader className="w-5 h-5 animate-spin" />
                Processing...
              </>
            ) : (
              <>
                <Check className="w-5 h-5" />
                Accept & Apply Final Edits
              </>
            )}
          </button>
        </div>
      </div>
    );
  }

  // Edit phase
  return (
    <div className="bg-white rounded-2xl shadow-xl p-8 max-w-2xl mx-auto">
      <div className="text-center mb-6">
        <Loader className="w-12 h-12 mx-auto mb-4 text-emerald-500 animate-spin" />
        <h2 className="text-2xl font-bold text-gray-800">Processing Final Video</h2>
        <p className="text-gray-600 mt-2">Applying final edits and enhancements...</p>
      </div>

      <div className="bg-gradient-to-br from-emerald-50 to-blue-50 rounded-xl p-6 border border-emerald-200">
        <div className="flex items-center justify-center">
          <div className="animate-pulse text-center">
            <p className="text-gray-600 text-sm">
              Your video is being enhanced with overlays, timestamps, and cricket-specific visual elements.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default VideoCreation;