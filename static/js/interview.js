// Interview-specific JavaScript for AI Interview Coach

// Global variables for interview session
let currentQuestion = null;
let currentCategory = 'behavioral';
let isRecording = false;
let recognition = null;

// Initialize interview interface
document.addEventListener('DOMContentLoaded', function() {
    initializeInterview();
});

function initializeInterview() {
    // Initialize speech recognition
    initializeSpeechRecognition();
    
    // Event listeners
    document.getElementById('start-interview')?.addEventListener('click', startInterview);
    document.getElementById('submit-response')?.addEventListener('click', submitResponse);
    document.getElementById('next-question')?.addEventListener('click', generateNextQuestion);
    document.getElementById('skip-question')?.addEventListener('click', skipQuestion);
    document.getElementById('voice-btn')?.addEventListener('click', toggleVoiceRecording);
    document.getElementById('end-session')?.addEventListener('click', endSession);
    document.getElementById('continue-interview')?.addEventListener('click', continueInterview);
    
    // Update session info periodically
    setInterval(updateSessionInfo, 30000); // Update every 30 seconds
}

// Speech recognition setup
function initializeSpeechRecognition() {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        recognition = new SpeechRecognition();
        
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = 'en-US';
        
        recognition.onstart = function() {
            isRecording = true;
            const voiceBtn = document.getElementById('voice-btn');
            if (voiceBtn) {
                voiceBtn.classList.add('recording');
                voiceBtn.innerHTML = '<i class="bi bi-stop"></i>';
            }
        };
        
        recognition.onresult = function(event) {
            const responseInput = document.getElementById('response-input');
            if (responseInput) {
                let finalTranscript = '';
                let interimTranscript = '';
                
                for (let i = event.resultIndex; i < event.results.length; i++) {
                    const transcript = event.results[i][0].transcript;
                    if (event.results[i].isFinal) {
                        finalTranscript += transcript;
                    } else {
                        interimTranscript += transcript;
                    }
                }
                
                responseInput.value = finalTranscript + interimTranscript;
            }
        };
        
        recognition.onerror = function(event) {
            console.error('Speech recognition error:', event.error);
            stopVoiceRecording();
            AIInterviewCoach.showAlert('Speech recognition error: ' + event.error, 'warning');
        };
        
        recognition.onend = function() {
            stopVoiceRecording();
        };
    } else {
        const voiceBtn = document.getElementById('voice-btn');
        if (voiceBtn) {
            voiceBtn.disabled = true;
            voiceBtn.title = 'Speech recognition not supported';
        }
    }
}

function toggleVoiceRecording() {
    if (isRecording) {
        stopVoiceRecording();
    } else {
        startVoiceRecording();
    }
}

function startVoiceRecording() {
    if (recognition) {
        recognition.start();
    }
}

function stopVoiceRecording() {
    if (recognition) {
        recognition.stop();
    }
    isRecording = false;
    const voiceBtn = document.getElementById('voice-btn');
    if (voiceBtn) {
        voiceBtn.classList.remove('recording');
        voiceBtn.innerHTML = '<i class="bi bi-mic"></i>';
    }
}

// Interview flow functions
async function startInterview() {
    try {
        AIInterviewCoach.showLoading('loading-state');
        AIInterviewCoach.hideLoading('question-section');
        
        await generateNextQuestion();
        
        AIInterviewCoach.hideLoading('loading-state');
        AIInterviewCoach.showLoading('question-content');
    } catch (error) {
        console.error('Error starting interview:', error);
        AIInterviewCoach.showAlert('Failed to start interview. Please try again.', 'danger');
        AIInterviewCoach.hideLoading('loading-state');
        AIInterviewCoach.showLoading('question-section');
    }
}

async function generateNextQuestion() {
    try {
        AIInterviewCoach.showLoading('loading-state');
        AIInterviewCoach.hideLoading('question-content');
        
        const response = await AIInterviewCoach.apiCall('/api/generate-question', {
            method: 'POST',
            body: JSON.stringify({
                category: currentCategory
            })
        });
        
        currentQuestion = response.question;
        currentCategory = response.category;
        
        // Update UI
        document.getElementById('current-question').textContent = currentQuestion;
        document.getElementById('question-category').textContent = currentCategory.replace('_', ' ').toUpperCase();
        document.getElementById('question-difficulty').textContent = response.difficulty.toUpperCase();
        
        // Clear previous response
        document.getElementById('response-input').value = '';
        
        AIInterviewCoach.hideLoading('loading-state');
        AIInterviewCoach.showLoading('question-content');
        
        // Update question counter
        updateQuestionCounter();
        
    } catch (error) {
        console.error('Error generating question:', error);
        AIInterviewCoach.showAlert('Failed to generate question. Please try again.', 'danger');
        AIInterviewCoach.hideLoading('loading-state');
        AIInterviewCoach.showLoading('question-content');
    }
}

async function submitResponse() {
    const responseInput = document.getElementById('response-input');
    const response = responseInput.value.trim();
    
    if (!response) {
        AIInterviewCoach.showAlert('Please provide a response before submitting.', 'warning');
        return;
    }
    
    if (!currentQuestion) {
        AIInterviewCoach.showAlert('No question available. Please generate a new question.', 'warning');
        return;
    }
    
    try {
        AIInterviewCoach.showLoading('loading-state');
        
        const evaluation = await AIInterviewCoach.apiCall('/api/evaluate-response', {
            method: 'POST',
            body: JSON.stringify({
                response: response,
                category: currentCategory
            })
        });
        
        displayFeedback(evaluation);
        updateSessionInfo();
        
        AIInterviewCoach.hideLoading('loading-state');
        
    } catch (error) {
        console.error('Error evaluating response:', error);
        AIInterviewCoach.showAlert('Failed to evaluate response. Please try again.', 'danger');
        AIInterviewCoach.hideLoading('loading-state');
    }
}

