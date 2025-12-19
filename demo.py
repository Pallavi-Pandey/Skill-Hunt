"""
Demo script to showcase TalentScout Hiring Assistant functionality
This script simulates an interview without requiring user input
"""
from candidate import Candidate
from llm_service import LLMService
from config import Config
import json

def run_demo():
    """Run a demonstration of the chatbot features"""
    
    print("\n" + "="*70)
    print("   TalentScout Hiring Assistant - Demo Mode   ".center(70))
    print("="*70)
    
    print("\n📋 This demo showcases the chatbot's capabilities:")
    print("   ✓ Candidate information management")
    print("   ✓ Tech stack analysis")
    print("   ✓ Dynamic question generation")
    print("   ✓ Interview data persistence")
    print("   ✓ LLM integration (when API key is configured)")
    
    # Create a sample candidate
    print("\n" + "-"*70)
    print("1. Creating Sample Candidate Profile")
    print("-"*70)
    
    candidate = Candidate()
    candidate.add_basic_info(
        name="Jane Smith",
        email="jane.smith@example.com",
        phone="+1-555-0123",
        years_of_experience=5,
        preferred_role="Senior Full Stack Developer"
    )
    
    tech_stack = ["React", "Node.js", "TypeScript", "MongoDB", "Docker", "AWS"]
    candidate.add_tech_stack(tech_stack)
    
    print(f"✓ Name: {candidate.name}")
    print(f"✓ Email: {candidate.email}")
    print(f"✓ Experience: {candidate.years_of_experience} years")
    print(f"✓ Role: {candidate.preferred_role}")
    print(f"✓ Tech Stack: {', '.join(candidate.tech_stack)}")
    
    # Initialize LLM service
    print("\n" + "-"*70)
    print("2. Initializing LLM Service")
    print("-"*70)
    
    llm_service = LLMService()
    
    if llm_service.is_available():
        print("✓ OpenAI API connection established")
        print(f"✓ Using model: {Config.OPENAI_MODEL}")
    else:
        print("⚠ Running in offline mode (API key not configured)")
        print("✓ Fallback question system active")
    
    # Generate technical questions
    print("\n" + "-"*70)
    print("3. Generating Technical Questions")
    print("-"*70)
    
    experience_level = "senior" if candidate.years_of_experience >= 5 else \
                      "mid-level" if candidate.years_of_experience >= 2 else "junior"
    
    print(f"Experience Level: {experience_level}")
    print(f"Generating {Config.MIN_QUESTIONS_PER_STACK} questions based on tech stack...")
    
    questions = llm_service.generate_technical_questions(
        tech_stack,
        experience_level,
        num_questions=Config.MIN_QUESTIONS_PER_STACK
    )
    
    print(f"\n✓ Generated {len(questions)} questions:\n")
    for idx, question in enumerate(questions, 1):
        print(f"{idx}. {question}")
    
    # Simulate candidate responses
    print("\n" + "-"*70)
    print("4. Recording Sample Responses")
    print("-"*70)
    
    sample_responses = [
        "React's Virtual DOM is an in-memory representation of the real DOM. It works by creating a lightweight copy of the DOM tree, and when state changes occur, React compares the new Virtual DOM with the previous one using a diffing algorithm. Only the differences are then updated in the real DOM, which minimizes expensive DOM operations and improves performance.",
        "In Node.js, I've built RESTful APIs using Express.js, implemented JWT authentication, and used middleware for error handling. I've also worked with async/await patterns for handling asynchronous operations and integrated with databases like MongoDB using Mongoose ODM.",
        "For scalability, I would use a microservices architecture with Node.js services, implement load balancing, use Redis for caching, set up horizontal scaling with container orchestration, and ensure proper monitoring and logging. Database sharding and read replicas would handle data scaling."
    ]
    
    for idx, (question, answer) in enumerate(zip(questions[:3], sample_responses), 1):
        candidate.add_response(question, answer)
        print(f"\n✓ Response {idx} recorded")
        print(f"  Q: {question[:80]}...")
        print(f"  A: {answer[:80]}...")
    
    # Display candidate summary
    print("\n" + "-"*70)
    print("5. Interview Summary")
    print("-"*70)
    
    print(candidate.get_summary())
    
    # Generate AI assessment if available
    if llm_service.is_available():
        print("\n" + "-"*70)
        print("6. AI-Powered Assessment")
        print("-"*70)
        print("\n🤖 Generating comprehensive evaluation...\n")
        
        try:
            assessment = llm_service.generate_interview_summary(candidate.to_dict())
            print(assessment)
        except Exception as e:
            print(f"⚠ Assessment generation failed: {e}")
    
    # Save interview data
    print("\n" + "-"*70)
    print("7. Data Persistence")
    print("-"*70)
    
    demo_data = candidate.to_dict()
    print("\n✓ Interview data structure:")
    print(json.dumps(demo_data, indent=2))
    
    print("\n" + "="*70)
    print("   Demo Completed Successfully!   ".center(70))
    print("="*70)
    
    print("\n📚 Key Features Demonstrated:")
    print("   ✓ Structured candidate data collection")
    print("   ✓ Tech stack-aware question generation")
    print("   ✓ Experience level adaptation")
    print("   ✓ Response recording and evaluation")
    print("   ✓ Comprehensive interview summaries")
    print("   ✓ JSON data export for integration")
    
    print("\n🚀 To run the full interactive chatbot:")
    print("   python chatbot.py")
    
    print("\n💡 To enable AI features:")
    print("   1. Copy .env.example to .env")
    print("   2. Add your OpenAI API key")
    print("   3. Run the chatbot again")
    
    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    try:
        run_demo()
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        import traceback
        traceback.print_exc()
