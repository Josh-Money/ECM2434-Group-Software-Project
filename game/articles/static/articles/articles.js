document.addEventListener("DOMContentLoaded", function () {

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

    document.getElementById("toggleQuiz").addEventListener("click", function () {
        const quizContainer = document.getElementById("quizContainer");
        if (quizContainer.style.display === "none" || quizContainer.classList.contains("hidden")) {
            quizContainer.style.display = "block";
            this.textContent = "Close Quiz ⬆"; // Change button text
        } else {
            quizContainer.style.display = "none";
            this.textContent = "Quiz 1 ⬇"; // Change button text
        }
        quizContainer.classList.toggle("hidden");
    });

    
    document.getElementById("checkAnswer").addEventListener("click", function () {
        
        const correctAnswers = {
            Q1: "false",
            Q2: "true",
            Q3: "false",
            Q4: "true",
            Q5: "true"
        };

        let score = 0;
        const totalQuestions = Object.keys(correctAnswers).length;

        Object.keys(correctAnswers).forEach(questionId => {
            // Get selected option
            const selectedOption = document.querySelector(`input[name="${questionId}"]:checked`);

            // Remove existing feedback (if any)
            const existingFeedback = document.getElementById(`feedback-${questionId}`);
            if (existingFeedback) {
                existingFeedback.remove();
            }

            // Create a new feedback element
            const feedback = document.createElement("span");
            feedback.id = `feedback-${questionId}`;
            feedback.style.marginLeft = "10px"; // Spacing for better visibility

            if (selectedOption) {
                if (selectedOption.value === correctAnswers[questionId]) {
                    feedback.textContent = "✅ Correct";
                    feedback.style.color = "green";
                    score++;
                } else {
                    feedback.textContent = "❌ Incorrect";
                    feedback.style.color = "red";
                }
            } else {
                feedback.textContent = "⚠️ Please select an option!";
                feedback.style.color = "orange";
            }

            // Insert feedback next to the selected option (or the last radio button if none are selected)
           
            const lastRadioButton = document.querySelectorAll(`input[name="${questionId}"]`);
            lastRadioButton[lastRadioButton.length - 1].parentNode.appendChild(feedback);
        });
        let scoreDisplay = document.getElementById("scoreDisplay");

        if (!scoreDisplay) {
            // If the score display doesn't exist, create it
            scoreDisplay = document.createElement("span");
            scoreDisplay.id = "scoreDisplay";
            scoreDisplay.style.marginLeft = "15px";
            document.getElementById("checkAnswer").after(scoreDisplay);
        }

        // Set the score text
        scoreDisplay.textContent = ` Score: ${score}/${totalQuestions}`;
        scoreDisplay.style.fontWeight = "bold";

        document.querySelectorAll('input[type="radio"]').forEach(input => {
            input.disabled = true;
        });

        // **Disable the "Check Answers" button**
        document.getElementById("checkAnswer").disabled = true;

        fetch('/articles/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: new URLSearchParams({
                'correct_answers': score
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok.');
            }
            return response.json();
        })
        .then(data => {
            console.log("Leaderboard updated:", data);
        })
        .catch(error => console.error("Error updating leaderboard:", error));
    });
});

