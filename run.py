#!/usr/bin/env python3
"""
AI Interview Coach - Run Script
Simple script to start the Flask application
"""

import os
import sys
from app import app

def main():
    """Main function to run the application."""
    
    # Check if OpenAI API key is set
    if not os.environ.get('OPENAI_API_KEY'):
        print("⚠️  Warning: OPENAI_API_KEY not found in environment variables.")
        print("   Please set your OpenAI API key to use the AI features.")
        print("   You can create a .env file with: OPENAI_API_KEY=your_key_here")
        print()
    
    # Check if Flask secret key is set
    if not os.environ.get('FLASK_SECRET_KEY'):
        print("⚠️  Warning: FLASK_SECRET_KEY not found in environment variables.")
        print("   Using default development secret key.")
        print()
    
    print("🚀 Starting AI Interview Coach...")
    print("📱 Open your browser to: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the server")
    print()
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Goodbye! Thanks for using AI Interview Coach.")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 