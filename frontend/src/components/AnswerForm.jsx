import { useState } from 'react';
import './AnswerForm.css';

function AnswerForm({ onSubmit, loading }) {
  const [answer, setAnswer] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (answer.trim()) {
      onSubmit(answer);
      setAnswer('');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="answer-form">
      <div className="form-group">
        <label htmlFor="answer">
          💬 Your Answer:
        </label>
        <textarea
          id="answer"
          value={answer}
          onChange={(e) => setAnswer(e.target.value)}
          placeholder="Type your answer here... Provide a detailed and thoughtful response."
          rows={8}
          disabled={loading}
          required
        />
        <div className="char-count">
          {answer.length} characters
        </div>
      </div>

      <button 
        type="submit" 
        className="btn btn-primary btn-large"
        disabled={loading || !answer.trim()}
      >
        {loading ? '⏳ Submitting...' : '📤 Submit Answer'}
      </button>
    </form>
  );
}

export default AnswerForm;

