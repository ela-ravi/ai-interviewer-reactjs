import { useState } from 'react';
import { interviewAPI } from '../services/api';
import './InterviewSetup.css';

function InterviewSetup({ onStart }) {
  const [technology, setTechnology] = useState('');
  const [position, setPosition] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!technology.trim() || !position.trim()) {
      setError('Please fill in both fields');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      // Create interview session
      const result = await interviewAPI.createInterview(technology, position);
      
      // Start the interview
      await interviewAPI.startInterview(result.session_id);
      
      // Notify parent component
      onStart(result.session_id, technology, position);
    } catch (err) {
      console.error('Error starting interview:', err);
      setError(err.response?.data?.error || 'Failed to start interview. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="interview-setup">
      <div className="setup-card">
        <h2>👋 Welcome to AI Interviewer!</h2>
        
        <div className="info-box">
          <h3>How it works:</h3>
          <ul>
            <li>🎤 <strong>Interviewer Agent</strong> - Asks relevant technical questions</li>
            <li>👨‍🏫 <strong>Coach Agent</strong> - Provides feedback on your answers</li>
            <li>📊 <strong>Scorer Agent</strong> - Evaluates your performance</li>
          </ul>
        </div>

        <form onSubmit={handleSubmit} className="setup-form">
          <div className="form-group">
            <label htmlFor="technology">
              🔧 Technology/Domain
            </label>
            <input
              id="technology"
              type="text"
              value={technology}
              onChange={(e) => setTechnology(e.target.value)}
              placeholder="e.g., Python, JavaScript, Machine Learning"
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="position">
              💼 Position
            </label>
            <input
              id="position"
              type="text"
              value={position}
              onChange={(e) => setPosition(e.target.value)}
              placeholder="e.g., Senior Developer, Data Scientist"
              disabled={loading}
            />
          </div>

          {error && (
            <div className="error-message">
              ⚠️ {error}
            </div>
          )}

          <button 
            type="submit" 
            className="btn btn-primary"
            disabled={loading}
          >
            {loading ? '⏳ Starting Interview...' : '🚀 Start Interview'}
          </button>
        </form>
      </div>
    </div>
  );
}

export default InterviewSetup;

