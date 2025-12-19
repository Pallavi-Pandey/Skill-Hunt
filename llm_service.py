"""
LLM Service module for interacting with OpenAI API
"""
from typing import List, Dict
from openai import OpenAI
from config import Config

class LLMService:
    """Service class for LLM interactions"""
    
    def __init__(self):
        """Initialize the LLM service"""
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY) if Config.OPENAI_API_KEY else None
        self.model = Config.OPENAI_MODEL
        self.conversation_history: List[Dict[str, str]] = []
        
    def is_available(self) -> bool:
        """Check if LLM service is available"""
        return self.client is not None and Config.OPENAI_API_KEY != ''
    
    def generate_technical_questions(self, tech_stack: List[str], 
                                     experience_level: str,
                                     num_questions: int = 5) -> List[str]:
        """
        Generate technical questions based on candidate's tech stack
        
        Args:
            tech_stack: List of technologies the candidate knows
            experience_level: junior, mid-level, or senior
            num_questions: Number of questions to generate
            
        Returns:
            List of technical questions
        """
        if not self.is_available():
            return self._get_fallback_questions(tech_stack, experience_level)
        
        tech_list = ", ".join(tech_stack)
        
        prompt = f"""As a technical recruiter for TalentScout, generate {num_questions} relevant technical interview questions for a {experience_level} level candidate with the following tech stack: {tech_list}.

Requirements:
1. Questions should be appropriate for {experience_level} level
2. Cover different aspects: theory, practical scenarios, and problem-solving
3. Be specific to the technologies mentioned
4. Range from fundamental concepts to more advanced topics
5. Be clear and concise

Return only the questions, numbered 1 through {num_questions}."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an experienced technical recruiter creating interview questions."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            questions_text = response.choices[0].message.content
            questions = [q.strip() for q in questions_text.split('\n') if q.strip() and q.strip()[0].isdigit()]
            
            # Clean up the questions (remove numbering)
            cleaned_questions = []
            for q in questions:
                # Remove leading numbers and dots/parentheses
                clean_q = q.lstrip('0123456789.) ').strip()
                if clean_q:
                    cleaned_questions.append(clean_q)
            
            return cleaned_questions[:num_questions]
            
        except Exception as e:
            print(f"Error generating questions with LLM: {e}")
            return self._get_fallback_questions(tech_stack, experience_level)
    
    def evaluate_response(self, question: str, answer: str, tech_stack: List[str]) -> str:
        """
        Evaluate a candidate's response to a technical question
        
        Args:
            question: The technical question asked
            answer: The candidate's answer
            tech_stack: Candidate's tech stack for context
            
        Returns:
            Evaluation feedback
        """
        if not self.is_available():
            return "Response recorded. (LLM evaluation unavailable - please configure OPENAI_API_KEY)"
        
        tech_list = ", ".join(tech_stack)
        
        prompt = f"""As a technical recruiter, evaluate this candidate's response:

Tech Stack: {tech_list}
Question: {question}
Answer: {answer}

Provide a brief, constructive evaluation (2-3 sentences) covering:
1. Correctness of the answer
2. Depth of understanding
3. Any suggestions for improvement"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an experienced technical recruiter evaluating candidate responses."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=200
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error evaluating response: {e}")
            return "Response recorded. (Evaluation error)"
    
    def generate_interview_summary(self, candidate_info: dict) -> str:
        """
        Generate a summary and recommendation for the candidate
        
        Args:
            candidate_info: Dictionary containing candidate information
            
        Returns:
            Summary and recommendation
        """
        if not self.is_available():
            return self._get_fallback_summary(candidate_info)
        
        prompt = f"""As a technical recruiter, provide a summary and recommendation for this candidate:

Name: {candidate_info['name']}
Experience: {candidate_info['years_of_experience']} years
Role: {candidate_info['preferred_role']}
Tech Stack: {', '.join(candidate_info['tech_stack'])}

Technical Interview Responses:
"""
        for idx, (question, answer) in enumerate(candidate_info['responses'].items(), 1):
            prompt += f"\nQ{idx}: {question}\nA{idx}: {answer}\n"
        
        prompt += """\nProvide:
1. Overall assessment (2-3 sentences)
2. Key strengths
3. Areas for improvement
4. Hiring recommendation (Strong Yes/Yes/Maybe/No) with brief justification"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an experienced technical recruiter providing hiring recommendations."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=500
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating summary: {e}")
            return self._get_fallback_summary(candidate_info)
    
    def _get_fallback_questions(self, tech_stack: List[str], experience_level: str) -> List[str]:
        """Fallback questions when LLM is not available"""
        questions = []
        
        for tech in tech_stack[:3]:  # Limit to first 3 technologies
            if experience_level == 'junior':
                questions.append(f"What is your understanding of {tech} and where have you used it?")
            elif experience_level == 'mid-level':
                questions.append(f"Describe a challenging problem you solved using {tech}.")
            else:  # senior
                questions.append(f"How would you architect a scalable system using {tech}? What are the key considerations?")
        
        # Add some general questions
        questions.append("Describe your approach to debugging a production issue.")
        questions.append("How do you stay updated with the latest technologies in your field?")
        
        return questions[:Config.MIN_QUESTIONS_PER_STACK]
    
    def _get_fallback_summary(self, candidate_info: dict) -> str:
        """Fallback summary when LLM is not available"""
        return f"""
Interview Summary:
- Candidate has {candidate_info['years_of_experience']} years of experience
- Tech Stack: {', '.join(candidate_info['tech_stack'])}
- Completed {len(candidate_info['responses'])} technical questions
- Role: {candidate_info['preferred_role']}

Note: Full AI-powered assessment unavailable. Please configure OPENAI_API_KEY for detailed analysis.
"""
