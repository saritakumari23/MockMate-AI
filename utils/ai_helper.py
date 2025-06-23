import openai
import json
from typing import Dict, List, Tuple
from config import Config

class AIHelper:
    """Helper class for OpenAI API interactions."""
    
    def __init__(self):
        """Initialize the AI helper with OpenAI configuration."""
        openai.api_key = Config.OPENAI_API_KEY
        self.model = Config.OPENAI_MODEL
        self.max_tokens = Config.OPENAI_MAX_TOKENS
        self.temperature = Config.OPENAI_TEMPERATURE
    
    def generate_question(self, user_profile: Dict, category: str, difficulty: str) -> str:
        """
        Generate an interview question based on user profile and parameters.
        
        Args:
            user_profile: Dictionary containing user information
            category: Question category (behavioral, technical, etc.)
            difficulty: Difficulty level (beginner, intermediate, advanced)
            
        Returns:
            Generated interview question
        """
        prompt = self._build_question_prompt(user_profile, category, difficulty)
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert interview coach. Generate relevant, challenging interview questions."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating question: {e}")
            return self._get_fallback_question(category, difficulty)
    
    def evaluate_response(self, question: str, user_response: str, category: str) -> Dict:
        """
        Evaluate user's response to an interview question.
        
        Args:
            question: The interview question
            user_response: User's response
            category: Question category
            
        Returns:
            Dictionary containing evaluation results
        """
        prompt = self._build_evaluation_prompt(question, user_response, category)
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert interview evaluator. Provide constructive feedback."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=0.3
            )
            
            evaluation_text = response.choices[0].message.content.strip()
            return self._parse_evaluation(evaluation_text)
        except Exception as e:
            print(f"Error evaluating response: {e}")
            return self._get_fallback_evaluation()
    
    def generate_qa_feedback(self, questions_answers: List[Tuple[str, str]], role: str = "General") -> str:
        """
        Generate structured feedback for a list of Q&A pairs.
        
        Args:
            questions_answers: List of tuples containing (question, answer) pairs
            role: The role/position being interviewed for
            
        Returns:
            Formatted feedback string with the requested structure
        """
        prompt = self._build_qa_feedback_prompt(questions_answers, role)
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert interview coach providing detailed, constructive feedback. Use the exact format requested with ✅, ⚠️, and 💡 symbols."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating Q&A feedback: {e}")
            return self._get_fallback_qa_feedback(questions_answers)
    
    def generate_role_questions(self, role: str, num_questions: int = 3) -> List[str]:
        """
        Generate interview questions based on a specific role.
        
        Args:
            role: The role/position to generate questions for
            num_questions: Number of questions to generate
            
        Returns:
            List of generated questions
        """
        prompt = self._build_role_questions_prompt(role, num_questions)
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert interview coach. Generate relevant, challenging interview questions for the specified role."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            questions_text = response.choices[0].message.content.strip()
            return self._parse_questions_list(questions_text)
        except Exception as e:
            print(f"Error generating role questions: {e}")
            return self._get_fallback_role_questions(role, num_questions)
    
    def _build_qa_feedback_prompt(self, questions_answers: List[Tuple[str, str]], role: str) -> str:
        """Build prompt for Q&A feedback generation."""
        prompt = f"""You will receive a list of interview questions and candidate answers for a {role} position. For each one, give:
- Positive feedback (what the answer did well)
- Areas to improve
- One specific tip to make the answer better

Format like this:
---
Question 1: <question>
Candidate Answer: <answer>
✅ Strengths:
⚠️ Weaknesses:
💡 Suggestion:
---

Here is the Q&A list:"""
        
        for i, (q, a) in enumerate(questions_answers, 1):
            prompt += f"\nQuestion {i}: {q}\nCandidate Answer: {a}\n"
        
        return prompt
    
    def _build_role_questions_prompt(self, role: str, num_questions: int) -> str:
        """Build prompt for role-specific question generation."""
        return f"""Generate {num_questions} interview questions for a {role} position. 
Include a mix of:
- Behavioral questions (about past experiences)
- Technical questions (role-specific skills)
- Situational questions (how they would handle scenarios)

Make the questions specific to the {role} role and return them as a numbered list.
Each question should be challenging but appropriate for the position level."""
    
    def _parse_questions_list(self, questions_text: str) -> List[str]:
        """Parse questions from AI response."""
        questions = []
        lines = questions_text.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('Q')):
                # Remove numbering and clean up
                question = line
                if '. ' in line:
                    question = line.split('. ', 1)[1]
                elif ': ' in line:
                    question = line.split(': ', 1)[1]
                questions.append(question)
        
        return questions if questions else self._get_fallback_role_questions("General", 3)
    
    def _get_fallback_qa_feedback(self, questions_answers: List[Tuple[str, str]]) -> str:
        """Get fallback feedback when AI generation fails."""
        feedback = ""
        for i, (question, answer) in enumerate(questions_answers, 1):
            feedback += f"""---
Question {i}: {question}
Candidate Answer: {answer}
✅ Strengths:
- Attempted to answer the question
- Showed some understanding of the topic

⚠️ Weaknesses:
- Response could be more detailed
- Missing specific examples
- Could improve structure

💡 Suggestion:
- Use the STAR method (Situation, Task, Action, Result) to structure your response
- Provide specific examples from your experience
- Be more concise and focused

---
"""
        return feedback
    
    def _get_fallback_role_questions(self, role: str, num_questions: int) -> List[str]:
        """Get fallback questions when AI generation fails."""
        fallback_questions = {
            "software_engineer": [
                "Tell me about a challenging technical problem you solved recently.",
                "How do you approach debugging a complex system issue?",
                "Describe a time when you had to learn a new technology quickly."
            ],
            "data_scientist": [
                "Walk me through a data analysis project you worked on.",
                "How do you handle missing or inconsistent data?",
                "Explain a machine learning model you've implemented."
            ],
            "product_manager": [
                "How do you prioritize features in a product roadmap?",
                "Tell me about a time you had to make a difficult product decision.",
                "How do you gather and analyze user feedback?"
            ]
        }
        
        return fallback_questions.get(role.lower().replace(" ", "_"), [
            "Tell me about yourself and your background.",
            "What are your greatest strengths and weaknesses?",
            "Where do you see yourself in 5 years?"
        ])[:num_questions]
    
    def _build_question_prompt(self, user_profile: Dict, category: str, difficulty: str) -> str:
        """Build prompt for question generation."""
        return f"""
        Generate an interview question for a {difficulty} level {category} interview.
        
        User Profile:
        - Career Field: {user_profile.get('career_field', 'General')}
        - Experience Level: {user_profile.get('experience_level', 'Entry Level')}
        - Target Role: {user_profile.get('target_role', 'General Position')}
        
        Requirements:
        - Category: {category}
        - Difficulty: {difficulty}
        - Make it specific to their career field
        - Ensure it's appropriate for their experience level
        - Return only the question, no additional text
        """
    
    def _build_evaluation_prompt(self, question: str, user_response: str, category: str) -> str:
        """Build prompt for response evaluation."""
        return f"""
        Evaluate this interview response and provide structured feedback.
        
        Question: {question}
        Category: {category}
        Response: {user_response}
        
        Please provide evaluation in the following JSON format:
        {{
            "score": 1-10,
            "strengths": ["strength1", "strength2"],
            "weaknesses": ["weakness1", "weakness2"],
            "feedback": "detailed feedback text",
            "improvement_areas": ["area1", "area2"],
            "resources": ["resource1", "resource2"]
        }}
        """
    
    def _parse_evaluation(self, evaluation_text: str) -> Dict:
        """Parse evaluation response from AI."""
        try:
            # Try to extract JSON from the response
            if '{' in evaluation_text and '}' in evaluation_text:
                start = evaluation_text.find('{')
                end = evaluation_text.rfind('}') + 1
                json_str = evaluation_text[start:end]
                return json.loads(json_str)
        except:
            pass
        
        # Fallback parsing
        return {
            "score": 7,
            "strengths": ["Good attempt at answering the question"],
            "weaknesses": ["Could provide more specific examples"],
            "feedback": evaluation_text,
            "improvement_areas": ["Provide more concrete examples", "Structure your response better"],
            "resources": ["Interview preparation guides", "STAR method resources"]
        }
    
    def _get_fallback_question(self, category: str, difficulty: str) -> str:
        """Get fallback questions when AI generation fails."""
        fallback_questions = {
            'behavioral': {
                'beginner': 'Tell me about a time when you had to work with a difficult team member.',
                'intermediate': 'Describe a situation where you had to adapt to a significant change at work.',
                'advanced': 'Tell me about a time when you had to make a difficult decision with limited information.'
            },
            'technical': {
                'beginner': 'What programming languages are you most comfortable with?',
                'intermediate': 'How would you approach debugging a complex system issue?',
                'advanced': 'Explain how you would design a scalable architecture for a high-traffic application.'
            }
        }
        
        return fallback_questions.get(category, {}).get(difficulty, 'Tell me about yourself.')
    
    def _get_fallback_evaluation(self) -> Dict:
        """Get fallback evaluation when AI evaluation fails."""
        return {
            "score": 6,
            "strengths": ["Attempted to answer the question"],
            "weaknesses": ["Response could be more detailed"],
            "feedback": "Your response shows effort, but could benefit from more specific examples and structure.",
            "improvement_areas": ["Provide specific examples", "Use the STAR method", "Be more concise"],
            "resources": ["Interview preparation guides", "STAR method resources"]
        } 