/* Author: Josh Money */

// Dynamically shows each leaderboardon the same page
document.addEventListener("DOMContentLoaded", function () {
    
    //Selects all buttons
    const buttons = document.querySelectorAll(".leaderboard-button");

    //Selects all leaderboard containers
    const leaderboards = document.querySelectorAll(".leaderboard-container");

    //Function to show the selected leaderboard and hide others
    function showLeaderboard(targetId) {
        leaderboards.forEach(lb => {
            if (lb.id === targetId) {
                lb.style.display = "block";
            } else {
                lb.style.display = "none";
            }
        });

        buttons.forEach(btn => btn.classList.remove("active"));

        document.querySelector(`[data_target="${targetId}"]`).classList.add("active");
    }

    buttons.forEach(button => {
        button.addEventListener("click", function() {
            const targetLeaderboard = this.getAttribute("data-target");
            showLeaderboard(targetLeaderboard);
        });
    });

    showLeaderboard("leaderboard-main");
});
