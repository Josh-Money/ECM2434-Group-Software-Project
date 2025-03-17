document.addEventListener('DOMContentLoaded', function() {
    const currentPath = window.location.pathname;
    const isPrivacyPage = currentPath === '/privacy-policy/';
    
    const logo = document.getElementById('footer-logo');
    const mascotImg = document.getElementById('mascot-img');
    const speechBubble = document.getElementById('speech-bubble');
    const mascotSpeechText = document.getElementById('mascot-speech-text');
    const closeButton = document.getElementById('close-speech');
    
    // Page-specific mascot messages - define this early so it can be used below
    const pageMessages = {
        '/home/': "Welcome back! Ready to make a difference today?",
        '/travel/': "How are you traveling to campus today?",
        // '/challenges/': "Check out these eco-challenges to earn points!",
        // '/articles/': "Learn something new about sustainability!",
        // '/leaderboard/': "See how you compare to other eco-warriors!",
        // '/qr/': "Scan a QR code to log your recycling!",
        //'/profile/': "Track your sustainability journey here!"
    };
    
    if (isPrivacyPage) {
        // Privacy policy page - mascot is already hidden via template logic
    } else {
        // On all other pages: hide logo
        if (logo) {
            logo.style.opacity = 0;
        }
        
        // Show initial speech bubble after a short delay
        setTimeout(function() {
            // Show page-specific message if available
            if (pageMessages[currentPath] && mascotSpeechText && speechBubble) {
                window.mascotSpeech(pageMessages[currentPath]);
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
            speechBubble.style.display = 'block';
            
            // Auto-hide after duration
            speechTimeout = setTimeout(function() {
                speechBubble.style.display = 'none';
            }, duration);
        }
    };
    
    // Mascot speech bubble functionality
    if (mascotImg && speechBubble) {
        // Click on mascot to show default message
        mascotImg.addEventListener('click', function() {
            window.mascotSpeech("Hello! I'm your eco-guide! Click me anytime for tips!");
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
});