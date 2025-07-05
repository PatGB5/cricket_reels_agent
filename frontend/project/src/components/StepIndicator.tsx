import React from 'react';
import { Check, FileText, Video, Download } from 'lucide-react';
import { AppStep } from '../types';

interface StepIndicatorProps {
  currentStep: AppStep;
}

const StepIndicator: React.FC<StepIndicatorProps> = ({ currentStep }) => {
  const steps = [
    { id: 'prompt', label: 'Create Prompt', icon: FileText },
    { id: 'script', label: 'Review Script', icon: Check },
    { id: 'create-video', label: 'Create & Edit Video', icon: Video },
    { id: 'result', label: 'Get Result', icon: Download },
  ];

  const getCurrentStepIndex = () => {
    return steps.findIndex(step => step.id === currentStep);
  };

  const currentIndex = getCurrentStepIndex();

  return (
    <div className="flex items-center justify-between max-w-2xl mx-auto mb-8">
      {steps.map((step, index) => {
        const isActive = index === currentIndex;
        const isCompleted = index < currentIndex;
        const Icon = step.icon;

        return (
          <div key={step.id} className="flex items-center">
            <div className={`
              flex items-center justify-center w-12 h-12 rounded-full transition-all duration-300
              ${isActive ? 'bg-emerald-500 text-white shadow-lg scale-110' : 
                isCompleted ? 'bg-emerald-100 text-emerald-600' : 'bg-gray-100 text-gray-400'}
            `}>
              <Icon className="w-5 h-5" />
            </div>
            <div className="ml-3">
              <p className={`text-sm font-medium ${isActive ? 'text-emerald-600' : isCompleted ? 'text-emerald-500' : 'text-gray-400'}`}>
                {step.label}
              </p>
            </div>
            {index < steps.length - 1 && (
              <div className={`
                flex-1 h-0.5 mx-6 transition-colors duration-300
                ${isCompleted ? 'bg-emerald-200' : 'bg-gray-200'}
              `} />
            )}
          </div>
        );
      })}
    </div>
  );
};

export default StepIndicator;