"""
Example usage scenarios for TalentScout Hiring Assistant
"""
from candidate import Candidate
from llm_service import LLMService
from config import Config

def example_1_basic_candidate_creation():
    """Example 1: Creating and managing candidate information"""
    print("\n" + "="*60)
    print("Example 1: Basic Candidate Creation")
    print("="*60)
    
    candidate = Candidate()
    candidate.add_basic_info(
        name="Alex Johnson",
        email="alex.j@example.com",
        phone="+1-555-9876",
        years_of_experience=3,
        preferred_role="Backend Developer"
    )
    
    candidate.add_tech_stack(["Python", "Django", "PostgreSQL", "Redis"])
    
    # Add some responses
    candidate.add_response(
        "What is your experience with Python?",
        "I have 3 years of experience with Python, primarily using Django for web applications."
    )
    
    print(candidate.get_summary())
    print("\n✓ Candidate object created successfully")
    return candidate

def example_2_tech_stack_categories():
    """Example 2: Exploring tech stack categories"""
    print("\n" + "="*60)
    print("Example 2: Tech Stack Categories")
    print("="*60)
    
    print("\nAvailable technology categories in TalentScout:\n")
    for category, technologies in Config.TECH_STACKS.items():
        print(f"{category.upper()}:")
        for tech in technologies:
            print(f"  • {tech}")
        print()
    
    print("✓ You can customize these in config.py")

def example_3_llm_service_modes():
    """Example 3: LLM Service in different modes"""
    print("\n" + "="*60)
    print("Example 3: LLM Service Modes")
    print("="*60)
    
    llm_service = LLMService()
    
    if llm_service.is_available():
        print("\n✓ LLM Service: ENABLED")
        print(f"  Model: {Config.OPENAI_MODEL}")
        print("\nCapabilities:")
        print("  • Dynamic question generation")
        print("  • Real-time response evaluation")
        print("  • Comprehensive interview summaries")
    else:
        print("\n⚠ LLM Service: OFFLINE MODE")
        print("\nCapabilities:")
        print("  • Preset question templates")
        print("  • Basic data collection")
        print("  • Manual review process")
        print("\n💡 To enable LLM features:")
        print("  1. Set OPENAI_API_KEY in .env file")
        print("  2. Restart the application")

def example_4_experience_levels():
    """Example 4: Experience level classification"""
    print("\n" + "="*60)
    print("Example 4: Experience Level Classification")
    print("="*60)
    
    test_cases = [
        (1, "Junior"),
        (3, "Mid-level"),
        (7, "Senior")
    ]
    
    print("\nExperience level mapping:")
    for years, level in test_cases:
        print(f"  {years} year(s) → {level}")
    
    print("\nThis affects:")
    print("  • Question difficulty")
    print("  • Technical depth expected")
    print("  • Evaluation criteria")

def example_5_question_generation():
    """Example 5: Question generation for different stacks"""
    print("\n" + "="*60)
    print("Example 5: Question Generation Examples")
    print("="*60)
    
    llm_service = LLMService()
    
    test_scenarios = [
        (["JavaScript", "React", "Node.js"], "junior"),
        (["Python", "Django", "PostgreSQL"], "mid-level"),
        (["Java", "Spring Boot", "Kubernetes"], "senior")
    ]
    
    for tech_stack, level in test_scenarios:
        print(f"\n{level.upper()} level - {', '.join(tech_stack)}:")
        questions = llm_service.generate_technical_questions(
            tech_stack, level, num_questions=3
        )
        for idx, q in enumerate(questions, 1):
            print(f"  {idx}. {q}")

def example_6_data_export():
    """Example 6: Data export and integration"""
    print("\n" + "="*60)
    print("Example 6: Data Export for Integration")
    print("="*60)
    
    candidate = Candidate()
    candidate.add_basic_info(
        name="Sarah Chen",
        email="sarah.chen@example.com",
        phone="+1-555-1234",
        years_of_experience=5,
        preferred_role="DevOps Engineer"
    )
    candidate.add_tech_stack(["Docker", "Kubernetes", "AWS", "Terraform"])
    candidate.add_response(
        "Describe your CI/CD experience",
        "I've implemented CI/CD pipelines using Jenkins and GitLab CI"
    )
    
    import json
    data = candidate.to_dict()
    
    print("\nJSON Export Format:")
    print(json.dumps(data, indent=2))
    print("\n✓ This format can be easily integrated with:")
    print("  • Applicant Tracking Systems (ATS)")
    print("  • HR Management Software")
    print("  • Database systems")
    print("  • API endpoints")

def main():
    """Run all examples"""
    print("\n" + "="*70)
    print("   TalentScout Hiring Assistant - Usage Examples   ".center(70))
    print("="*70)
    
    examples = [
        example_1_basic_candidate_creation,
        example_2_tech_stack_categories,
        example_3_llm_service_modes,
        example_4_experience_levels,
        example_5_question_generation,
        example_6_data_export
    ]
    
    for example_func in examples:
        try:
            example_func()
        except Exception as e:
            print(f"\n❌ Example failed: {e}")
    
    print("\n" + "="*70)
    print("   All Examples Completed   ".center(70))
    print("="*70)
    print("\n📚 For more information, see README.md")
    print("🚀 To run the chatbot: python chatbot.py")
    print("🎯 To run the demo: python demo.py")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
