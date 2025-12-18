import './QuestionCard.css';

function QuestionCard({ question, questionNumber }) {
  return (
    <div className="question-card">
      <div className="question-header">
        <span className="question-label">🎤 Question #{questionNumber}</span>
      </div>
      <div className="question-content">
        <p>{question}</p>
      </div>
    </div>
  );
}

export default QuestionCard;

