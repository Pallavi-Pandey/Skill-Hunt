"""
TalentScout Hiring Assistant Chatbot
Main chatbot orchestration module
"""
import json
import os
from typing import List, Optional
from datetime import datetime
from candidate import Candidate
from llm_service import LLMService
from config import Config

class TalentScoutChatbot:
    """Main chatbot class for conducting candidate interviews"""
    
    def __init__(self):
        """Initialize the chatbot"""
        self.llm_service = LLMService()
        self.candidate: Optional[Candidate] = None
        self.current_questions: List[str] = []
        self.current_question_index = 0
        
    def start_interview(self):
        """Start a new interview session"""
        self.candidate = Candidate()
        self.current_questions = []
        self.current_question_index = 0
        
        print("\n" + "="*60)
        print("   Welcome to TalentScout Hiring Assistant   ".center(60))
        print("="*60)
        print("\nHello! I'm your AI-powered hiring assistant.")
        print("I'll help screen your application for technology positions.")
        print("Let's get started!\n")
        
        # Collect basic information
        self._collect_basic_info()
        
        # Collect tech stack
        self._collect_tech_stack()
        
        # Generate and ask technical questions
        self._conduct_technical_interview()
        
        # Generate summary
        self._generate_summary()
        
        # Save interview data
        self._save_interview()
        
    def _collect_basic_info(self):
        """Collect basic candidate information"""
        print("\n--- Basic Information ---\n")
        
        name = input("What's your full name? ").strip()
        email = input("What's your email address? ").strip()
        phone = input("What's your phone number? ").strip()
        
        while True:
            try:
                years_exp = int(input("How many years of professional experience do you have? ").strip())
                if years_exp < 0:
                    print("Please enter a valid number of years.")
                    continue
                break
            except ValueError:
                print("Please enter a valid number.")
        
        role = input("What role are you applying for? (e.g., Full Stack Developer, Backend Engineer) ").strip()
        
        self.candidate.add_basic_info(name, email, phone, years_exp, role)
        
        print(f"\nThank you, {name}! Let's talk about your technical skills.")
        
    def _collect_tech_stack(self):
        """Collect candidate's tech stack"""
        print("\n--- Technical Skills ---\n")
        
        print("Please list the technologies you're proficient in.")
        print("You can mention programming languages, frameworks, databases, tools, etc.")
        print("\nExample tech stacks from our database:")
        for category, techs in Config.TECH_STACKS.items():
            print(f"  {category.capitalize()}: {', '.join(techs[:3])}...")
        
        print("\nEnter your tech stack (comma-separated):")
        tech_input = input("> ").strip()
        
        # Parse tech stack
        tech_stack = [tech.strip() for tech in tech_input.split(',') if tech.strip()]
        
        if not tech_stack:
            print("\nNo technologies entered. Let's try again.")
            return self._collect_tech_stack()
        
        self.candidate.add_tech_stack(tech_stack)
        
        print(f"\nGreat! I see you work with: {', '.join(tech_stack)}")
        print("Now I'll ask you some technical questions based on your skills.")
        
    def _conduct_technical_interview(self):
        """Conduct the technical interview"""
        print("\n--- Technical Interview ---\n")
        
        # Determine experience level
        years = self.candidate.years_of_experience
        if years < 2:
            experience_level = 'junior'
        elif years < 5:
            experience_level = 'mid-level'
        else:
            experience_level = 'senior'
        
        print(f"Based on your {years} years of experience, I'll ask {experience_level} level questions.")
        
        # Check if LLM is available
        if not self.llm_service.is_available():
            print("\nNote: Running in offline mode with preset questions.")
            print("For AI-powered dynamic questions, please configure your OpenAI API key in .env file.\n")
        else:
            print("\nGenerating personalized questions using AI...\n")
        
        # Generate questions
        self.current_questions = self.llm_service.generate_technical_questions(
            self.candidate.tech_stack,
            experience_level,
            num_questions=Config.MIN_QUESTIONS_PER_STACK
        )
        
        # Ask questions
        for idx, question in enumerate(self.current_questions, 1):
            print(f"\nQuestion {idx}/{len(self.current_questions)}:")
            print(f"{question}")
            print("\nYour answer:")
            answer = input("> ").strip()
            
            if not answer:
                answer = "[No response provided]"
            
            self.candidate.add_response(question, answer)
            
            # Provide immediate feedback if LLM is available
            if self.llm_service.is_available() and answer != "[No response provided]":
                print("\n💭 Evaluating your response...")
                feedback = self.llm_service.evaluate_response(
                    question, 
                    answer, 
                    self.candidate.tech_stack
                )
                print(f"\nFeedback: {feedback}")
        
        print("\n✅ Technical interview completed!")
        
    def _generate_summary(self):
        """Generate and display interview summary"""
        print("\n" + "="*60)
        print("   Interview Summary   ".center(60))
        print("="*60)
        
        candidate_dict = self.candidate.to_dict()
        
        if self.llm_service.is_available():
            print("\n🤖 Generating AI-powered assessment...\n")
            summary = self.llm_service.generate_interview_summary(candidate_dict)
            print(summary)
        else:
            print(self.candidate.get_summary())
        
        print("\n" + "="*60)
        
    def _save_interview(self):
        """Save interview data to file"""
        # Create interviews directory if it doesn't exist
        os.makedirs('interviews', exist_ok=True)
        
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = "".join(c for c in self.candidate.name if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_name = safe_name.replace(' ', '_')
        filename = f"interviews/{safe_name}_{timestamp}.json"
        
        # Save to JSON
        with open(filename, 'w') as f:
            json.dump(self.candidate.to_dict(), f, indent=2)
        
        print(f"\n💾 Interview data saved to: {filename}")
        print("\nThank you for your time! Our team will review your responses and get back to you soon.")
        print("Good luck! 🚀")

def main():
    """Main entry point"""
    chatbot = TalentScoutChatbot()
    
    try:
        chatbot.start_interview()
    except KeyboardInterrupt:
        print("\n\nInterview interrupted. Thank you for your time!")
    except Exception as e:
        print(f"\n\nAn error occurred: {e}")
        print("Please try again or contact support.")

if __name__ == "__main__":
    main()
