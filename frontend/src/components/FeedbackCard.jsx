import './FeedbackCard.css';

function FeedbackCard({ result }) {
  const getScoreColor = (score) => {
    if (score >= 8) return 'excellent';
    if (score >= 6) return 'good';
    if (score >= 4) return 'average';
    return 'poor';
  };

  return (
    <div className="feedback-container">
      <div className="question-review">
        <h3>❓ Question</h3>
        <p>{result.question}</p>
      </div>

      <div className="answer-review">
        <h3>💬 Your Answer</h3>
        <p>{result.answer}</p>
      </div>

      <div className="feedback-grid">
        <div className="feedback-box">
          <h3>👨‍🏫 Coach Feedback</h3>
          <div className="feedback-content">
            {result.feedback.split('\n').map((line, index) => (
              <p key={index}>{line}</p>
            ))}
          </div>
        </div>

        <div className="score-box">
          <h3>📊 Score</h3>
          <div className={`score-display ${getScoreColor(result.score)}`}>
            <div className="score-number">{result.score}</div>
            <div className="score-label">out of 10</div>
          </div>
          <div className="score-details">
            {result.score_details.split('\n').map((line, index) => (
              <p key={index}>{line}</p>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default FeedbackCard;

