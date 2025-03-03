document.addEventListener('DOMContentLoaded', function() {
    emailjs.init("I2O_65b92fRzGoI9q");
    
    const contactForm = document.getElementById('contact-form');
    const statusMessage = document.getElementById('status-message');
    const submitButton = document.getElementById('submit-btn');
    
    contactForm.addEventListener('submit', function(event) {
        event.preventDefault();
        
        
        submitButton.disabled = true; // prevent multiple submissions
        submitButton.textContent = 'Sending...';
        
        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const message = document.getElementById('message').value;
        
        const templateParams = {
            to_email: email,
            from_name: "Syntax Squad",
            to_name: name,
            message: message,
            reply_to: "syntaxsquad2025@gmail.com"
        };
        
        // Send email
        emailjs.send('service_t8gkz6o', 'template_ltcprtq', templateParams)
            .then(function(response) {
                console.log('Email sent successfully!', response.status, response.text);
                
                // Show success message
                statusMessage.textContent = 'Thanks for your message! A confirmation has been sent to your email.';
                statusMessage.className = 'alert alert-success';
                statusMessage.style.display = 'block';
                
                contactForm.reset(); // Reset
                
                // Re-enable the button
                submitButton.disabled = false;
                submitButton.textContent = 'Send Message';
            })
            .catch(function(error) {
                console.error('Failed to send email:', error);
                
                statusMessage.textContent = 'There was an error sending your message. Please try again later.';
                statusMessage.className = 'alert alert-danger';
                statusMessage.style.display = 'block';
                
                submitButton.disabled = false;
                submitButton.textContent = 'Send Message';
            });
    });
});