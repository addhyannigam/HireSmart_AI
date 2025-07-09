# hr.py
import streamlit as st
import base64
import pandas as pd
from streamlit_option_menu import option_menu
from backend.database import firebase as fb
import io
import matplotlib.pyplot as plt
import seaborn as sns

import pandas as pd
import plotly.express as px

import pandas as pd

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

def show_admin_page():
    with st.sidebar:
        selected = option_menu("HireSmart HR",
                            ["Dashboard", "Users"],
                            icons=["speedometer", "people"],
                            menu_icon="briefcase",
                            default_index=0,
                            orientation="vertical")
    if st.sidebar.button("Logout"):
        st.session_state['is_logged_in'] = False
        st.session_state['role'] = None
        st.session_state['page'] = 'Login'
        st.rerun()
    # Helper: Get only 'User' role data from Firebase
    def fetch_user_data():
        all_users = fb.rdb.child("users").get().val()
        if all_users:
            data = [v for v in all_users.values() if isinstance(v, dict) and v.get('role') == 'User']
            return pd.DataFrame(data)
        return pd.DataFrame()

    # ------------------- Dashboard ------------------- #
    if selected == "Dashboard":
        st.header("📊 HR Dashboard")

        df_firebase = fetch_user_data()
        if not df_firebase.empty:
            # ✅ Total Users Metric
            total_users = len(df_firebase)
            st.markdown("### 🧑‍💼 Overview")
            col1, _ = st.columns([1, 4])
            with col1:
                st.metric("Total Candidates", total_users)

            st.markdown("---")
            st.subheader("📋 Candidate Data")
            st.dataframe(df_firebase)

            # Process timestamp for monthly trend chart
            if "timestamp" in df_firebase.columns:
                df_firebase["timestamp"] = pd.to_datetime(df_firebase["timestamp"], errors='coerce')
                df_firebase["Month"] = df_firebase["timestamp"].dt.to_period("M").astype(str)
                monthly_counts = df_firebase["Month"].value_counts().sort_index()
            else:
                monthly_counts = pd.Series()

            # ============================
            # 📊 Charts in Grid Layout
            # ============================
            
            st.markdown("**📅 Registrations Over Time**")
            if not monthly_counts.empty:
                st.line_chart(monthly_counts)
            else:
                st.info("No timestamp data available for time series analysis.")           

        else:
            st.info("No candidate records found in Firebase.")

        st.subheader("📊 Candidate Experience Distribution")

        data = pd.read_csv("candidate_data/candidate_levels.csv")
        
        level_counts = data['Level'].value_counts().reset_index()
        level_counts.columns = ['Experience Level', 'Count']

        fig = px.pie(level_counts, names='Experience Level', values='Count',
                    color_discrete_sequence=px.colors.qualitative.Pastel,
                    title="Distribution of Candidate Experience Levels")
        st.plotly_chart(fig)


    # ------------------- Settings ------------------- #
    elif selected == "Users":
        st.header("⚙️ User Settings")
        df_firebase = fetch_user_data()

        if not df_firebase.empty:
            for index, row in df_firebase.iterrows():
                user_email = row['email']
                user_role = row['role']
                uid = None
                # Find UID
                all_users = fb.rdb.child("users").get().val()
                for k, v in all_users.items():
                    if v.get('email') == user_email and v.get('role') == 'User':
                        uid = k
                        break

                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{row['username']}** | {user_email} | Role: {user_role}")

                    if uid:
                        # Fetch existing HR comment if any
                        existing_comment = all_users[uid].get("hr_comment", "")
                        comment_input = st.text_input(
                            f"📝 HR Comment for {row['username']}", 
                            value=existing_comment, 
                            key=f"comment_{uid}"
                        )
                        if st.button("💾 Save Comment", key=f"save_{uid}"):
                            fb.rdb.child("users").child(uid).update({"hr_comment": comment_input})
                            st.success(f"Comment saved for {row['username']}")
                            st.rerun()

                with col2:
                    if st.button(f"Delete", key=user_email):
                        if uid:
                            fb.rdb.child("users").child(uid).remove()
                            st.success(f"Deleted user: {user_email}")
                            st.rerun()
        else:
            st.info("No candidates to manage.")
