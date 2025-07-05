const API_BASE_URL = import.meta.env.VITE_REACT_APP_API_URL || 'http://localhost:8000';

export const generateScript = async (additionalPrompt: string): Promise<{
  status: string;
  script: string;
  script_path: string;
}> => {
  const formData = new FormData();
  formData.append("extra_prompt", additionalPrompt); // Must match FastAPI Form param

  const response = await fetch(`${API_BASE_URL}/generate_script/`, {
    method: "POST",
    body: formData, // Browser handles Content-Type for FormData
  });

  if (!response.ok) {
    throw new Error("Failed to generate script");
  }

  const data = await response.json();

  if (data.status !== "success") {
    throw new Error(data.message || "Script generation failed");
  }

  return data;
};

export const createVideo = async (script: string): Promise<{
  status: string;
  download_url: string;
}> => {
  const formData = new FormData();
  formData.append("script", script);

  const response = await fetch(`${API_BASE_URL}/create_video/`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Failed to create video");
  }

  const data = await response.json();

  if (data.status !== "created") {
    throw new Error(data.message || "Video creation failed");
  }

  return data;
};

export const editVideo = async (): Promise<string> => {
  const response = await fetch(`${API_BASE_URL}/edit_video/`, {
    method: "POST",
  });

  if (!response.ok) {
    throw new Error("Failed to edit video");
  }

  const data = await response.json();

  if (data.status !== "edited") {
    throw new Error(data.message || "Video editing failed");
  }

  return data.final_url;
};



// Keep the old uploadVideo function for backward compatibility if needed
export const uploadVideo = async (videoFile: File, script: string): Promise<any> => {
  const formData = new FormData();
  formData.append('video', videoFile);
  formData.append('script', script);

  const response = await fetch(`${API_BASE_URL}/upload_video/`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    throw new Error('Failed to upload video');
  }

  return response.json();
};