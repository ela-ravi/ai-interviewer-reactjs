import { useEffect, useState } from 'react';
import { interviewAPI } from '../services/api';
import './InterviewSetup.css';

const API_KEY_STORAGE = 'interviewApiKey';
// Paste a YouTube watch, share, or embed link.
const GROQ_KEY_VIDEO_URL = 'https://www.youtube.com/watch?v=X3_nJyuksqU';

function youtubeEmbedUrl(pageUrl) {
  const raw = (pageUrl || '').trim();
  if (!raw) return '';
  try {
    const url = new URL(raw);
    const host = url.hostname.replace(/^www\./, '');
    let id = '';
    if (host === 'youtu.be') {
      id = url.pathname.split('/').filter(Boolean)[0] || '';
    } else if (host === 'youtube.com' || host === 'youtube-nocookie.com' || host === 'm.youtube.com') {
      if (url.pathname === '/watch') {
        id = url.searchParams.get('v') || '';
      } else {
        const parts = url.pathname.split('/').filter(Boolean);
        const marker = parts.findIndex((part) => part === 'embed' || part === 'shorts' || part === 'live');
        id = marker >= 0 ? parts[marker + 1] || '' : '';
      }
    }
    if (!/^[A-Za-z0-9_-]{11}$/.test(id)) return '';
    return `https://www.youtube-nocookie.com/embed/${id}`;
  } catch {
    return '';
  }
}

const GROQ_KEY_VIDEO_EMBED = youtubeEmbedUrl(GROQ_KEY_VIDEO_URL);

function readSavedApiKey() {
  try {
    // Drop any key saved by the earlier localStorage version.
    window.localStorage.removeItem(API_KEY_STORAGE);
    return (window.sessionStorage.getItem(API_KEY_STORAGE) || '').trim();
  } catch {
    return '';
  }
}

function rememberApiKey(value) {
  try {
    window.localStorage.removeItem(API_KEY_STORAGE);
    const trimmed = value.trim();
    if (trimmed) {
      window.sessionStorage.setItem(API_KEY_STORAGE, trimmed);
    } else {
      window.sessionStorage.removeItem(API_KEY_STORAGE);
    }
  } catch {
    // Private mode can block storage. The field still works for this visit.
  }
}

function InterviewSetup({ onStart }) {
  const [technology, setTechnology] = useState('');
  const [position, setPosition] = useState('');
  const [providers, setProviders] = useState([]);
  const [provider, setProvider] = useState('');
  const [apiKey, setApiKey] = useState(readSavedApiKey);
  const [showKeyVideo, setShowKeyVideo] = useState(false);
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
              placeholder="e.g., Python, MBD(Automotive), JavaScript, Machine Learning, SIL, MIL, etc..,"
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
              onChange={(e) => {
                setApiKey(e.target.value);
                rememberApiKey(e.target.value);
              }}
              placeholder="Paste your Groq API key"
              autoComplete="off"
              disabled={loading}
            />
            <p className="field-hint">
              {apiKey.trim()
                ? 'Kept for this tab only. Close the tab to forget it.'
                : 'Used for this tab only. It is not saved on this device.'}
            </p>
            <details className="key-help" open={showKeyVideo}>
              <summary
                onClick={(e) => {
                  e.preventDefault();
                  setShowKeyVideo((open) => !open);
                }}
              >
                How to get a Groq API key
              </summary>
              <div className="key-help-body">
                {showKeyVideo && GROQ_KEY_VIDEO_EMBED && (
                  <div className="video-frame">
                    <iframe
                      src={GROQ_KEY_VIDEO_EMBED}
                      title="How to get a Groq API key"
                      allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                      allowFullScreen
                    />
                  </div>
                )}
                <a
                  className="key-help-link"
                  href="https://console.groq.com/keys"
                  target="_blank"
                  rel="noreferrer"
                >
                  Open the Groq console
                </a>
              </div>
            </details>
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

