from flask import Flask, render_template, request, redirect, session
import pandas as pd
import random
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necessary for session management

# Load the CSV file
file_path = 'google_alltime.csv'
data = pd.read_csv(file_path)

# Ensure the CSV has the necessary columns
if 'Completed' not in data.columns:
    data['Completed'] = False
if 'Notes' not in data.columns:
    data['Notes'] = ""

# Helper function to check if all current questions are completed
def all_completed(question_ids):
    return all(data.loc[data['ID'].isin(question_ids), 'Completed'])

# Route to serve the questions
@app.route('/')
def home():
    # Check if the current session already has a list of questions
    if 'current_questions' not in session or all_completed(session['current_questions']):
        not_completed = data[data['Completed'] == False]
        if len(not_completed) == 0:
            session['current_questions'] = []
            return render_template('index.html', questions=[], message="All questions have been completed!")
        random_questions = not_completed.sample(n=10) if len(not_completed) >= 10 else not_completed
        session['current_questions'] = random_questions['ID'].tolist()

    # Fetch the current list of questions
    questions = data[data['ID'].isin(session['current_questions'])].to_dict(orient='records')
    return render_template('index.html', questions=questions)

# Route to handle marking a question as completed and adding notes
@app.route('/complete', methods=['POST'])
def complete():
    question_id = int(request.form['question_id'])
    note = request.form['note']

    # Update the CSV with completion status and note
    data.loc[data['ID'] == question_id, 'Completed'] = True
    data.loc[data['ID'] == question_id, 'Notes'] = note
    data.to_csv(file_path, index=False)

    return redirect('/')

# Run the Flask app
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
