import { useEffect, useState } from 'react';
import { interviewAPI } from '../services/api';
import './InterviewSetup.css';

function InterviewSetup({ onStart }) {
  const [technology, setTechnology] = useState('');
  const [position, setPosition] = useState('');
  const [providers, setProviders] = useState([]);
  const [provider, setProvider] = useState('');
  const [apiKey, setApiKey] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    interviewAPI.getProviders()
      .then((data) => {
        const list = data?.providers || [];
        setProviders(list);
        if (list[0]) {
          setProvider(list[0].id);
        }
      })
      .catch(() => setError('Could not load providers. Is the backend running?'));
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!technology.trim() || !position.trim() || !provider || !apiKey.trim()) {
      setError('Please fill in every field, including your API key');
      return;
    }

    setLoading(true);
    setError(null);
    const key = apiKey.trim();
    // Developer override, set in the browser console:
    // localStorage.setItem('interviewModel', 'openai/gpt-oss-20b')
    const modelOverride = (window.localStorage.getItem('interviewModel') || '').trim();

    try {
      const result = await interviewAPI.createInterview(
        technology,
        position,
        provider,
        modelOverride,
        key,
      );
      setApiKey('');

      await interviewAPI.startInterview(result.session_id);

      const chosen = providers.find((item) => item.id === provider);
      onStart(result.session_id, technology, position, chosen?.label || provider, result.model);
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
        
        <details className="info-box">
          <summary>Curious on How it works!</summary>
          <ul>
            <li>🎤 <strong>Interviewer Agent</strong> - Asks relevant technical questions</li>
            <li>👨‍🏫 <strong>Coach Agent</strong> - Provides feedback on your answers</li>
            <li>📊 <strong>Scorer Agent</strong> - Evaluates your performance</li>
          </ul>
        </details>

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

          {providers.length > 1 && (
            <div className="form-group">
              <label htmlFor="provider">
                Provider
              </label>
              <select
                id="provider"
                value={provider}
                onChange={(e) => setProvider(e.target.value)}
                disabled={loading}
              >
                {providers.map((item) => (
                  <option key={item.id} value={item.id}>{item.label}</option>
                ))}
              </select>
            </div>
          )}

          <div className="form-group">
            <label htmlFor="apiKey">
              API key
            </label>
            <input
              id="apiKey"
              type="password"
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              placeholder="Paste your Groq API key"
              autoComplete="off"
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

