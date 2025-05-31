# 🚀 HireSmart AI
HireSmart AI is an AI-powered Resume Analyzer and Job Matcher platform designed to assist recruiters and job seekers by providing intelligent insights into resumes and job roles. It uses advanced natural language processing (NLP) and machine learning techniques to evaluate candidate levels, match them with job descriptions, and provide recommendations—all with a user-friendly Streamlit frontend and Firebase backend.

📌 Features
🧠 Resume Level Detection: Automatically determines if a resume is from a Fresher, Intermediate, or Experienced candidate based on its content.

📄 Job Role Matching: Analyzes resume content and matches it with relevant job descriptions.

🔐 Secure Authentication: Firebase-based user authentication system.

📊 Admin Dashboard: Centralized panel to view and manage uploaded resumes and candidate levels.

☁️ Firebase Integration: Resume metadata is securely stored and managed in Firebase.

🧾 Data Logging: Candidate data (email, resume name, timestamp, level) is saved for insights and analytics.

📈 Expandable Architecture: Built to integrate APIs like OpenAI and external job boards for advanced features.

📂 Project Structure
pgsql
Copy
Edit
HireSmart_AI/
│
├── backend/
│   ├── config/
│   │   └── config.py
│   ├── database/
│   │   ├── firebase.py
│   │   └── firebase_key.json
│   └── utils/
│       ├── resume_parser.py
│       └── job_matcher.py
│
├── frontend/
│   ├── app.py           # Streamlit app
│   └── assets/          # Logos, styles
│
├── candidate_data/      # Stores user-level JSON logs
├── requirements.txt
└── README.md
🛠️ Technologies Used
Frontend: Streamlit

Backend: Python

Database: Firebase Realtime Database & Firebase Storage

Authentication: Firebase Auth

Machine Learning/NLP: Spacy, Scikit-learn

APIs (Planned): OpenAI, Job Boards (LinkedIn, Indeed, etc.)

🚀 Getting Started
1. Clone the Repository
bash
Copy
Edit
git clone https://github.com/YOUR_USERNAME/HireSmart_AI.git
cd HireSmart_AI
2. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
3. Add Firebase Credentials
Place your Firebase JSON key in:

pgsql
Copy
Edit
backend/database/firebase_key.json
Update the config in firebase.py with your project-specific details.

4. Run the Application
bash
Copy
Edit
cd frontend
streamlit run app.py
🔒 GitHub Secret Push Protection
To avoid GitHub push protection errors:

NEVER commit API keys or credentials.

Add sensitive files (like .env, firebase_key.json) to .gitignore.

If secrets were accidentally committed:

Remove them from Git history using tools like git filter-repo or BFG.

Force-push the clean history.

Rotate the exposed credentials.

🧪 Sample Usage
Login or sign up using email/password.

Upload your resume (PDF).

View your candidate level and suggested job roles.

Admin can view and download metadata from the dashboard.

👨‍💻 Contributors
Abhinav Pradeep – @abhinavpradeep

Add Collaborators Here

🤝 Contributing
We welcome contributions!

Fork the repo.

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

