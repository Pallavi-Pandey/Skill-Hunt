"""
LLM Service module for interacting with Google Gemini API
"""
from typing import List, Dict
from google import genai
from groq import Groq
from config import Config

class LLMService:
    """Service class for LLM interactions supporting multiple providers"""
    
    def __init__(self, provider: str = "gemini"):
        """Initialize the LLM service with a specific provider"""
        self.provider = provider
        self.gemini_client = None
        self.groq_client = None
        
        if Config.GEMINI_API_KEY:
            self.gemini_client = genai.Client(api_key=Config.GEMINI_API_KEY)
            
        if Config.GROQ_API_KEY:
            self.groq_client = Groq(api_key=Config.GROQ_API_KEY)
            
        self.conversation_history: List[Dict[str, str]] = []
        
    def is_available(self) -> bool:
        """Check if selected LLM service is available"""
        if self.provider == "gemini":
            return self.gemini_client is not None
        elif self.provider == "groq":
            return self.groq_client is not None
        return False
    
    def generate_technical_questions(self, tech_stack: List[str], 
                                     experience_level: str,
                                     num_questions: int = 5) -> List[str]:
        """
        Generate technical questions based on candidate's tech stack
        """
        if not self.is_available():
            return self._get_fallback_questions(tech_stack, experience_level)
        
        tech_list = ", ".join(tech_stack)
        
        prompt = f"""As a technical recruiter for SkillHunt, generate {num_questions} relevant technical interview questions for a {experience_level} level candidate with the following tech stack: {tech_list}.

Requirements:
1. Questions should be appropriate for {experience_level} level
2. Cover different aspects: theory, practical scenarios, and problem-solving
3. Be specific to the technologies mentioned
4. Range from fundamental concepts to more advanced topics
5. Be clear and concise

Return only the questions, numbered 1 through {num_questions}."""

        try:
            if self.provider == "gemini":
                response = self.gemini_client.models.generate_content(
                    model=Config.GEMINI_MODEL,
                    contents=prompt,
                    config=genai.types.GenerateContentConfig(
                        temperature=0.7,
                        max_output_tokens=1000
                    )
                )
                questions_text = response.text
            else:  # groq
                completion = self.groq_client.chat.completions.create(
                    model=Config.GROQ_MODEL,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=1000,
                )
                questions_text = completion.choices[0].message.content
            
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
            return self._get_fallback_questions(tech_stack, experience_level, num_questions)
    
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
            return "Response recorded. (LLM evaluation unavailable - please configure GEMINI_API_KEY)"
        
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
            if self.provider == "gemini":
                response = self.gemini_client.models.generate_content(
                    model=Config.GEMINI_MODEL,
                    contents=prompt,
                    config=genai.types.GenerateContentConfig(
                        temperature=0.5,
                        max_output_tokens=200
                    )
                )
                return response.text.strip()
            else:  # groq
                completion = self.groq_client.chat.completions.create(
                    model=Config.GROQ_MODEL,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.5,
                    max_tokens=200,
                )
                return completion.choices[0].message.content.strip()
            
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
            if self.provider == "gemini":
                response = self.gemini_client.models.generate_content(
                    model=Config.GEMINI_MODEL,
                    contents=prompt,
                    config=genai.types.GenerateContentConfig(
                        temperature=0.5,
                        max_output_tokens=500
                    )
                )
                return response.text.strip()
            else:  # groq
                completion = self.groq_client.chat.completions.create(
                    model=Config.GROQ_MODEL,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.5,
                    max_tokens=500,
                )
                return completion.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating summary: {e}")
            return self._get_fallback_summary(candidate_info)
    
    def _get_fallback_questions(self, tech_stack: List[str], experience_level: str, num_questions: int = None) -> List[str]:
        """Fallback questions when LLM is not available"""
        if num_questions is None:
            num_questions = Config.MIN_QUESTIONS_PER_STACK
            
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
        
        return questions[:num_questions]
    
    def _get_fallback_summary(self, candidate_info: dict) -> str:
        """Fallback summary when LLM is not available"""
        return f"""
Interview Summary:
- Candidate has {candidate_info['years_of_experience']} years of experience
- Tech Stack: {', '.join(candidate_info['tech_stack'])}
- Completed {len(candidate_info['responses'])} technical questions
- Role: {candidate_info['preferred_role']}

Note: Full AI-powered assessment unavailable. Please configure GEMINI_API_KEY for detailed analysis.
"""
