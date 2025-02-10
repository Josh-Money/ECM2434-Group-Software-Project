// Author: Will Cooke

document.addEventListener("DOMContentLoaded", function () {
    const loggedIn = document.getElementById("loggedIn");
    const loggedOut = document.getElementById("loggedOut");
    const userIsAuthenticated = false;
    console.log('User is authenticated:', userIsAuthenticated);

    if (userIsAuthenticated) {
        loggedIn.style.display = "block";
    } else {
        loggedOut.style.display = "block";
    }
});