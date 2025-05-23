import pymysql
import streamlit as st
from config.settings import DB_CONFIG
from database.models import UserData
import pandas as pd 
import plotly.express as px

def create_connection():
    return pymysql.connect(**DB_CONFIG)

def initialize_database():
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            # Create DB if not exists
            cursor.execute("CREATE DATABASE IF NOT EXISTS CV;")
            
            # Create table
            table_sql = """
            CREATE TABLE IF NOT EXISTS user_data (
                ID INT NOT NULL AUTO_INCREMENT,
                Name varchar(500) NOT NULL,
                Email_ID VARCHAR(500) NOT NULL,
                resume_score VARCHAR(8) NOT NULL,
                Timestamp VARCHAR(50) NOT NULL,
                Page_no VARCHAR(5) NOT NULL,
                Predicted_Field BLOB NOT NULL,
                User_level BLOB NOT NULL,
                Actual_skills BLOB NOT NULL,
                Recommended_skills BLOB NOT NULL,
                Recommended_courses BLOB NOT NULL,
                PRIMARY KEY (ID)
            );
            """
            cursor.execute(table_sql)
        connection.commit()
    finally:
        connection.close()

def insert_data(user_data):
    connection = create_connection()
    cursor = connection.cursor()
    DB_table_name = 'user_data'
    
    insert_sql = f"""
        INSERT INTO {DB_table_name}
        VALUES (0, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    rec_values = (
        user_data.name,
        user_data.email,
        user_data.resume_score,
        user_data.timestamp,
        user_data.no_of_pages,
        user_data.predicted_field,
        user_data.user_level,
        user_data.actual_skills,
        user_data.recommended_skills,
        user_data.recommended_courses
    )
    
    try:
        cursor.execute(insert_sql, rec_values)
        connection.commit()
        print("✅ Resume data inserted into MySQL.")
    except Exception as e:
        print("❌ Error inserting data:", e)
    finally:
        connection.close()


def get_all_user_data():
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM user_data")
            return cursor.fetchall()
    finally:
        connection.close()

def delete_user_data(user_id):
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM user_data WHERE ID = %s", (user_id,))
        connection.commit()
        st.success(f"Deleted user with ID {user_id}")
    except Exception as e:
        st.error(f"Error deleting user: {e}")
    finally:
        connection.close()


def display_admin_insights():
    try:
        connection = create_connection()
        query = 'SELECT * FROM user_data;'
        plot_data = pd.read_sql(query, connection)

        # Decode BLOB columns (Predicted_Field, User_level, etc.)
        for col in plot_data.columns:
            if plot_data[col].dtype == object:
                plot_data[col] = plot_data[col].apply(lambda x: x.decode('utf-8') if isinstance(x, bytes) else x)

        # --- Pie chart for predicted field recommendation ---
        if 'Predicted_Field' in plot_data.columns:
            field_counts = plot_data['Predicted_Field'].value_counts().reset_index()
            field_counts.columns = ['Predicted_Field', 'Count']
            st.subheader("**Pie-Chart for Predicted Field Recommendation**")
            fig = px.pie(field_counts, values='Count', names='Predicted_Field',
                         title='Predicted Field according to the Skills')
            st.plotly_chart(fig)
        else:
            st.warning("Column 'Predicted_Field' not found in user_data.")

        # --- Pie chart for user level ---
        if 'User_level' in plot_data.columns:
            level_counts = plot_data['User_level'].value_counts().reset_index()
            level_counts.columns = ['User_level', 'Count']
            st.subheader("**Pie-Chart for User's Experienced Level**")
            fig = px.pie(level_counts, values='Count', names='User_level',
                         title="Pie-Chart📈 for User's👨‍💻 Experienced Level")
            st.plotly_chart(fig)
        else:
            st.warning("Column 'User_level' not found in user_data.")

    except Exception as e:
        st.error(f"Error while fetching or visualizing data: {e}")
