# user.py
import streamlit as st
import base64
from streamlit_tags import st_tags
from streamlit_option_menu import option_menu
import base64
from PIL import Image
import os
import pandas as pd
from backend.services.job_fetcher import get_job_suggestions
from backend.services.ats_score import extract_text_from_pdf, evaluate_resume_sections
from backend.services.resume_parser import get_number_of_pages,extract_skills,pdf_reader
from backend.services.skill_analyzer import get_most_suitable_job_role, recommended_skills

import json
import uuid
from Courses import resume_videos, interview_videos
from yt_dlp import YoutubeDL

import random
import csv
from datetime import datetime

def get_image_as_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img_base64 = get_image_as_base64("frontend/Desings/falcons.png")

st.markdown(
    f"""
    <div style="position: fixed; top: 40px; right: 40px;">
        <img src="data:image/png;base64,{img_base64}" width="100">
    </div>
    """,
    unsafe_allow_html=True
)




def show_user_page():
    with st.sidebar:
        selected = option_menu(
            "HireSmart AI",
            ["Home", "Resume Analyzer", "Job Suggestions", "Contact Us"],
            icons=["house", "file-earmark-text", "briefcase", "envelope"],
            menu_icon="robot",
            default_index=0
        )
    if st.sidebar.button("Logout"):
        st.session_state['is_logged_in'] = False
        st.session_state['role'] = None
        st.session_state['page'] = 'Login'
        st.rerun()

    # -------------- HOME PAGE -------------- #
    if selected == "Home":
        img = Image.open("frontend/Desings/logo-removebg-preview.png")
        st.image(img)
        st.title("👋 Welcome to HireSmart AI!")
        st.markdown("""
        **HireSmart AI** is your intelligent assistant for improving your resume and increasing your chances of landing your dream job.  
        Here's what you can do:
        - 📝 **Resume Analyzer**: Upload your resume, get an ATS (Applicant Tracking System) score, and personalized feedback.
        - 💼 **Job Suggestions**: Receive job role suggestions based on your resume content.
        - 📊 **Reports**: Download detailed feedback and suggested improvements.
        - 🎓 **Courses & Resources**: Get recommended YouTube videos and courses to upgrade your skills.
        """)

    # -------------- RESUME ANALYZER -------------- #
    elif selected == "Resume Analyzer":
        st.title("📄Resume Analyzer")
        uploaded_resume = st.file_uploader("Upload Your Resume (PDF format)", type=["pdf"])

        if uploaded_resume is not None:
            save_path = os.path.join("Uploaded_Resumes", uploaded_resume.name)
            with open(save_path, "wb") as f:
                f.write(uploaded_resume.read())
                st.success("Resume uploaded successfully!")

            with st.spinner("Analyzing your resume..."):
                text = extract_text_from_pdf(uploaded_resume)
                ats_score = evaluate_resume_sections(text)
            st.subheader("✅ ATS Score")
            st.markdown(f"**Score:** {ats_score}/100")

            cand_level = ''
            if get_number_of_pages(save_path) == 1:
                cand_level = "Fresher"
                st.markdown('''<h4 style='text-align: left; color: #d73b5c;'>You are looking Fresher.</h4>''',
                            unsafe_allow_html=True)
            elif get_number_of_pages(save_path) == 2:
                cand_level = "Intermediate"
                st.markdown('''<h4 style='text-align: left; color: #1ed760;'>You are at intermediate level!</h4>''',
                            unsafe_allow_html=True)
            elif get_number_of_pages(save_path) >= 3:
                cand_level = "Experienced"
                st.markdown('''<h4 style='text-align: left; color: #fba171;'>You are at experience level!''',
                            unsafe_allow_html=True)
                
            user_email = st.session_state.get("user_email", "anonymous")
            data = {
                    "Level": [cand_level],
                    }
            df = pd.DataFrame(data)
            csv_file = "candidate_data/candidate_levels.csv"

            # If file exists, append without writing header again
            if os.path.exists(csv_file):
                df.to_csv(csv_file, mode='a', header=False, index=False)
            else:
                df.to_csv(csv_file, index=False)

            st.subheader("**Skills Recommendation💡**")
            text_extract = pdf_reader(save_path)
            skill_sets = extract_skills(text_extract)
            
            keywords = st.multiselect(label = "Skills you have!",
                                      options = skill_sets,
                                      default = skill_sets,
                                      disabled = True,
                                      key = '1')
            role = get_most_suitable_job_role(skill_sets)
            
            role1 = role["role"]
            matches = role["matched_skills"]
            recommended = recommended_skills(role1,matches)
            st.success(f"** Our analysis says you are looking for {role1} role**")
            recommended_skill = st.multiselect(label = 'Recommended skills for you.',
                                         options = recommended,
                                         default = recommended,
                                         disabled = True,
                                         key = '2')
            
            st.subheader("**YouTube Videos for Resume improvement and Interview Prep**")
            def fetch_yt_video(link):
                ydl_opts = {}
                with YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(link, download=False)
                    return info_dict.get('title', 'Unknown Title')


            ## Resume writing video
            st.header("*Bonus Video for Resume Writing Tips💡*")
            resume_vid = random.choice(resume_videos)
            res_vid_title = fetch_yt_video(resume_vid)
            st.subheader("✅ *"+res_vid_title+"*")
            st.video(resume_vid)


            ## Interview Preparation Video
            st.header("*Bonus Video for Interview Tips💡*")
            interview_vid = random.choice(interview_videos)
            int_vid_title = fetch_yt_video(interview_vid)
            st.subheader("✅ *" + int_vid_title + "*")
            st.video(interview_vid)

            
            

    # -------------- JOB SUGGESTIONS -------------- #
    elif selected == "Job Suggestions":
        st.title("🔍 Job Suggestions")

        # 1. Add experience level input
        Experience = st.selectbox("Select your experience level:", ["Intern", "Fresher", "Experienced"])

        # 2. Upload resume
        uploaded_resume = st.file_uploader("Upload Resume for Job Matching", type=["pdf"])
        if uploaded_resume is not None:
            save_path = os.path.join("Uploaded_Resumes", uploaded_resume.name)
            with open(save_path, "wb") as f:
                f.write(uploaded_resume.read())

            # 3. Analyze resume with experience level
            with st.spinner("Analyzing your resume..."):
                skills, suggestions = get_job_suggestions(save_path, Experience)

                st.subheader("Extracted Skills")
                st.write(skills)

                st.subheader("Suggested Job Roles")
                st.write(suggestions)


    # -------------- CONTACT US -------------- #
    elif selected == "Contact Us":
        st.title("📬 Contact Us")

        st.markdown("""
        **We'd love to hear from you!**  
        For any queries, support, or feedback, please fill out the form below or contact us through the following:
        """)


        # Basic contact form
        with st.form(key="contact_form"):
            name = st.text_input("Your Name")
            email = st.text_input("Your Email")
            message = st.text_area("Your Message")
            submit = st.form_submit_button("Send")

            if submit:
                # You can later integrate with Firebase/email API here
                st.success("Thank you for contacting us! We'll get back to you soon.")
        
        st.markdown("""
        - 📧 Email: support@hiresmart.ai  
        - 🌐 Website: [www.hiresmart.ai](http://www.hiresmart.ai)  
        - 📱 Phone: +91 0000000000
        """)

