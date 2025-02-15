// Author: Will Cooke
console.log('x');

const TEST_USER = {
    id: "123",
    name: "John Doe",
    points: 101
};
const NO_USER = null;

window.userLoaded = new Promise((resolve) => {
    const timeout = setTimeout(() => {
        reject(new Error("User failed to load after 5 seconds."));
    }, 5000);

    setTimeout(() => {
        window.user = NO_USER
        clearTimeout(timeout);
        resolve(window.user);
    }, 1000);
});

document.addEventListener("DOMContentLoaded", () => {
    profileButton = document.getElementById('profile-button')
    
    window.userLoaded.then((user) => {
        console.log("User loaded:", user);
        profileButton.style.opacity = 1;
        
        if (user) {
            profileButton.src = profileButton.getAttribute("data-profile");
        } else {
            profileButton.src = profileButton.getAttribute("data-login");
            profileButton.addEventListener("click", () => {
                window.location.href = '/login'
            });
        }
        
    }).catch((error) => {
        console.error("Error loading user:", error);
    });
});