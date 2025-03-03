document.addEventListener('DOMContentLoaded', function() {
    const submitButton = document.getElementById('submit');
    
    submitButton.addEventListener('click', function(event) {
        event.preventDefault();
        
        // Get form values
        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const message = document.getElementById('message').value;
        
        // Log the message to console
        console.log('Message submitted:', message);
        
        // Email functionality using EmailJS (you'll need to include this library)
        // First, add this script to your HTML:
        // <script src="https://cdn.jsdelivr.net/npm/@emailjs/browser@3/dist/email.min.js"></script>
        
        // Initialize EmailJS with your user ID
        emailjs.init("I2O_65b92fRzGoI9q"); // Replace with your actual EmailJS user ID
        
        // Prepare template parameters
        const templateParams = {
            to_email: email,
            from_name: "Syntax Squad",
            to_name: name,
            message: "Thank you for contacting us! We have received your message and will get back to you shortly.",
            reply_to: "syntaxsquad2025@gmail.com"
        };
        
        // Send email
        emailjs.send('service_t8gkz6o', 'template_ltcprtq', templateParams) // Replace with your service and template IDs
            .then(function(response) {
                console.log('Email sent successfully!', response.status, response.text);
                alert('Thanks for your message! A confirmation has been sent to your email.');
                
                // Optional: Reset the form
                document.querySelector('.contact-form').reset();
            })
            .catch(function(error) {
                console.error('Failed to send email:', error);
                alert('Message received, but there was an issue sending the confirmation email.');
            });
    });
});