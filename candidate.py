"""
Candidate data model for storing candidate information
"""
from typing import List, Dict
from datetime import datetime

class Candidate:
    """Represents a candidate in the recruitment process"""
    
    def __init__(self):
        self.name = ""
        self.email = ""
        self.phone = ""
        self.years_of_experience = 0
        self.tech_stack: List[str] = []
        self.preferred_role = ""
        self.responses: Dict[str, str] = {}
        self.interview_date = datetime.now().isoformat()
        
    def add_basic_info(self, name: str, email: str, phone: str, 
                      years_of_experience: int, preferred_role: str):
        """Add basic candidate information"""
        self.name = name
        self.email = email
        self.phone = phone
        self.years_of_experience = years_of_experience
        self.preferred_role = preferred_role
        
    def add_tech_stack(self, tech_stack: List[str]):
        """Add candidate's tech stack"""
        self.tech_stack = tech_stack
        
    def add_response(self, question: str, answer: str):
        """Add a question-answer pair"""
        self.responses[question] = answer
        
    def get_summary(self) -> str:
        """Get a formatted summary of the candidate"""
        summary = f"""
=== Candidate Information ===
Name: {self.name}
Email: {self.email}
Phone: {self.phone}
Experience: {self.years_of_experience} years
Preferred Role: {self.preferred_role}
Tech Stack: {', '.join(self.tech_stack)}
Interview Date: {self.interview_date}

=== Technical Responses ===
"""
        for idx, (question, answer) in enumerate(self.responses.items(), 1):
            summary += f"\nQ{idx}: {question}\nA{idx}: {answer}\n"
            
        return summary
    
    def to_dict(self) -> dict:
        """Convert candidate to dictionary format"""
        return {
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'years_of_experience': self.years_of_experience,
            'preferred_role': self.preferred_role,
            'tech_stack': self.tech_stack,
            'responses': self.responses,
            'interview_date': self.interview_date
        }
