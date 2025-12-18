/**
 * Frontend configuration from environment variables
 */

export const config = {
  // API Configuration
  apiUrl: import.meta.env.VITE_API_URL || 'http://localhost:5001/api',
  
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

