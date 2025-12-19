import axios from 'axios';
import { config } from '../config';

// Normalize API base URL to always end with /api
// Handles cases where VITE_API_URL might be set without /api suffix
let API_BASE_URL = config.apiUrl.trim();
if (!API_BASE_URL.endsWith('/api')) {
  // If it doesn't end with /api, add it
  if (API_BASE_URL.endsWith('/')) {
    API_BASE_URL = API_BASE_URL + 'api';
  } else {
    API_BASE_URL = API_BASE_URL + '/api';
  }
}

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interview API functions
export const interviewAPI = {
  // Create a new interview session
  createInterview: async (technology, position) => {
    // #region agent log
    const logData = {
      sessionId: 'debug-session',
      runId: 'run1',
      hypothesisId: 'A',
      location: 'services/api.js:createInterview',
      message: 'Frontend API call (normalized)',
      data: {
        originalApiUrl: config.apiUrl,
        normalizedBaseURL: API_BASE_URL,
        path: '/interview/create',
        expectedFullURL: API_BASE_URL + '/interview/create',
        method: 'POST'
      },
      timestamp: Date.now()
    };
    fetch('http://127.0.0.1:7243/ingest/53e08bbd-97d2-4d2e-a9de-853ed95b6016', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(logData)
    }).catch(() => {});
    // #endregion
    const response = await api.post('/interview/create', {
      technology,
      position,
    });
    return response.data;
  },

  // Start the interview and get first question
  startInterview: async (sessionId) => {
    const response = await api.post(`/interview/${sessionId}/start`);
    return response.data;
  },

  // Submit an answer
  submitAnswer: async (sessionId, answer) => {
    const response = await api.post(`/interview/${sessionId}/answer`, {
      answer,
    });
    return response.data;
  },

  // Get next question
  getNextQuestion: async (sessionId) => {
    const response = await api.post(`/interview/${sessionId}/next-question`);
    return response.data;
  },

  // End interview and get summary
  endInterview: async (sessionId) => {
    const response = await api.post(`/interview/${sessionId}/end`);
    return response.data;
  },

  // Get session info
  getSessionInfo: async (sessionId) => {
    const response = await api.get(`/interview/${sessionId}`);
    return response.data;
  },

  // Delete session
  deleteSession: async (sessionId) => {
    const response = await api.delete(`/interview/${sessionId}`);
    return response.data;
  },
};

// Health check
export const checkHealth = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL.replace('/api', '')}/health`);
    return response.data;
  } catch (error) {
    throw new Error('Backend is not available');
  }
};

export default api;

