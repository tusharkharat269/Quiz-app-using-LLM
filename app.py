from flask import Flask, render_template, request, redirect, url_for, session
from mcqService import fetchQuestions

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a secure random key

# Quiz data organized by topics
Quiz_topics = {
    "python": {
        "name": "Python",
        "icon": "fab fa-python"
        },
    "java": {
        "name": "Java",
        "icon": "fab fa-java",
    },
    "cpp": {
        "name": "C++",
        "icon": "fas fa-code"
    }
}


@app.route('/')
def index():
    session.clear()
    return render_template('index.html', topics=Quiz_topics)

@app.route('/start_quiz', methods=['POST'])
def start_quiz():
    selected_topic = request.form.get('topic')
    if not selected_topic or selected_topic not in Quiz_topics:
        return redirect(url_for('index'))
    
    session['topic'] = selected_topic
    session['current_question'] = 0
    session['score'] = 0
    session['answers'] = []
    session['quiz_questions'] = fetchQuestions(session.get('topic'))

    return redirect(url_for('quiz'))

@app.route('/quiz')
def quiz():
    topic = session.get('topic')
    if not topic or topic not in Quiz_topics:
        return redirect(url_for('index'))
    
    current_q = session.get('current_question', 0)
    quiz_questions = session.get('quiz_questions')

    
    if current_q >= len(quiz_questions):
        return redirect(url_for('results'))
    
    question_data = quiz_questions[current_q]
    topic_info = Quiz_topics[topic]
    
    return render_template('quiz.html', 
                         question=question_data, 
                         question_num=current_q + 1,
                         total_questions=len(quiz_questions),
                         topic_info=topic_info)

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    topic = session.get('topic')
    if not topic or topic not in Quiz_topics:
        return redirect(url_for('index'))
    
    current_q = session.get('current_question', 0)
    selected_answer = int(request.form.get('answer', -1))

    # Store the answer
    if 'answers' not in session:
        session['answers'] = []
    
    session['answers'].append(selected_answer)
    quiz_questions = session.get('quiz_questions')

    if quiz_questions and selected_answer == int(quiz_questions[current_q]['answer']):
        session['score'] = session.get('score', 0) + 1
    
    # Move to next question
    session['current_question'] = current_q + 1
    
    return redirect(url_for('quiz'))


@app.route('/results')
def results():
    topic = session.get('topic')
    quiz_questions = session.get('quiz_questions')

    if not topic or topic not in Quiz_topics:
        return redirect(url_for('index'))
    
    score = session.get('score', 0)
    total = len(quiz_questions)
    answers = session.get('answers', [])
    topic_info = Quiz_topics[topic]
    
    # Calculate percentage
    percentage = (score / total) * 100 if total > 0 else 0
    
    return render_template('results.html', 
                         score=score, 
                         total=total, 
                         percentage=percentage,
                         Quiz_topics=quiz_questions,
                         user_answers=answers,
                         topic_info=topic_info)

if __name__ == '__main__':
    app.run(debug=True)