job_role_keywords = {
    "data_scientist": ['machine learning', 'deep learning', 'pandas', 'numpy', 'scikit-learn', 'matplotlib', 'seaborn', 'tensorflow', 'keras', 'pytorch', 'xgboost', 'lightgbm', 'data wrangling', 'jupyter', 'streamlit', 'flask'],
    
    "ml_engineer": ['mlops', 'tensorflow', 'keras', 'pytorch', 'airflow', 'docker', 'kubernetes', 'scikit-learn', 'xgboost', 'model deployment', 'ci/cd', 'cloud', 'aws', 'gcp', 'azure'],

    "data_analyst": ['excel', 'sql', 'power bi', 'tableau', 'google data studio', 'pandas', 'numpy', 'data cleaning', 'data visualization', 'business analysis', 'looker', 'dash', 'matplotlib', 'seaborn'],

    "data_engineer": ['sql', 'python', 'spark', 'hadoop', 'airflow', 'aws', 'azure', 'gcp', 'bigquery', 'kafka', 'etl', 'data pipeline', 'snowflake', 'databricks', 'nosql', 'mongodb'],

    "fullstack_developer": ['html', 'css', 'javascript', 'react', 'node.js', 'express', 'mongodb', 'sql', 'django', 'flask', 'typescript', 'next.js', 'tailwindcss', 'git'],

    "frontend_developer": ['html', 'css', 'javascript', 'react', 'vue', 'angular', 'tailwindcss', 'bootstrap', 'typescript', 'next.js', 'jquery'],

    "backend_developer": ['python', 'java', 'node.js', 'express', 'flask', 'django', 'sql', 'mongodb', 'postgresql', 'redis', 'docker', 'rest api', 'graphql'],

    "android_developer": ['java', 'kotlin', 'android', 'firebase', 'android studio', 'sqlite', 'mvvm', 'xml'],

    "ios_developer": ['swift', 'ios', 'xcode', 'core data', 'firebase', 'cocoa touch', 'mvvm', 'swiftui'],

    "flutter_developer": ['flutter', 'dart', 'firebase', 'bloc', 'sqlite', 'rest api', 'android', 'ios'],

    "devops_engineer": ['docker', 'kubernetes', 'jenkins', 'ansible', 'terraform', 'aws', 'azure', 'gcp', 'ci/cd', 'linux', 'bash', 'monitoring', 'prometheus', 'grafana'],

    "cloud_engineer": ['aws', 'azure', 'gcp', 'cloudformation', 'terraform', 'devops', 'cloud architecture', 'serverless', 's3', 'ec2', 'cloud security'],

    "ai_engineer": ['deep learning', 'tensorflow', 'keras', 'pytorch', 'llm', 'openai', 'transformers', 'huggingface', 'nlp', 'computer vision', 'reinforcement learning', 'cnn', 'rnn'],

    "nlp_engineer": ['nlp', 'spacy', 'nltk', 'transformers', 'bert', 'gpt', 'openai', 'huggingface', 'text classification', 'named entity recognition', 'llm'],

    "cv_engineer": ['opencv', 'computer vision', 'image processing', 'cnn', 'pytorch', 'tensorflow', 'keras', 'object detection', 'image segmentation'],

    "ui_ux_designer": ['figma', 'adobe xd', 'sketch', 'wireframing', 'prototyping', 'user research', 'usability testing', 'design systems', 'interaction design', 'illustrator'],

    "product_manager": ['agile', 'scrum', 'kanban', 'jira', 'trello', 'product roadmap', 'user stories', 'wireframing', 'analytics', 'stakeholder management', 'confluence'],

    "business_analyst": ['excel', 'power bi', 'tableau', 'sql', 'data analysis', 'business analysis', 'requirement gathering', 'dashboards', 'kpis', 'etl'],

    "cybersecurity_analyst": ['penetration testing', 'ethical hacking', 'network security', 'kali linux', 'burpsuite', 'wireshark', 'nmap', 'siem', 'vulnerability assessment'],

    "blockchain_developer": ['blockchain', 'web3', 'solidity', 'smart contracts', 'ethereum', 'metamask', 'truffle', 'hardhat', 'ipfs', 'ganache'],

    "iot_engineer": ['iot', 'raspberry pi', 'arduino', 'mqtt', 'edge computing', 'iot security', 'sensors', 'esp32', 'cloud integration', 'data logging'],

    "researcher": ['academic writing', 'research methodology', 'latex', 'scopus', 'ieee', 'bibliometrics', 'ml', 'ai', 'citations', 'hypothesis'],

    "content_writer": ['content writing', 'seo', 'sem', 'wordpress', 'copywriting', 'editing', 'proofreading', 'technical writing', 'canva', 'google docs'],

    "marketing_analyst": ['google analytics', 'seo', 'sem', 'facebook ads', 'google ads', 'email marketing', 'hubspot', 'market research', 'campaigns', 'crm'],

    "hr_analyst": ['recruitment', 'hr operations', 'training', 'onboarding', 'interview scheduling', 'employee engagement', 'payroll', 'compliance'],

    "sales_executive": ['crm', 'salesforce', 'lead generation', 'cold calling', 'negotiation', 'customer relationship', 'product demos', 'pipeline management'],

    "customer_support": ['customer support', 'ticketing tools', 'communication', 'problem-solving', 'chat support', 'crm', 'email support', 'zendesk'],

    "project_manager": ['project management', 'jira', 'scrum', 'kanban', 'agile', 'gantt charts', 'risk management', 'resource allocation', 'status reporting'],

    "qa_engineer": ['manual testing', 'automation testing', 'selenium', 'test cases', 'bug tracking', 'jira', 'postman', 'api testing', 'regression testing'],

    "robotics_engineer": ['robotics', 'ros', 'embedded systems', 'arduino', 'raspberry pi', 'sensors', 'control systems', 'c++', 'python', 'simulation'],

    "finance_analyst": ['financial modeling', 'accounting', 'budgeting', 'excel', 'quickbooks', 'erp', 'sap', 'market analysis', 'valuation', 'forecasting'],
}

def get_most_suitable_job_role(resume_skills):
    best_match = None
    max_matches = 0

    for role, keywords in job_role_keywords.items():
        matched = [skill for skill in resume_skills if skill.lower() in map(str.lower, keywords)]
        if len(matched) > max_matches:
            max_matches = len(matched)
            best_match = {
                "role": role,
                "matched_skills": matched,
                "match_count": len(matched)
            }

    return best_match

def recommended_skills(role, matched_skill):
    recommended = []
    for roles, keywords in job_role_keywords.items():
        if role == roles:
            # Add only those skills not already matched
            recommended = [skill for skill in keywords if skill.lower() not in map(str.lower, matched_skill)]
            break
    return recommended


                        
