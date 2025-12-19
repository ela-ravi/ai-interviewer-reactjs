/**
 * Frontend configuration from environment variables
 */

// #region agent log
// Log actual config values
const apiUrlValue = import.meta.env.VITE_API_URL || 'http://localhost:5001/api';
const logData = {
  sessionId: 'debug-session',
  runId: 'run1',
  hypothesisId: 'A',
  location: 'config.js:config',
  message: 'Frontend config loaded',
  data: {
    VITE_API_URL: import.meta.env.VITE_API_URL,
    apiUrl: apiUrlValue,
    allEnvVars: Object.keys(import.meta.env).filter(k => k.startsWith('VITE_'))
  },
  timestamp: Date.now()
};
fetch('http://127.0.0.1:7243/ingest/53e08bbd-97d2-4d2e-a9de-853ed95b6016', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(logData)
}).catch(() => {});
// #endregion

export const config = {
  // API Configuration
  apiUrl: apiUrlValue,
  
  // App Configuration
  appName: import.meta.env.VITE_APP_NAME || 'AI Interviewer',
  appDescription: import.meta.env.VITE_APP_DESCRIPTION || 'Multi-Agent Interview System',
  
  // Feature Flags
  enableAnalytics: import.meta.env.VITE_ENABLE_ANALYTICS === 'true',
  enableDebug: import.meta.env.VITE_ENABLE_DEBUG === 'true',
};

// Log configuration in development
if (config.enableDebug) {
  console.log('🔧 App Configuration:', config);
}

export default config;

