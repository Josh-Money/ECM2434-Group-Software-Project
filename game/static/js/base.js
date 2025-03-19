document.addEventListener('DOMContentLoaded', function() {
    const currentPath = window.location.pathname;
    const isPrivacyPage = currentPath === '/privacy-policy/';
    
    console.log('Current path:', currentPath);
    
    const logo = document.getElementById('footer-logo');
    const mascotImg = document.getElementById('mascot-img');
    const speechBubble = document.getElementById('speech-bubble');
    const mascotSpeechText = document.getElementById('mascot-speech-text');
    const closeButton = document.getElementById('close-speech');
    
    // Collection of eco-friendly jokes for the mascot
    const ecoJokes = [
        "Why did the recycling bin go to therapy? It had too many issues to sort through! ♻️",
        "What's a tree's favorite drink? Root beer! 🌳",
        "How do you organize an eco-friendly party? You planet! 🌎",
        "Why did the bicycle fall over? Because it was two-tired from reducing carbon emissions! 🚲",
        "What's an environmentalist's favorite kind of joke? Recycled ones! ♻️",
        "What did one LED bulb say to the other? 'You're so bright!' 💡",
        "Why do trees have so many friends? They branch out! 🌲",
        "What happens when you throw a green stone into the Red Sea? It gets wet! 💦",
        "What do you call a suspicious looking tree? Shady! 🌴",
    ];
    
    // Page-specific mascot messages - define this early so it can be used below
    const pageMessages = {
        '/home/': "Welcome back! Ready to make a difference today?",
        '/travel/': "How are you traveling to campus today? Don't lie to me!",
        // '/challenges/': "Check out these eco-challenges to earn points!",
        // '/articles/': "Learn something new about sustainability!",
        // '/leaderboard/': "See how you compare to other eco-warriors!",
        // '/qr/': "Scan a QR code to log your recycling!",
        //'/profile/': "Track your sustainability journey here!"
    };
    
    // Function to get a random joke from the collection
    function getRandomJoke() {
        const randomIndex = Math.floor(Math.random() * ecoJokes.length);
        return ecoJokes[randomIndex];
    }
    
    // Function to check if this is the first visit to a page in this session
    function isFirstVisit(path) {
        // Get the visited pages from local storage or initialize as empty array
        const visitedPagesKey = 'ecoQuestVisitedPages';
        const visitedPages = JSON.parse(localStorage.getItem(visitedPagesKey) || '[]');
        
        console.log('Visited pages from storage:', visitedPages);
        console.log('Checking if visited:', path);
        
        // Check if this page has been visited
        const hasVisited = visitedPages.includes(path);
        console.log('Has visited before:', hasVisited);
        
        if (hasVisited) {
            return false;
        } else {
            // Add this page to visited pages and save to local storage
            visitedPages.push(path);
            localStorage.setItem(visitedPagesKey, JSON.stringify(visitedPages));
            return true;
        }
    }
    
    if (isPrivacyPage) {
        // Privacy policy page - mascot is already hidden via template logic
    } else {
        // On all other pages: hide logo
        if (logo) {
            logo.style.opacity = 0;
        }
        
        // Show initial speech bubble after a short delay, but only for first visit to specific pages
        setTimeout(function() {
            // Check if there's a page-specific message for this path
            const hasPageMessage = pageMessages.hasOwnProperty(currentPath);
            console.log('Has page message:', hasPageMessage, 'for path:', currentPath);
            
            // Show page-specific message if available AND it's first visit in this session
            if (hasPageMessage && mascotSpeechText && speechBubble) {
                if (isFirstVisit(currentPath)) {
                    console.log('Showing mascot message for first visit to:', currentPath);
                    window.mascotSpeech(pageMessages[currentPath]);
                } else {
                    console.log('Not showing mascot message, already visited:', currentPath);
                }
            } else if (mascotSpeechText && speechBubble) {
                // Default message if no page-specific message
                // window.mascotSpeech("Hello! I'm your eco-guide!");
            }
        }, 1000);
    }
    
    // Auto-hide speech bubble after 8 seconds
    let speechTimeout;
    
    // Global function to make the mascot speak
    window.mascotSpeech = function(text, duration = 8000) {
        if (mascotSpeechText && speechBubble) {
            // Clear any existing timeout
            if (speechTimeout) {
                clearTimeout(speechTimeout);
            }
            
            // Set the text and show the bubble
            mascotSpeechText.textContent = text;
            
            // Adjust font size based on text length
            if (text.length > 100) {
                mascotSpeechText.style.fontSize = '12px';
            } else if (text.length > 70) {
                mascotSpeechText.style.fontSize = '13px';
            } else {
                mascotSpeechText.style.fontSize = '14px';
            }
            
            // Show the speech bubble
            speechBubble.style.display = 'block';
            
            // Auto-hide after duration
            speechTimeout = setTimeout(function() {
                speechBubble.style.display = 'none';
                // Reset font size to default after hiding
                mascotSpeechText.style.fontSize = '14px';
            }, duration);
        }
    };
    
    // Mascot speech bubble functionality
    if (mascotImg && speechBubble) {
        // Click on mascot to show a random joke
        mascotImg.addEventListener('click', function() {
            const joke = getRandomJoke();
            window.mascotSpeech(joke, 10000);
        });
        
        // Close button functionality
        if (closeButton) {
            closeButton.addEventListener('click', function(e) {
                e.stopPropagation(); // Prevent event from bubbling up
                speechBubble.style.display = 'none';
                // Clear any existing timeout
                if (speechTimeout) {
                    clearTimeout(speechTimeout);
                }
            });
        }
    }
    
    // Debug: Show a way to reset storage for testing
    console.log('To reset visited pages, run in console: localStorage.removeItem("ecoQuestVisitedPages")');
});