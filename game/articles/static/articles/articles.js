// Author: Marcos Vega Ipas 

document.addEventListener("DOMContentLoaded", function () {

    document.getElementById("toggleQuiz").addEventListener("click", function () {
        const quizContainer = document.getElementById("quizContainer");
        if (quizContainer.style.display === "none" || quizContainer.classList.contains("hidden")) {
            quizContainer.style.display = "block";
            this.textContent = "Close Quiz ⬆"; 
        } else {
            quizContainer.style.display = "none";
            this.textContent = "Quiz 1 ⬇"; 
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
           
            const selectedOption = document.querySelector(`input[name="${questionId}"]:checked`);

           
            const existingFeedback = document.getElementById(`feedback-${questionId}`);
            if (existingFeedback) {
                existingFeedback.remove();
            }

           
            const feedback = document.createElement("span");
            feedback.id = `feedback-${questionId}`;
            feedback.style.marginLeft = "10px"; 

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

           
           
            const lastRadioButton = document.querySelectorAll(`input[name="${questionId}"]`);
            lastRadioButton[lastRadioButton.length - 1].parentNode.appendChild(feedback);
        });
        let scoreDisplay = document.getElementById("scoreDisplay");

        if (!scoreDisplay) {
            scoreDisplay = document.createElement("span");
            scoreDisplay.id = "scoreDisplay";
            scoreDisplay.style.marginLeft = "15px";
            document.getElementById("checkAnswer").after(scoreDisplay);
        }

       
        scoreDisplay.textContent = ` Score: ${score}/${totalQuestions}`;
        scoreDisplay.style.fontWeight = "bold";

        document.querySelectorAll('input[type="radio"]').forEach(input => {
            input.disabled = true;
        });

        document.getElementById("checkAnswer").disabled = true;
    });
})
