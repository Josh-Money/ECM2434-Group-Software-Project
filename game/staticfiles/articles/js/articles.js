// Author: Marcos Vega Ipas 

document.addEventListener("DOMContentLoaded", function () {
    console.log("DOM content loaded");
    
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
    
    function checkCompletedQuizzes() {
        const quizContainers = document.querySelectorAll('.quizContainer');
        console.log("Found quiz containers for checking completion:", quizContainers.length);
        
        quizContainers.forEach(function(quizContainer) {
            const quizId = quizContainer.querySelector('.quiz-id').value;
            if (isQuizCompleted(quizId)) {
                console.log("Found completed quiz:", quizId);
                
                quizContainer.querySelectorAll('input[type="radio"]').forEach(input => {
                    input.disabled = true;
                });
                
                const checkBtn = quizContainer.querySelector('.checkAnswer');
                if (checkBtn) {
                    checkBtn.disabled = true;
                    checkBtn.textContent = "Quiz Completed";
                }
                
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
    
    function isQuizCompleted(quizId) {
        return localStorage.getItem('completed_quiz_' + quizId) === 'true';
    }
});

