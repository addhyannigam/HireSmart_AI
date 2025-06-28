import sys
import os
import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import base64

sys.path.append(os.path.abspath(os.path.join(os.path.dirname("frontend/"), '..')))

from frontend import hr, user
from backend.database import firebase as fb  # Pyrebase config


st.set_page_config(
    page_title="HireSmart AI",
    page_icon="frontend/Desings/favicon.png",
    layout="centered"
)

def get_image_as_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img_base64 = get_image_as_base64("frontend/Desings/image-removebg-preview.png")

st.markdown(
    f"""
    <div style="position: fixed; top: 40px; right: 40px;">
        <img src="data:image/png;base64,{img_base64}" width="100">
    </div>
    """,
    unsafe_allow_html=True
)

# Initialize session state variables
if "is_logged_in" not in st.session_state:
    st.session_state['is_logged_in'] = False
if "role" not in st.session_state:
    st.session_state['role'] = None
if "page" not in st.session_state:
    st.session_state['page'] = 'Login'

# If already logged in → redirect to the respective page
if st.session_state['is_logged_in']:
    role = st.session_state['role']
    if role == "Admin":
        hr.show_admin_page()
    elif role == "User":
        user.show_user_page()
    else:
        st.error("Invalid user role. Contact support.")
    st.stop()  # Prevent further rendering of login/signup UI

# Sidebar option menu
with st.sidebar:
    st.image("frontend/Desings/logo.png")
    selected = option_menu("HireSmart AI", ["Login", "SignUp"],
                           menu_icon="robot", default_index=0)

# ---------------------- LOGIN ---------------------- #
# ---------------------- LOGIN ---------------------- #
if selected == "Login":
    st.image("frontend/Desings/logo-removebg-preview.png")
    st.session_state['page'] = 'Login'
    st.title("Login")
    login_email = st.text_input(label="Email")
    login_password = st.text_input(label="Password", type="password")

    col1, col2 = st.columns([1, 1])
    with col1:
        login_clicked = st.button("Login")
        forgot_clicked = st.button("Forgot Password?")
        

    if login_clicked:
        if not login_email or not login_password:
            st.warning("Please enter both email and password.")
        else:
            try:
                user_data = fb.auth.sign_in_with_email_and_password(login_email, login_password)
                uid = user_data['localId']
                user_info = fb.rdb.child("users").child(uid).get().val()

                if not user_info:
                    st.error("Account not found. Please sign up first.")
                else:
                    username = user_info.get("username")
                    role = user_info.get("role")
                    st.session_state['is_logged_in'] = True
                    st.session_state['role'] = role
                    st.session_state['username'] = username
                    st.rerun()
            except Exception as e:
                error_msg = str(e).lower()
                if "invalid" in error_msg:
                    st.error("Invalid email or password.")
                elif "email" in error_msg:
                    st.error("Invalid email address.")
                elif "password" in error_msg:
                    st.error("Incorrect password.")
                elif "no user" in error_msg or "does not exist" in error_msg:
                    st.error("User does not exist. Please sign up first.")
                else:
                    st.error("Login failed. Please try again.")

    if forgot_clicked:
        if not login_email:
            st.warning("Please enter your email address to reset password.")
        else:
            try:
                fb.auth.send_password_reset_email(login_email)
                st.success("Password reset email sent. Please check your inbox.")
            except Exception as e:
                st.error("Failed to send reset email. Make sure the email is registered.")


# ---------------------- SIGN UP ---------------------- #
if selected == "SignUp":
    st.image("frontend/Desings/logo-removebg-preview.png")
    st.session_state['page'] = 'SignUp'
    st.title("Sign Up")
    username = st.text_input(label="Username")
    signup_email = st.text_input(label="Email")
    signup_password = st.text_input(label="Password", type="password")
    user_type = st.selectbox("Role", options=["User", ])

    if st.button("Register"):
        if not username or not signup_email or not signup_password:
            st.warning("All fields are required.")
        else:
            try:
                user_data = fb.auth.create_user_with_email_and_password(signup_email, signup_password)
                uid = user_data['localId']
                data = {
                    "username": username,
                    "email": signup_email,
                    "role": user_type
                }
                fb.rdb.child("users").child(uid).set(data)
                st.success("Account created successfully! Please Login")
                st.session_state['page'] = 'Login'
                st.rerun()
            except Exception as e:
                error_msg = str(e).lower()
                if "email exists" in error_msg:
                    st.error("Email already registered. Please login.")
                elif "invalid email" in error_msg:
                    st.error("Enter a valid email address.")
                elif "password" in error_msg:
                    st.error("Password should be at least 6 characters.")
                else:
                    st.error("Signup failed. Please try again.")
