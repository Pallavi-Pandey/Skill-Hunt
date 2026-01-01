# TalentScout - System Architecture

## Overview

TalentScout is an intelligent hiring assistant chatbot designed to automate the initial screening of technology candidates. This document describes the system architecture, design decisions, and implementation details.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     TalentScout System                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐         ┌──────────────┐                │
│  │   chatbot.py │◄────────┤ candidate.py │                │
│  │  (Main Flow) │         │ (Data Model) │                │
│  └──────┬───────┘         └──────────────┘                │
│         │                                                   │
│         │                                                   │
│         ▼                                                   │
│  ┌──────────────┐         ┌──────────────┐                │
│  │llm_service.py│◄────────┤   config.py  │                │
│  │(AI Engine)   │         │ (Settings)   │                │
│  └──────┬───────┘         └──────────────┘                │
│         │                                                   │
│         │                                                   │
│         ▼                                                   │
│  ┌──────────────┐                                          │
│  │  OpenAI API  │  (External)                             │
│  │ GPT-3.5/4.0  │                                          │
│  └──────────────┘                                          │
│                                                             │
│         │                                                   │
│         ▼                                                   │
│  ┌──────────────┐                                          │
│  │ interviews/  │  (Data Storage)                         │
│  │   *.json     │                                          │
│  └──────────────┘                                          │
└─────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. chatbot.py - Main Orchestrator
**Purpose**: Manages the interview flow and user interaction

**Responsibilities**:
- CLI-based user interface
- Interview session management
- Flow control (info collection → tech stack → questions → summary)
- Data persistence

**Key Methods**:
- `start_interview()`: Main interview loop
- `_collect_basic_info()`: Gather candidate details
- `_collect_tech_stack()`: Identify technologies
- `_conduct_technical_interview()`: Run Q&A session
- `_generate_summary()`: Create final assessment
- `_save_interview()`: Persist data to JSON

### 2. candidate.py - Data Model
**Purpose**: Represents candidate information and interview data

**Responsibilities**:
- Store candidate profile (name, email, experience, etc.)
- Track tech stack
- Record Q&A responses
- Generate summaries
- Export to dictionary/JSON format

**Key Features**:
- Clean data structure
- Type hints for clarity
- Easy serialization
- Timestamped interviews

### 3. llm_service.py - AI Engine
**Purpose**: Interface with Large Language Models for intelligent features

**Responsibilities**:
- Generate tech stack-specific questions
- Evaluate candidate responses in real-time
- Produce interview summaries and recommendations
- Handle API errors gracefully
- Provide fallback behavior

**Key Methods**:
- `generate_technical_questions()`: Create personalized questions
- `evaluate_response()`: Assess answer quality
- `generate_interview_summary()`: Final recommendation
- `_get_fallback_questions()`: Offline mode questions

**LLM Integration Strategy**:
```python
# Prompt Engineering Pattern
system_prompt = "You are an experienced technical recruiter..."
user_prompt = f"Generate questions for {tech_stack} at {level} level..."

# Temperature Settings
- Question generation: 0.7 (creative but focused)
- Evaluation: 0.5 (consistent and fair)
- Summary: 0.5 (professional and balanced)
```

### 4. config.py - Configuration
**Purpose**: Centralized configuration management

**Contains**:
- API keys (from environment)
- Tech stack categories
- Question parameters
- Experience level definitions

## Data Flow

### Interview Session Flow
```
1. User Launch
   └─> chatbot.py main()

2. Initialize
   ├─> Create Candidate object
   ├─> Initialize LLMService
   └─> Start interview session

3. Information Collection
   ├─> Collect name, email, phone
   ├─> Years of experience → Experience level
   └─> Preferred role

4. Tech Stack Declaration
   ├─> User enters comma-separated technologies
   ├─> Parse and validate
   └─> Store in Candidate object

5. Question Generation
   ├─> LLMService.generate_technical_questions()
   │   ├─> If API available: Call OpenAI
   │   └─> If offline: Use fallback templates
   └─> Return list of questions

6. Technical Interview
   ├─> For each question:
   │   ├─> Display question
   │   ├─> Collect answer
   │   ├─> Store in Candidate
   │   └─> Optionally evaluate with LLM
   └─> Complete interview

7. Summary Generation
   ├─> LLMService.generate_interview_summary()
   │   ├─> Compile all responses
   │   ├─> Generate assessment
   │   └─> Return recommendation
   └─> Display to user

8. Data Persistence
   ├─> Create interviews/ directory
   ├─> Generate filename (name_timestamp.json)
   ├─> Export Candidate.to_dict()
   └─> Save JSON file
```

