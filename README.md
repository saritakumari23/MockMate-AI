# MockMate AI

MockMate AI is an advanced, AI-powered mock interview simulator designed to help you ace your job interviews. Built with Python, Flask, and the OpenAI API, this application provides a dynamic and realistic practice environment where you can sharpen your skills, get instant feedback, and build your confidence.

## ✨ Key Features

-   🤖 **AI-Powered Question Engine**: Generates interview questions dynamically based on your specified career field, experience level, and target role.
-   🧠 **Adaptive Difficulty**: The questions automatically adjust to your performance, creating a challenging yet optimal learning curve.
-   📝 **Real-time Performance Feedback**: Receive instant, detailed evaluations of your answers, with scores and qualitative feedback.
-   💡 **Q&A Feedback Tool**: Submit a list of your own question-and-answer pairs for a specific role and get structured feedback on each, highlighting strengths, weaknesses, and suggestions.
-   🎤 **Speech Recognition**: Practice speaking your answers naturally with integrated voice-to-text functionality.
-   📊 **Session Summaries**: Review your performance at the end of each session to track your progress over time.
-   🎨 **Modern & Responsive UI**: A clean, intuitive, and mobile-friendly interface built with Bootstrap 5.

## 🛠️ Technology Stack

-   **Backend**: Python, Flask
-   **AI**: OpenAI API
-   **Frontend**: HTML5, CSS3, JavaScript
-   **UI Framework**: Bootstrap 5
-   **Speech-to-Text**: Web Speech API

## 🚀 Getting Started

Follow these instructions to get the project up and running on your local machine.

### Prerequisites

-   Python 3.7+
-   An active OpenAI API key.

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/mockmate-ai.git
    cd mockmate-ai
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    ```
    Activate it:
    -   Windows: `venv\\Scripts\\activate`
    -   macOS/Linux: `source venv/bin/activate`

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    -   Rename the `env_example.txt` file to `.env`.
    -   Open the `.env` file and add your credentials:
        ```env
        OPENAI_API_KEY="your_openai_api_key_here"
        FLASK_SECRET_KEY="a_strong_random_secret_key"
        ```

5.  **Run the application:**
    ```bash
    python run.py
    ```

6.  Open your browser and navigate to `http://127.0.0.1:5000`.

## 📂 Project Structure

```
mockmate-ai/
├── app.py                # Main Flask application with routes
├── run.py                # Script to run the application
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── env_example.txt       # Example environment variables file
├── static/               # Static assets (CSS, JavaScript)
│   ├── css/style.css
│   └── js/
│       ├── main.js
│       └── interview.js
├── templates/            # Jinja2 HTML templates
│   ├── base.html
│   ├── index.html
│   ├── interview.html
│   └── ... (other templates)
└── utils/                # Helper modules
    ├── ai_helper.py      # Handles all OpenAI API interactions
    └── session_manager.py # Manages user session data
```

