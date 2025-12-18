import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5001/api';

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