function displayFeedback(evaluation) {
    const modal = new bootstrap.Modal(document.getElementById('feedbackModal'));
    const feedbackContent = document.getElementById('feedback-content');
    
    const scoreClass = evaluation.score >= 8 ? 'score-excellent' : 
                      evaluation.score >= 6 ? 'score-good' : 'score-needs-improvement';
    
    feedbackContent.innerHTML = `
        <div class="text-center mb-4">
            <div class="score-display ${scoreClass}">
                ${evaluation.score}/10
            </div>
            <h5>Response Evaluation</h5>
        </div>
        
        <div class="row">
            <div class="col-md-6">
                <h6 class="text-success">
                    <i class="bi bi-check-circle"></i> Strengths
                </h6>
                <ul class="list-unstyled">
                    ${evaluation.strengths.map(strength => `<li><i class="bi bi-check text-success"></i> ${strength}</li>`).join('')}
                </ul>
            </div>
            <div class="col-md-6">
                <h6 class="text-warning">
                    <i class="bi bi-exclamation-triangle"></i> Areas for Improvement
                </h6>
                <ul class="list-unstyled">
                    ${evaluation.improvement_areas.map(area => `<li><i class="bi bi-arrow-up text-warning"></i> ${area}</li>`).join('')}
                </ul>
            </div>
        </div>
        
        <div class="mt-4">
            <h6>Detailed Feedback</h6>
            <p>${evaluation.feedback}</p>
        </div>
        
        ${evaluation.resources.length > 0 ? `
        <div class="mt-4">
            <h6>Recommended Resources</h6>
            <ul class="list-unstyled">
                ${evaluation.resources.map(resource => `<li><i class="bi bi-link-45deg text-primary"></i> ${resource}</li>`).join('')}
            </ul>
        </div>
        ` : ''}
    `;
    
    modal.show();
}

function continueInterview() {
    const modal = bootstrap.Modal.getInstance(document.getElementById('feedbackModal'));
    modal.hide();
    generateNextQuestion();
}

function skipQuestion() {
    if (confirm('Are you sure you want to skip this question?')) {
        generateNextQuestion();
    }
}

async function endSession() {
    if (confirm('Are you sure you want to end this interview session?')) {
        try {
            await AIInterviewCoach.apiCall('/api/end-session', {
                method: 'POST'
            });
            
            AIInterviewCoach.stopSessionTimer();
            window.location.href = '/results';
            
        } catch (error) {
            console.error('Error ending session:', error);
            AIInterviewCoach.showAlert('Failed to end session properly.', 'warning');
        }
    }
}

// UI update functions
function updateQuestionCounter() {
    const counter = document.getElementById('question-counter');
    if (counter) {
        const currentCount = parseInt(counter.textContent) || 0;
        counter.textContent = currentCount + 1;
    }
}

async function updateSessionInfo() {
    try {
        const summary = await AIInterviewCoach.apiCall('/api/session-summary');
        
        // Update session info
        document.getElementById('questions-asked').textContent = summary.total_questions;
        document.getElementById('avg-score').textContent = summary.average_score;
        document.getElementById('current-difficulty').textContent = summary.difficulty_level.toUpperCase();
        
        // Update feedback list
        updateFeedbackList(summary.responses);
        
    } catch (error) {
        console.error('Error updating session info:', error);
    }
}

function updateFeedbackList(responses) {
    const feedbackList = document.getElementById('feedback-list');
    if (!feedbackList) return;
    
    if (responses.length === 0) {
        feedbackList.innerHTML = '<p class="text-muted text-center">No feedback yet</p>';
        return;
    }
    
    const recentResponses = responses.slice(-3).reverse(); // Show last 3 responses
    feedbackList.innerHTML = recentResponses.map(response => `
        <div class="mb-3 pb-3 border-bottom">
            <div class="d-flex justify-content-between align-items-start">
                <small class="text-muted">Q${response.question.substring(0, 30)}...</small>
                <span class="badge bg-${response.evaluation.score >= 7 ? 'success' : response.evaluation.score >= 5 ? 'warning' : 'danger'}">
                    ${response.evaluation.score}/10
                </span>
            </div>
            <p class="small mb-1">${response.response.substring(0, 50)}...</p>
        </div>
    `).join('');
}

// Keyboard shortcuts
document.addEventListener('keydown', function(event) {
    // Ctrl/Cmd + Enter to submit response
    if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
        event.preventDefault();
        submitResponse();
    }
    
    // Ctrl/Cmd + N for next question
    if ((event.ctrlKey || event.metaKey) && event.key === 'n') {
        event.preventDefault();
        generateNextQuestion();
    }
    
    // Ctrl/Cmd + Space to toggle voice recording
    if ((event.ctrlKey || event.metaKey) && event.key === ' ') {
        event.preventDefault();
        toggleVoiceRecording();
    }
});

// Cleanup on page unload
window.addEventListener('beforeunload', function() {
    if (isRecording) {
        stopVoiceRecording();
    }
    AIInterviewCoach.stopSessionTimer();
}); 