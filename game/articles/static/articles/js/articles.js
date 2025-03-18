// Author: Marcos Vega Ipas (updated for dynamic quizzes)

document.addEventListener("DOMContentLoaded", function () {
    console.log("DOM content loaded");
    
    // Check for completed quizzes when page loads
    checkCompletedQuizzes();
    
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    // Function to check already completed quizzes
    function checkCompletedQuizzes() {
        // Get all quiz containers
        const quizContainers = document.querySelectorAll('.quizContainer');
        console.log("Found quiz containers for checking completion:", quizContainers.length);
        
        quizContainers.forEach(function(quizContainer) {
            const quizId = quizContainer.querySelector('.quiz-id').value;
            // Check if this quiz is already completed
            if (isQuizCompleted(quizId)) {
                console.log("Found completed quiz:", quizId);
                
                // Disable all inputs
                quizContainer.querySelectorAll('input[type="radio"]').forEach(input => {
                    input.disabled = true;
                });
                
                // Disable the check button
                const checkBtn = quizContainer.querySelector('.checkAnswer');
                if (checkBtn) {
                    checkBtn.disabled = true;
                    checkBtn.textContent = "Quiz Completed";
                }
                
                // Add completed message if not already present
                if (!quizContainer.querySelector('.completed-message')) {
                    const completedMsg = document.createElement('div');
                    completedMsg.className = 'completed-message';
                    completedMsg.textContent = 'You have already completed this quiz.';
                    completedMsg.style.color = '#4CAF50';
                    completedMsg.style.fontWeight = 'bold';
                    completedMsg.style.marginTop = '10px';
                    completedMsg.style.textAlign = 'center';
                    checkBtn.after(completedMsg);
                }
            }
        });
    }
    
    // Function to check if quiz is completed
    function isQuizCompleted(quizId) {
        return localStorage.getItem('completed_quiz_' + quizId) === 'true';
    }

    // The check answers functionality is now handled by inline JavaScript in the HTML template
});