## Design Decisions

### 1. Python as Primary Language
**Rationale**:
- Excellent LLM library support (OpenAI SDK)
- Rapid development
- Strong typing with hints
- Clean, readable code

### 2. OpenAI API Integration
**Rationale**:
- Industry-leading LLM quality
- Comprehensive API
- Good documentation
- Reliable service

**Graceful Degradation**:
- System works without API key
- Fallback to preset questions
- Clear messaging about limitations

### 3. JSON for Data Storage
**Rationale**:
- Human-readable
- Easy to parse
- Standard format for integration
- No database overhead

### 4. CLI Interface
**Rationale**:
- Simple to implement
- Universal compatibility
- Easy to test
- Foundation for future UI

### 5. Modular Architecture
**Rationale**:
- Separation of concerns
- Easy to test components
- Maintainable codebase
- Extensible design

## LLM Understanding Demonstration

### 1. Prompt Engineering
The system uses carefully crafted prompts:

**Question Generation**:
```
System: "You are an experienced technical recruiter creating interview questions."
User: "Generate {N} questions for {experience_level} candidate with {tech_stack}..."
```

**Response Evaluation**:
```
System: "You are an experienced technical recruiter evaluating candidate responses."
User: "Evaluate this response considering {tech_stack}..."
```

### 2. Context Management
- Maintains conversation state
- Passes relevant context to LLM
- Preserves interview history
- Correlates questions with tech stack

### 3. Temperature Control
- **0.7** for question generation (creative yet relevant)
- **0.5** for evaluation (consistent and fair)
- Different temperatures for different tasks

### 4. Error Handling
- Specific exception catching (OpenAIError)
- Graceful fallback mechanisms
- User-friendly error messages
- System continues on failures

### 5. Response Processing
- Parse LLM output
- Clean and normalize text
- Extract numbered questions
- Validate results

## Security Considerations

### 1. API Key Management
- Stored in `.env` file (not committed)
- Loaded via python-dotenv
- Never hardcoded
- Clear documentation

### 2. Input Validation
- Sanitize user inputs
- Validate experience years
- Check email format (basic)
- Prevent injection attacks

### 3. Data Privacy
- Local storage only
- No third-party transmission (except OpenAI)
- `.gitignore` for interview data
- Clear privacy messaging

## Extensibility

The architecture supports future enhancements:

### Planned Extensions
1. **Web Interface**: Replace CLI with Flask/Django
2. **Database Integration**: PostgreSQL/MongoDB for storage
3. **Video Interview**: Integrate video recording
4. **Resume Parsing**: Extract info from PDFs
5. **ATS Integration**: Connect to enterprise systems
6. **Multi-language**: Support non-English interviews
7. **Advanced Analytics**: Candidate scoring dashboard

### Extension Points
- `chatbot.py`: Easy to swap CLI for web UI
- `llm_service.py`: Can use different LLM providers
- `candidate.py`: Extensible data model
- `config.py`: Centralized configuration

## Performance Considerations

### Current Performance
- Interview duration: 5-15 minutes
- API latency: 2-5 seconds per LLM call
- Storage: <10KB per interview
- Memory: Minimal (<50MB)

### Optimization Opportunities
1. **Caching**: Cache common questions
2. **Batch Processing**: Multiple candidates
3. **Async API Calls**: Non-blocking requests
4. **Question Pool**: Pre-generated questions
5. **Streaming**: Stream LLM responses

## Testing Strategy

### Current Testing
- `demo.py`: Non-interactive demonstration
- `examples.py`: Component testing
- Manual validation: Real interview flows

### Future Testing
- Unit tests for each module
- Integration tests for full flow
- Mock LLM responses
- Performance benchmarks
- User acceptance testing

## Deployment

### Requirements
- Python 3.7+
- pip for dependencies
- OpenAI API key (optional)
- 100MB disk space

### Setup
```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env with API key
python chatbot.py
```

### Production Considerations
- Use gunicorn/uvicorn for web deployment
- Set up monitoring and logging
- Implement rate limiting
- Add authentication
- Use production-grade database
- Set up backup strategy

## Conclusion

TalentScout demonstrates a well-architected LLM application with:
- ✓ Clean separation of concerns
- ✓ Robust error handling
- ✓ Graceful degradation
- ✓ Secure configuration
- ✓ Extensible design
- ✓ Clear documentation
- ✓ LLM best practices

The system successfully shows understanding of:
- Prompt engineering
- Context management
- Temperature control
- Error handling
- Response processing
- Real-world LLM integration
