"""
AI Interview Agents using Autogen framework
"""
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from typing import Dict, List, Tuple
import os
from dotenv import load_dotenv

load_dotenv()


class InterviewAgents:
    """Manages all AI agents for the interview process"""
    
    def __init__(self, technology: str, position: str):
        self.technology = technology
        self.position = position
        
        # Create model client for OpenRouter with Mistral AI
        self.model_client = OpenAIChatCompletionClient(
            model=os.getenv("MODEL", "mistralai/mistral-small-creative"),
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url=os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
            model_info={
                "vision": False,
                "function_calling": True,
                "json_output": True,
                "structured_output": False,
                "family": "unknown",
            }
        )
        
        self.interview_history = []
        self.scores = []
        self.feedbacks = []
        
        self._setup_agents()
    
    def _setup_agents(self):
        """Initialize all agents with their specific roles"""
        
        # 1. Interviewer Agent - Asks questions
        self.interviewer = AssistantAgent(
            name="Interviewer",
            model_client=self.model_client,
            description=f"Technical interviewer for {self.position} position focusing on {self.technology}",
            system_message=f"""You are an experienced technical interviewer conducting an interview for a {self.position} position focusing on {self.technology}.

Your responsibilities:
- Ask ONE relevant technical question at a time
- Questions should be appropriate for the {self.position} level
- Progress from basic to advanced concepts
- Ask follow-up questions based on previous answers
- Cover various aspects: theory, practical implementation, best practices, and problem-solving
- Keep questions clear and concise

IMPORTANT: Only ask ONE question per response. Wait for the answer before asking the next question.
Do not provide answers or hints. Just ask the question and wait.
Format: Simply state the question without extra commentary.""",
        )
        
        # 3. Coach Agent - Provides feedback on answers
        self.coach = AssistantAgent(
            name="Coach",
            model_client=self.model_client,
            description=f"Expert interview coach for {self.technology} and {self.position}",
            system_message=f"""You are an expert interview coach specializing in {self.technology} and {self.position} roles.

Your responsibilities:
- Analyze the candidate's answer to each interview question
- Identify strengths in the answer
- Point out areas for improvement
- Suggest better ways to structure or present the answer
- Provide specific examples of what a strong answer would include
- Be constructive and encouraging

Format your feedback as:
STRENGTHS: [What was good about the answer]
IMPROVEMENTS: [What could be better]
IDEAL ANSWER APPROACH: [How to structure a better response]

Keep feedback concise but actionable.""",
        )
        
        # 4. Scorer Agent - Scores each answer
        self.scorer = AssistantAgent(
            name="Scorer",
            model_client=self.model_client,
            description=f"Objective evaluator for {self.position} interviews",
            system_message=f"""You are an objective evaluator for {self.position} interviews focused on {self.technology}.

Your responsibilities:
- Score each answer on a scale of 0-10
- Consider: accuracy, completeness, depth, clarity, and practical understanding
- Provide brief justification for the score
- Be fair but maintain high standards appropriate for {self.position}

Format your response as:
SCORE: [X/10]
JUSTIFICATION: [Brief explanation of the score]

Be consistent in your scoring criteria.""",
        )
    
    async def get_next_question(self, question_number: int) -> str:
        """
        Get the next interview question
        
        Args:
            question_number: The current question number
            
        Returns:
            The interview question as a string
        """
        from autogen_core import CancellationToken
        from autogen_agentchat.messages import TextMessage
        
        context = ""
        if self.interview_history:
            context = f"\nPrevious questions and answers context (for follow-up):\n"
            for i, item in enumerate(self.interview_history[-2:], 1):  # Last 2 Q&A for context
                context += f"Q{i}: {item['question']}\nA{i}: {item['answer'][:100]}...\n"
        
        prompt = f"""This is question #{question_number} for the {self.position} position interview on {self.technology}.
{context}
Please ask ONE clear, relevant technical question. Just state the question directly."""
        
        # Get question from interviewer
        await self.interviewer.on_reset(CancellationToken())
        response = await self.interviewer.on_messages(
            [TextMessage(content=prompt, source="user")],
            CancellationToken()
        )
        
        return response.chat_message.content
    
    async def get_feedback(self, question: str, answer: str) -> str:
        """
        Get coaching feedback on the answer
        
        Args:
            question: The interview question
            answer: The candidate's answer
            
        Returns:
            Feedback from the coach
        """
        from autogen_core import CancellationToken
        from autogen_agentchat.messages import TextMessage
        
        prompt = f"""
Question asked: {question}

Candidate's answer: {answer}

Please provide constructive feedback on this answer."""
        
        await self.coach.on_reset(CancellationToken())
        response = await self.coach.on_messages(
            [TextMessage(content=prompt, source="user")],
            CancellationToken()
        )
        
        return response.chat_message.content
    
    async def get_score(self, question: str, answer: str) -> Tuple[int, str]:
        """
        Get score for the answer
        
        Args:
            question: The interview question
            answer: The candidate's answer
            
        Returns:
            Tuple of (score, justification)
        """
        from autogen_core import CancellationToken
        from autogen_agentchat.messages import TextMessage
        
        prompt = f"""
Question: {question}

Answer: {answer}

Please evaluate and score this answer."""
        
        await self.scorer.on_reset(CancellationToken())
        response = await self.scorer.on_messages(
            [TextMessage(content=prompt, source="user")],
            CancellationToken()
        )
        
        score_response = response.chat_message.content
        
        # Parse score from response
        score = 0
        justification = score_response
        
        try:
            if "SCORE:" in score_response:
                score_line = [line for line in score_response.split('\n') if 'SCORE:' in line][0]
                score_str = score_line.split('SCORE:')[1].strip().split('/')[0].strip()
                score = int(score_str)
        except:
            score = 5  # Default score if parsing fails
        
        return score, score_response
    
    async def process_answer(self, question: str, answer: str, question_number: int) -> Dict:
        """
        Process a complete Q&A cycle: get feedback and score
        
        Args:
            question: The interview question
            answer: The candidate's answer
            question_number: Current question number
            
        Returns:
            Dictionary containing feedback, score, and justification
        """
        # Get feedback from coach
        feedback = await self.get_feedback(question, answer)
        
        # Get score from scorer
        score, score_details = await self.get_score(question, answer)
        
        # Store in history
        qa_record = {
            'question_number': question_number,
            'question': question,
            'answer': answer,
            'feedback': feedback,
            'score': score,
            'score_details': score_details
        }
        
        self.interview_history.append(qa_record)
        self.scores.append(score)
        self.feedbacks.append(feedback)
        
        return qa_record
    
    async def get_overall_summary(self) -> Dict:
        """
        Get overall interview summary
        
        Returns:
            Dictionary with overall statistics and summary
        """
        from autogen_core import CancellationToken
        from autogen_agentchat.messages import TextMessage
        
        if not self.scores:
            return {
                'average_score': 0,
                'total_questions': 0,
                'summary': 'No questions answered yet.'
            }
        
        avg_score = sum(self.scores) / len(self.scores)
        
        summary_prompt = f"""
Based on this interview for {self.position} position on {self.technology}:
- Total questions: {len(self.scores)}
- Average score: {avg_score:.1f}/10
- Scores: {self.scores}

Provide a brief overall assessment of the candidate's performance (2-3 sentences).
Include strengths and areas for improvement."""
        
        await self.coach.on_reset(CancellationToken())
        response = await self.coach.on_messages(
            [TextMessage(content=summary_prompt, source="user")],
            CancellationToken()
        )
        
        overall_feedback = response.chat_message.content
        
        return {
            'average_score': round(avg_score, 2),
            'total_questions': len(self.scores),
            'scores': self.scores,
            'summary': overall_feedback,
            'history': self.interview_history
        }

