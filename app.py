from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
import random
from config import Config
from utils.ai_helper import AIHelper
from utils.session_manager import SessionManager

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Initialize helpers
ai_helper = AIHelper()
session_manager = SessionManager()

@app.route('/')
def index():
    """Home page with user profile setup."""
    return render_template('index.html')

@app.route('/setup', methods=['GET', 'POST'])
def setup():
    """User profile setup page."""
    if request.method == 'POST':
        user_profile = {
            'name': request.form.get('name', ''),
            'career_field': request.form.get('career_field', ''),
            'experience_level': request.form.get('experience_level', ''),
            'target_role': request.form.get('target_role', ''),
            'interview_type': request.form.get('interview_type', 'behavioral')
        }
        
        # Create new session
        session_id = session_manager.create_session(user_profile)
        session['session_id'] = session_id
        
        return redirect(url_for('interview'))
    
    return render_template('setup.html', 
                         career_fields=Config.CAREER_FIELDS,
                         interview_categories=Config.INTERVIEW_CATEGORIES)

@app.route('/interview')
def interview():
    """Main interview interface."""
    session_id = session.get('session_id')
    if not session_id:
        return redirect(url_for('setup'))
    
    user_session = session_manager.get_session(session_id)
    if not user_session:
        return redirect(url_for('setup'))
    
    return render_template('interview.html', 
                         user_profile=user_session['user_profile'],
                         session_data=user_session)

@app.route('/api/generate-question', methods=['POST'])
def generate_question():
    """Generate a new interview question."""
    session_id = session.get('session_id')
    if not session_id:
        return jsonify({'error': 'No active session'}), 400
    
    user_session = session_manager.get_session(session_id)
    if not user_session:
        return jsonify({'error': 'Session expired'}), 400
    
    data = request.get_json()
    category = data.get('category', 'behavioral')
    difficulty = user_session['difficulty_level']
    
    # Generate question using AI
    question = ai_helper.generate_question(
        user_session['user_profile'], 
        category, 
        difficulty
    )
    
    # Update session
    session_manager.update_session(session_id, {
        'current_question': question,
        'categories_covered': user_session['categories_covered'].union([category])
    })
    
    return jsonify({
        'question': question,
        'category': category,
        'difficulty': difficulty
    })

@app.route('/api/evaluate-response', methods=['POST'])
def evaluate_response():
    """Evaluate user's response to a question."""
    session_id = session.get('session_id')
    if not session_id:
        return jsonify({'error': 'No active session'}), 400
    
    user_session = session_manager.get_session(session_id)
    if not user_session:
        return jsonify({'error': 'Session expired'}), 400
    
    data = request.get_json()
    user_response = data.get('response', '')
    question = user_session.get('current_question', '')
    category = data.get('category', 'behavioral')
    
    if not user_response or not question:
        return jsonify({'error': 'Missing response or question'}), 400
    
    # Evaluate response using AI
    evaluation = ai_helper.evaluate_response(question, user_response, category)
    
    # Add response to session
    session_manager.add_response(session_id, question, user_response, evaluation)
    
    return jsonify(evaluation)

@app.route('/api/generate-role-questions', methods=['POST'])
def generate_role_questions():
    """Generate interview questions based on a specific role."""
    data = request.get_json()
    role = data.get('role', 'General')
    num_questions = data.get('num_questions', 3)
    
    if not role:
        return jsonify({'error': 'Role is required'}), 400
    
    try:
        questions = ai_helper.generate_role_questions(role, num_questions)
        return jsonify({
            'questions': questions,
            'role': role,
            'count': len(questions)
        })
    except Exception as e:
        print(f"Error generating role questions: {e}")
        return jsonify({'error': 'Failed to generate questions'}), 500

@app.route('/api/qa-feedback', methods=['POST'])
def qa_feedback():
    """Generate structured feedback for a list of Q&A pairs."""
    data = request.get_json()
    questions_answers = data.get('questions_answers', [])
    role = data.get('role', 'General')
    
    if not questions_answers:
        return jsonify({'error': 'Questions and answers are required'}), 400
    
    # Validate input format
    try:
        qa_list = []
        for qa in questions_answers:
            if isinstance(qa, dict):
                question = qa.get('question', '')
                answer = qa.get('answer', '')
            elif isinstance(qa, list) and len(qa) == 2:
                question, answer = qa
            else:
                return jsonify({'error': 'Invalid Q&A format'}), 400
            
            if question and answer:
                qa_list.append((question, answer))
        
        if not qa_list:
            return jsonify({'error': 'No valid Q&A pairs found'}), 400
        
    except Exception as e:
        return jsonify({'error': 'Invalid input format'}), 400
    
    try:
        feedback = ai_helper.generate_qa_feedback(qa_list, role)
        return jsonify({
            'feedback': feedback,
            'role': role,
            'qa_count': len(qa_list)
        })
    except Exception as e:
        print(f"Error generating Q&A feedback: {e}")
        return jsonify({'error': 'Failed to generate feedback'}), 500

@app.route('/qa-feedback-form')
def qa_feedback_form():
    """Q&A feedback form page."""
    return render_template('qa_feedback.html')

@app.route('/session-summary')
def session_summary():
    """Get session summary and analytics."""
    session_id = session.get('session_id')
    if not session_id:
        return jsonify({'error': 'No active session'}), 400
    
    summary = session_manager.get_session_summary(session_id)
    if not summary:
        return jsonify({'error': 'Session not found'}), 400
    
    return jsonify(summary)

@app.route('/results')
def results():
    """Display interview results and feedback."""
    session_id = session.get('session_id')
    if not session_id:
        return redirect(url_for('setup'))
    
    summary = session_manager.get_session_summary(session_id)
    if not summary:
        return redirect(url_for('setup'))
    
    return render_template('results.html', summary=summary)

@app.route('/api/end-session', methods=['POST'])
def end_session():
    """End the current interview session."""
    session_id = session.get('session_id')
    if session_id:
        session_manager.update_session(session_id, {'session_complete': True})
        session.pop('session_id', None)
    
    return jsonify({'message': 'Session ended successfully'})

@app.route('/api/restart-session', methods=['POST'])
def restart_session():
    """Restart a new interview session."""
    session_id = session.get('session_id')
    if session_id:
        session_manager.delete_session(session_id)
    
    session.pop('session_id', None)
    return jsonify({'message': 'Session restarted'})

@app.route('/resources')
def resources():
    """Display learning resources."""
    return render_template('resources.html')

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Clean up expired sessions on startup
    session_manager.cleanup_expired_sessions()
    
    app.run(debug=Config.DEBUG, host='0.0.0.0', port=5000) 