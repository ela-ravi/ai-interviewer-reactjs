import './Summary.css';

function Summary({ summary, technology, position, onReset }) {
  const getPerformanceLevel = (avgScore) => {
    if (avgScore >= 8) return { label: 'Excellent', emoji: '🌟', class: 'excellent' };
    if (avgScore >= 6) return { label: 'Good', emoji: '👍', class: 'good' };
    if (avgScore >= 4) return { label: 'Average', emoji: '📈', class: 'average' };
    return { label: 'Needs Improvement', emoji: '💪', class: 'poor' };
  };

  const performance = getPerformanceLevel(summary.average_score);

  return (
    <div className="summary-container">
      <div className="summary-header">
        <h2>🎊 Interview Complete!</h2>
        <p>{technology} - {position}</p>
      </div>

      <div className="summary-stats">
        <div className="stat-card">
          <div className="stat-value">{summary.total_questions}</div>
          <div className="stat-label">Questions Answered</div>
        </div>

        <div className="stat-card">
          <div className="stat-value">{summary.average_score}</div>
          <div className="stat-label">Average Score</div>
        </div>

        <div className="stat-card">
          <div className={`stat-value performance ${performance.class}`}>
            {performance.emoji} {performance.label}
          </div>
          <div className="stat-label">Performance</div>
        </div>
      </div>

      <div className="summary-feedback">
        <h3>📝 Overall Assessment</h3>
        <div className="feedback-text">
          {summary.summary.split('\n').map((line, index) => (
            <p key={index}>{line}</p>
          ))}
        </div>
      </div>

      <div className="summary-breakdown">
        <h3>📊 Question Breakdown</h3>
        
        {summary.history && summary.history.map((qa) => (
          <details key={qa.question_number} className="qa-accordion">
            <summary>
              <span className="qa-title">Question {qa.question_number}</span>
              <span className="qa-score">Score: {qa.score}/10</span>
            </summary>
            <div className="qa-details">
              <div className="qa-section">
                <h4>❓ Question:</h4>
                <p>{qa.question}</p>
              </div>

              <div className="qa-section">
                <h4>💬 Your Answer:</h4>
                <p>{qa.answer}</p>
              </div>

              <div className="qa-section">
                <h4>👨‍🏫 Feedback:</h4>
                <p className="feedback">{qa.feedback}</p>
              </div>

              <div className="qa-section">
                <h4>📊 Score Details:</h4>
                <p className="score-detail">{qa.score_details}</p>
              </div>
            </div>
          </details>
        ))}
      </div>

      <div className="summary-actions">
        <button 
          onClick={onReset}
          className="btn btn-primary btn-large"
        >
          🔄 Start New Interview
        </button>
      </div>
    </div>
  );
}

export default Summary;

