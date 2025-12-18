import { useState, useEffect } from 'react';
import { interviewAPI } from '../services/api';
import QuestionCard from './QuestionCard';
import AnswerForm from './AnswerForm';
import FeedbackCard from './FeedbackCard';
import Summary from './Summary';
import './Interview.css';

function Interview({ sessionId, technology, position, onReset }) {
  const [currentQuestion, setCurrentQuestion] = useState(null);
  const [questionNumber, setQuestionNumber] = useState(0);
  const [waitingForAnswer, setWaitingForAnswer] = useState(false);
  const [lastResult, setLastResult] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showSummary, setShowSummary] = useState(false);
  const [summary, setSummary] = useState(null);
  const [stats, setStats] = useState({ answered: 0, avgScore: 0 });

  useEffect(() => {
    loadFirstQuestion();
  }, [sessionId]);

  const loadFirstQuestion = async () => {
    try {
      setLoading(true);
      const result = await interviewAPI.getSessionInfo(sessionId);
      
      // If session already started, get question from the start endpoint
      const questionData = await interviewAPI.startInterview(sessionId);
      setCurrentQuestion(questionData.question);
      setQuestionNumber(questionData.question_number);
      setWaitingForAnswer(true);
      setError(null);
    } catch (err) {
      console.error('Error loading question:', err);
      setError('Failed to load question. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmitAnswer = async (answer) => {
    try {
      setLoading(true);
      const result = await interviewAPI.submitAnswer(sessionId, answer);
      
      setLastResult(result);
      setWaitingForAnswer(false);
      
      // Update stats
      const info = await interviewAPI.getSessionInfo(sessionId);
      setStats({
        answered: info.questions_answered,
        avgScore: info.average_score
      });
      
      setError(null);
    } catch (err) {
      console.error('Error submitting answer:', err);
      setError('Failed to submit answer. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleNextQuestion = async () => {
    try {
      setLoading(true);
      const result = await interviewAPI.getNextQuestion(sessionId);
      
      setCurrentQuestion(result.question);
      setQuestionNumber(result.question_number);
      setWaitingForAnswer(true);
      setLastResult(null);
      setError(null);
    } catch (err) {
      console.error('Error getting next question:', err);
      setError('Failed to get next question. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleEndInterview = async () => {
    if (stats.answered === 0) {
      setError('Please answer at least one question before ending the interview.');
      return;
    }

    try {
      setLoading(true);
      const result = await interviewAPI.endInterview(sessionId);
      
      setSummary(result.summary);
      setShowSummary(true);
      setError(null);
    } catch (err) {
      console.error('Error ending interview:', err);
      setError('Failed to end interview. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  if (loading && questionNumber === 0) {
    return (
      <div className="loading-container">
        <div className="spinner"></div>
        <p>Loading your interview...</p>
      </div>
    );
  }

  if (showSummary && summary) {
    return (
      <Summary 
        summary={summary}
        technology={technology}
        position={position}
        onReset={onReset}
      />
    );
  }

  return (
    <div className="interview-container">
      <div className="interview-header">
        <div className="interview-info">
          <h2>{technology} - {position}</h2>
          <div className="stats">
            <span className="stat-badge">Question #{questionNumber}</span>
            <span className="stat-badge">Answered: {stats.answered}</span>
            {stats.answered > 0 && (
              <span className="stat-badge score">Avg Score: {stats.avgScore}/10</span>
            )}
          </div>
        </div>
        <div className="interview-actions">
          <button 
            onClick={handleEndInterview}
            className="btn btn-secondary"
            disabled={loading}
          >
            🏁 End Interview
          </button>
          <button 
            onClick={onReset}
            className="btn btn-outline"
          >
            🔄 New Interview
          </button>
        </div>
      </div>

      {error && (
        <div className="error-banner">
          ⚠️ {error}
        </div>
      )}

      {waitingForAnswer && currentQuestion && (
        <>
          <QuestionCard 
            question={currentQuestion}
            questionNumber={questionNumber}
          />
          <AnswerForm 
            onSubmit={handleSubmitAnswer}
            loading={loading}
          />
        </>
      )}

      {lastResult && !waitingForAnswer && (
        <>
          <FeedbackCard result={lastResult} />
          <div className="next-actions">
            <button 
              onClick={handleNextQuestion}
              className="btn btn-primary btn-large"
              disabled={loading}
            >
              {loading ? '⏳ Loading...' : '➡️ Next Question'}
            </button>
            <button 
              onClick={handleEndInterview}
              className="btn btn-secondary btn-large"
              disabled={loading}
            >
              🏁 End Interview
            </button>
          </div>
        </>
      )}
    </div>
  );
}

export default Interview;

