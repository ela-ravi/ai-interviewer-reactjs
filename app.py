"""
AI Interviewer - Streamlit Frontend
Multi-agent interview system using Autogen
"""
import streamlit as st
from agents import InterviewAgents
import os
from dotenv import load_dotenv

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Interviewer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .question-box {
        background-color: #f0f8ff;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 10px 0;
    }
    .feedback-box {
        background-color: #fff8dc;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #ffa500;
        margin: 10px 0;
    }
    .score-box {
        background-color: #f0fff0;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #32cd32;
        margin: 10px 0;
    }
    .summary-box {
        background-color: #fff0f5;
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #ff69b4;
        margin: 20px 0;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        padding: 10px;
    }
    .stButton>button:hover {
        background-color: #145a8d;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables"""
    if 'agents' not in st.session_state:
        st.session_state.agents = None
    if 'interview_started' not in st.session_state:
        st.session_state.interview_started = False
    if 'current_question' not in st.session_state:
        st.session_state.current_question = None
    if 'question_number' not in st.session_state:
        st.session_state.question_number = 1
    if 'waiting_for_answer' not in st.session_state:
        st.session_state.waiting_for_answer = False
    if 'interview_complete' not in st.session_state:
        st.session_state.interview_complete = False
    if 'qa_history' not in st.session_state:
        st.session_state.qa_history = []


async def start_interview_async(technology: str, position: str):
    """Initialize and start the interview (async)"""
    st.session_state.agents = InterviewAgents(technology, position)
    st.session_state.interview_started = True
    st.session_state.question_number = 1
    st.session_state.qa_history = []
    st.session_state.interview_complete = False
    
    # Get first question
    question = await st.session_state.agents.get_next_question(1)
    st.session_state.current_question = question
    st.session_state.waiting_for_answer = True


def start_interview(technology: str, position: str):
    """Initialize and start the interview"""
    try:
        import asyncio
        with st.spinner("🤔 Preparing your first question..."):
            asyncio.run(start_interview_async(technology, position))
        
        st.success("✅ Interview started! Answer the question below.")
        st.rerun()
    except Exception as e:
        st.error(f"❌ Error starting interview: {str(e)}")
        st.info("💡 Make sure your OpenRouter API key is set in the .env file")


async def submit_answer_async(answer: str):
    """Process the submitted answer (async)"""
    # Process the answer through coach and scorer
    result = await st.session_state.agents.process_answer(
        st.session_state.current_question,
        answer,
        st.session_state.question_number
    )
    
    # Store in history
    st.session_state.qa_history.append(result)
    
    # Display feedback and score
    st.session_state.last_result = result
    st.session_state.waiting_for_answer = False


def submit_answer(answer: str):
    """Process the submitted answer"""
    if not answer.strip():
        st.warning("⚠️ Please provide an answer before submitting.")
        return
    
    with st.spinner("🔄 Analyzing your answer... (This may take a moment)"):
        try:
            import asyncio
            asyncio.run(submit_answer_async(answer))
        except Exception as e:
            st.error(f"❌ Error processing answer: {str(e)}")


async def get_next_question_async():
    """Get the next interview question (async)"""
    question = await st.session_state.agents.get_next_question(
        st.session_state.question_number
    )
    st.session_state.current_question = question
    st.session_state.waiting_for_answer = True
    st.session_state.last_result = None


def get_next_question():
    """Get the next interview question"""
    st.session_state.question_number += 1
    
    with st.spinner("🤔 Preparing next question..."):
        try:
            import asyncio
            asyncio.run(get_next_question_async())
            st.rerun()
        except Exception as e:
            st.error(f"❌ Error getting next question: {str(e)}")


def end_interview():
    """End the interview and show summary"""
    st.session_state.interview_complete = True
    st.session_state.waiting_for_answer = False


def main():
    """Main application"""
    initialize_session_state()
    
    # Header
    st.markdown('<div class="main-header">🎯 AI Interviewer</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Multi-Agent Interview System powered by AI</div>', unsafe_allow_html=True)
    
    # Check for API key
    if not os.getenv("OPENROUTER_API_KEY"):
        st.error("❌ OpenRouter API key not found!")
        st.info("📝 Please create a .env file with your OPENROUTER_API_KEY")
        st.code("OPENROUTER_API_KEY=your_openrouter_api_key_here")
        st.info("💡 Get your API key from: https://openrouter.ai/keys")
        return
    
    # Sidebar for interview setup
    with st.sidebar:
        st.header("📋 Interview Setup")
        
        if not st.session_state.interview_started:
            st.markdown("### Configure Interview")
            
            technology = st.text_input(
                "🔧 Technology/Domain",
                placeholder="e.g., Python, JavaScript, Machine Learning",
                help="Enter the main technology or domain for the interview"
            )
            
            position = st.text_input(
                "💼 Position",
                placeholder="e.g., Senior Developer, Data Scientist",
                help="Enter the position level and role"
            )
            
            st.markdown("---")
            
            if st.button("🚀 Start Interview", type="primary", key="start_interview_btn"):
                if technology and position:
                    start_interview(technology, position)
                else:
                    st.warning("⚠️ Please fill in both fields")
        
        else:
            st.markdown("### 📊 Interview Progress")
            st.metric("Question Number", st.session_state.question_number)
            st.metric("Questions Answered", len(st.session_state.qa_history))
            
            if st.session_state.qa_history:
                avg_score = sum([qa['score'] for qa in st.session_state.qa_history]) / len(st.session_state.qa_history)
                st.metric("Average Score", f"{avg_score:.1f}/10")
            
            st.markdown("---")
            
            if not st.session_state.interview_complete:
                if st.button("🏁 End Interview", type="secondary", key="sidebar_end_interview_btn"):
                    if len(st.session_state.qa_history) > 0:
                        end_interview()
                        st.rerun()
                    else:
                        st.warning("Answer at least one question before ending")
            
            if st.button("🔄 Start New Interview", key="sidebar_new_interview_btn"):
                # Reset all state
                st.session_state.clear()
                st.rerun()
    
    # Main content area
    if not st.session_state.interview_started:
        # Welcome screen
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            ## 👋 Welcome to AI Interviewer!
            
            This intelligent interview system uses **4 specialized AI agents**:
            
            1. 🎤 **Interviewer Agent** - Asks relevant technical questions
            2. 👤 **User Proxy Agent** - Facilitates your responses
            3. 👨‍🏫 **Coach Agent** - Provides feedback on your answers
            4. 📊 **Scorer Agent** - Evaluates your performance
            
            ### How it works:
            1. Enter the technology/domain and position in the sidebar
            2. Click "Start Interview" to begin
            3. Answer questions one at a time
            4. Receive instant feedback and scoring
            5. Review your overall performance
            
            ### Get Started:
            Fill in the interview details in the sidebar to begin! 👈
            """)
    
    elif st.session_state.interview_complete:
        # Show final summary
        st.markdown("## 🎊 Interview Complete!")
        
        import asyncio
        summary = asyncio.run(st.session_state.agents.get_overall_summary())
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Questions", summary['total_questions'])
        with col2:
            st.metric("Average Score", f"{summary['average_score']}/10")
        with col3:
            score_emoji = "🌟" if summary['average_score'] >= 8 else "👍" if summary['average_score'] >= 6 else "📈"
            st.metric("Performance", score_emoji)
        
        st.markdown('<div class="summary-box">', unsafe_allow_html=True)
        st.markdown("### 📝 Overall Assessment")
        st.write(summary['summary'])
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Detailed breakdown
        st.markdown("---")
        st.markdown("### 📊 Detailed Breakdown")
        
        for qa in st.session_state.qa_history:
            with st.expander(f"Question {qa['question_number']}: Score {qa['score']}/10"):
                st.markdown(f"**❓ Question:**")
                st.info(qa['question'])
                
                st.markdown(f"**💬 Your Answer:**")
                st.write(qa['answer'])
                
                st.markdown(f"**👨‍🏫 Coach Feedback:**")
                st.warning(qa['feedback'])
                
                st.markdown(f"**📊 Score Details:**")
                st.success(qa['score_details'])
        
        st.markdown("---")
        st.info("💡 Click 'Start New Interview' in the sidebar to try again with different topics!")
    
    else:
        # Active interview
        if st.session_state.waiting_for_answer and st.session_state.current_question:
            # Display current question
            st.markdown(f"## Question {st.session_state.question_number}")
            
            st.markdown('<div class="question-box">', unsafe_allow_html=True)
            st.markdown("### 🎤 Interviewer asks:")
            st.markdown(f"**{st.session_state.current_question}**")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Answer input
            st.markdown("### 💬 Your Answer:")
            answer = st.text_area(
                "Type your answer here...",
                height=200,
                key=f"answer_{st.session_state.question_number}",
                placeholder="Provide a detailed answer to the question above..."
            )
            
            if st.button("📤 Submit Answer", type="primary", key="submit_answer_btn"):
                submit_answer(answer)
                st.rerun()
        
        elif hasattr(st.session_state, 'last_result') and st.session_state.last_result:
            # Show feedback and score
            result = st.session_state.last_result
            
            st.markdown(f"## Question {result['question_number']} - Results")
            
            # Question
            st.markdown('<div class="question-box">', unsafe_allow_html=True)
            st.markdown("### ❓ Question:")
            st.write(result['question'])
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Answer
            st.markdown("### 💬 Your Answer:")
            st.write(result['answer'])
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Feedback
                st.markdown('<div class="feedback-box">', unsafe_allow_html=True)
                st.markdown("### 👨‍🏫 Coach Feedback:")
                st.write(result['feedback'])
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                # Score
                st.markdown('<div class="score-box">', unsafe_allow_html=True)
                st.markdown("### 📊 Score:")
                st.markdown(f"## {result['score']}/10")
                st.write(result['score_details'])
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Next question button
            st.markdown("---")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("➡️ Next Question", type="primary", key="next_question_btn"):
                    get_next_question()
            with col2:
                if st.button("🏁 End Interview", key="main_end_interview_btn"):
                    end_interview()
                    st.rerun()


if __name__ == "__main__":
    main()

