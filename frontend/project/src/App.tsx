import React, { useState } from 'react';
import Header from './components/Header';
import StepIndicator from './components/StepIndicator';
import PromptInput from './components/PromptInput';
import ScriptDisplay from './components/ScriptDisplay';
import VideoCreation from './components/VideoCreation';
import VideoResult from './components/VideoResult';
import ErrorMessage from './components/ErrorMessage';
import { generateScript } from './services/api';
import { AppStep } from './types';

function App() {
  const [currentStep, setCurrentStep] = useState<AppStep>('prompt');
  const [prompt, setPrompt] = useState('');
  const [script, setScript] = useState('');
  const [finalVideoUrl, setFinalVideoUrl] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleGenerateScript = async (inputPrompt: string) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await generateScript(inputPrompt);
  
      if (response.status === "success") {
        setPrompt(inputPrompt);
        setScript(response.script);
        setCurrentStep("script");
      } else {
        setError("Failed to generate script");
      }
    } catch (err) {
      setError("Failed to generate script. Please check your connection and try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleAcceptScript = () => {
    setCurrentStep('create-video');
  };

  const handleRejectScript = () => {
    setCurrentStep('prompt');
    setScript('');
  };

  const handleVideoComplete = (videoUrl: string) => {
    setFinalVideoUrl(videoUrl);
    setCurrentStep('result');
  };

  const handleBackToScript = () => {
    setCurrentStep('script');
  };

  const handleStartOver = () => {
    setCurrentStep('prompt');
    setPrompt('');
    setScript('');
    setFinalVideoUrl('');
    setError(null);
  };

  const renderCurrentStep = () => {
    if (error) {
      return (
        <ErrorMessage
          message={error}
          onRetry={() => {
            setError(null);
            if (currentStep === 'script') {
              handleGenerateScript(prompt);
            }
          }}
        />
      );
    }

    switch (currentStep) {
      case 'prompt':
        return (
          <PromptInput
            onSubmit={handleGenerateScript}
            isLoading={isLoading}
          />
        );
      case 'script':
        return (
          <ScriptDisplay
            script={script}
            onAccept={handleAcceptScript}
            onReject={handleRejectScript}
            isLoading={isLoading}
          />
        );
      case 'create-video':
        return (
          <VideoCreation
            script={script}
            onComplete={handleVideoComplete}
            isLoading={isLoading}
            onReject={handleBackToScript}
          />
        );
      case 'result':
        return (
          <VideoResult
            videoUrl={finalVideoUrl}
            onStartOver={handleStartOver}
          />
        );
      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-50 via-blue-50 to-indigo-50">
      <Header />
      
      <main className="container mx-auto px-4 py-12">
        {!error && <StepIndicator currentStep={currentStep} />}
        {renderCurrentStep()}
      </main>

      <footer className="bg-white border-t border-gray-200 mt-16 py-8">
        <div className="max-w-4xl mx-auto px-6 text-center">
          <p className="text-gray-600">
            Powered by AI • Create engaging cricket content effortlessly
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;