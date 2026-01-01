# Usage Examples

This document provides detailed examples of how to interact with the TalentScout Hiring Assistant.

## Example Conversation Flow

### 1. Initial Greeting

**Assistant:**
```
Hello! 👋 Welcome to TalentScout's Hiring Assistant!

I'm here to help with your initial candidate screening for technology positions. 
I'll gather some essential information about you and then ask a few technical 
questions based on your expertise.

This should take about 10-15 minutes. Let's get started!

May I have your full name, please?
```

### 2. Providing Information

**User:** "John Doe"

**Assistant:** "Great! Thank you, John. Could you please provide your email address?"

**User:** "john.doe@example.com"

**Assistant:** "Perfect! What's the best phone number to reach you?"

**User:** "555-123-4567"

**Assistant:** "Thank you. How many years of professional experience do you have?"

**User:** "5 years"

**Assistant:** "Excellent! What position(s) are you interested in?"

**User:** "Senior Full Stack Developer"

**Assistant:** "Great choice! Where are you currently located?"

**User:** "San Francisco, CA"

**Assistant:** "Perfect! Now, please tell me about your tech stack. What programming languages, frameworks, databases, and tools are you proficient in?"

### 3. Declaring Tech Stack

**User:** "I'm proficient in Python, Django, JavaScript, React, PostgreSQL, Docker, and AWS"

**Assistant:** 
```
Excellent tech stack! Based on your experience with Python, Django, JavaScript, 
React, PostgreSQL, Docker, and AWS, I'd like to ask you a few technical questions 
to assess your proficiency.

Technical Questions:

1. Python & Django:
   Can you explain the difference between Django's function-based views and 
   class-based views? When would you choose one over the other?

2. React & JavaScript:
   How do you manage state in a complex React application? Can you compare 
   different state management solutions you've used?

3. PostgreSQL:
   What indexing strategies have you implemented to optimize database query 
   performance in PostgreSQL?

4. Docker & AWS:
   Can you describe your experience with containerization? How have you deployed 
   Docker containers to AWS, and what services did you use?

Please take your time to answer these questions. Your responses will help us 
better understand your technical capabilities.
```

### 4. Answering Technical Questions

**User:** 
```
1. Function-based views are simpler and more straightforward for basic operations, 
while class-based views offer better code reusability through inheritance and 
mixins. I prefer CBVs for CRUD operations and FBVs for unique, one-off endpoints.

2. I've used Redux for large applications with complex state requirements, and 
Context API with hooks for smaller applications. Recently, I've been exploring 
Zustand for its simplicity...
```

**Assistant:**
```
Thank you for your detailed responses! Your answers demonstrate solid understanding 
of these technologies. 

Is there anything else you'd like to add about your experience or qualifications?
```

### 5. Ending the Conversation

**User:** "No, that covers everything. Thank you!"

**Assistant:**
```
Thank you for your time! 🎉

Your information has been recorded. Our recruitment team will review your profile 
and technical responses. You can expect to hear from us within 3-5 business days 
via email.

If your profile matches our current openings, we'll reach out to schedule a 
detailed technical interview.

Best of luck with your job search! Feel free to return anytime if you have 
additional information to share.

Goodbye! 👋
```

## Alternative Ending Keywords

You can end the conversation at any time using these keywords:
- "goodbye"
- "bye"
- "exit"
- "quit"
- "done"
- "no thanks"
- "stop"
- "end"

## Example Tech Stacks

### Full Stack Developer
```
Languages: JavaScript, TypeScript, Python
Frontend: React, Next.js, Tailwind CSS
Backend: Node.js, Express, FastAPI
Database: MongoDB, PostgreSQL
DevOps: Docker, Kubernetes, GitHub Actions, AWS
```

### Mobile Developer
```
Languages: Swift, Kotlin, Dart
Frameworks: SwiftUI, Jetpack Compose, Flutter
Backend: Firebase, GraphQL, REST APIs
Tools: Xcode, Android Studio, Postman
```

### Data Engineer
```
Languages: Python, Scala, SQL
Frameworks: Apache Spark, Apache Airflow, dbt
Databases: PostgreSQL, MongoDB, Snowflake, BigQuery
Tools: Docker, Kubernetes, Terraform, Git
Cloud: AWS (S3, EMR, Redshift), GCP
```

### DevOps Engineer
```
Languages: Python, Bash, Go
IaC: Terraform, CloudFormation, Ansible
CI/CD: Jenkins, GitLab CI, GitHub Actions, CircleCI
Containerization: Docker, Kubernetes, Helm
Cloud: AWS, Azure, GCP
Monitoring: Prometheus, Grafana, ELK Stack
```

## Tips for Best Experience

1. **Be Specific**: Instead of "JavaScript frameworks", say "React, Vue.js, and Angular"
2. **Include Versions**: "Python 3.10+" or "React 18" shows currency with technology
3. **Mention Experience Level**: "5 years with Django" provides context
4. **List Tools**: Don't forget to mention IDEs, version control, testing frameworks
5. **Be Honest**: Only list technologies you're actually proficient in

## Handling Unclear Questions

If the assistant asks something you don't understand:

**User:** "I'm not sure what you mean by that. Could you clarify?"

The assistant will rephrase or provide more context.

## Starting Over

If you want to start a new conversation:
1. Click the "🔄 Start New Conversation" button in the sidebar, or
2. Refresh the page in your browser

## Privacy Note

All conversation data is stored only in your browser session and is cleared when you:
- Click "Start New Conversation"
- Close the browser tab
- Refresh the page

No data is permanently stored on any server.
