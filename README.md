# AI Interview Coach

An AI-driven mock interview simulator built using OpenAI's GPT-4 and Flask. It dynamically generates interview questions based on the user's profile and career goal, evaluates their responses using NLP, and provides structured feedback.

## Features

- 🤖 **AI-Powered Questions**: Dynamic question generation based on user profile and career goals
- 📊 **Response Evaluation**: NLP-based analysis of interview responses
- 🎯 **Personalized Feedback**: Structured feedback with improvement areas
- 📈 **Adaptive Difficulty**: Questions adapt to user performance
- 🎤 **Speech Recognition**: Optional voice input integration
- 📚 **Resource Links**: Curated learning resources for improvement
- 🎨 **Modern UI**: Clean Bootstrap-based interface

## Tech Stack

- **Backend**: Flask, OpenAI GPT-4, Python
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **AI**: OpenAI API for question generation and response evaluation
- **Speech**: Web Speech API for voice input

## Setup Instructions

1. Clone the repository
2. Install Python dependencies: `pip install -r requirements.txt`
3. Set up your OpenAI API key in environment variables
4. Run the Flask application: `python app.py`
5. Open your browser to `http://localhost:5000`

## Project Structure

```
ai-interview-coach/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── static/              # Static files (CSS, JS, images)
├── templates/           # HTML templates
├── utils/              # Utility functions
└── README.md           # This file
```

## Environment Variables

Create a `.env` file with:
```
OPENAI_API_KEY=your_openai_api_key_here
FLASK_SECRET_KEY=your_secret_key_here
```

## License

MIT License 