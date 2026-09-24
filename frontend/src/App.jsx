import { useEffect, useState } from 'react'
import InterviewSetup from './components/InterviewSetup'
import Interview from './components/Interview'
import { checkHealth } from './services/api'
import './App.css'

function App() {
  const [sessionId, setSessionId] = useState(null)
  const [interviewData, setInterviewData] = useState(null)
  const [modelName, setModelName] = useState(null)
  const [providerName, setProviderName] = useState(null)

  useEffect(() => {
    checkHealth()
      .then((data) => {
        setModelName(data?.model || null)
        setProviderName(data?.provider || null)
      })
      .catch(() => {})
  }, [])

  const handleStartInterview = (sessionId, technology, position) => {
    setSessionId(sessionId)
    setInterviewData({ technology, position })
  }

  const handleResetInterview = () => {
    setSessionId(null)
    setInterviewData(null)
  }

  return (
    <div className="App">
      <header className="app-header">
        <h1>🎯 AI Interviewer</h1>
        <p>Multi-Agent Interview System powered by AI</p>
      </header>

      <main className="container">
        {!sessionId ? (
          <InterviewSetup onStart={handleStartInterview} />
        ) : (
          <Interview 
            sessionId={sessionId} 
            technology={interviewData.technology}
            position={interviewData.position}
            onReset={handleResetInterview}
          />
        )}
      </main>

      <footer className="app-footer">
        <p>
          {modelName && providerName
            ? `Powered by ${modelName} via ${providerName}`
            : modelName
              ? `Powered by ${modelName}`
              : providerName
                ? `Powered by ${providerName}`
                : 'Powered by AI'}
          {' | Built with React & Flask'}
        </p>
      </footer>
    </div>
  )
}

export default App

