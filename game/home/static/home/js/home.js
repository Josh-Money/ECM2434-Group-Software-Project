// Author: Will Cooke
console.log('x');

window.userLoaded
    .then((user) => { // user and their data is loaded

        const loggedIn = document.getElementById("loggedIn");
        const userIsAuthenticated = true;
        console.log('User is authenticated:', userIsAuthenticated);
        loggedIn.style.display = "block";
    })
    .catch((error) => { // user did not load
        const loggedOut = document.getElementById("loggedOut");
        loggedOut.style.display = "block";
    });

