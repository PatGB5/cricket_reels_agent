export interface ScriptResponse {
  status: string;
  script: string;
  script_path: string;
  message?: string;
}

export interface CreateVideoResponse {
  status: string;
  download_url: string;
  message?: string;
}

export interface VideoUploadResponse {
  edited_video_url: string;
  success: boolean;
  message?: string;
}

export type AppStep = 'prompt' | 'script' | 'create-video' | 'result';