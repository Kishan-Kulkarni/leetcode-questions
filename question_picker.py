import streamlit as st
import pandas as pd
import random

# Load the data from the CSV file
file_path = 'google_alltime.csv'  # Update with your file path
data = pd.read_csv(file_path)

# Add a "Completed" column to the dataframe
data['Completed'] = False

# Dashboard Title
st.title("LeetCode Question Dashboard")

# Sidebar for options
st.sidebar.header("Options")

# Sort by difficulty
difficulty = st.sidebar.selectbox("Sort by Difficulty", ["All", "Easy", "Medium", "Hard"])
if difficulty != "All":
    data = data[data['Difficulty'] == difficulty]

# Show completed or not completed questions
show_completed = st.sidebar.checkbox("Show Completed Questions", value=False)
if show_completed:
    st.dataframe(data[data['Completed'] == True])
else:
    st.dataframe(data[data['Completed'] == False])

# Mark questions as completed
selected_ids = st.multiselect("Mark Questions as Completed (by ID)", data['ID'].tolist())
if selected_ids:
    data.loc[data['ID'].isin(selected_ids), 'Completed'] = True
    st.success(f"Marked questions {selected_ids} as completed.")

# Randomly select 10 questions that aren't completed
if st.button("Get 10 Random Questions"):
    not_completed = data[data['Completed'] == False]
    random_questions = not_completed.sample(n=10)
    st.write("Here are 10 random questions:")
    st.dataframe(random_questions)

# Save changes to the CSV file
data.to_csv('google_alltime_updated.csv', index=False)
