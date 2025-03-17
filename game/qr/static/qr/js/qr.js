//Author: Josh Money

// Hybrid approach with both manual entry and optional camera scanning
document.addEventListener('DOMContentLoaded', function() {
    
    // Get DOM elements
    const preview = document.getElementById('preview');
    const scanStatus = document.getElementById('scanStatus');
    const qrForm = document.getElementById('qrForm');
    const qrCodeInput = document.getElementById('qr_code');
    
    // Set status message
    function setStatus(message, type = 'info') {
        scanStatus.textContent = message;
        scanStatus.className = `alert alert-${type} mt-3 mb-4`;
        console.log(`Status: ${message}`);
    }
    
    // Try to initialize the camera scanner, but don't worry if it fails
    try {
        // Don't initialize camera if Instascan isn't available
        if (typeof Instascan === 'undefined') {
            console.log('Instascan library not available, skipping camera initialization');
            return;
        }
        
        // Create scanner instance
        let scanner = new Instascan.Scanner({
            video: preview,
            scanPeriod: 3,
            mirror: false
        });
        
        // Add scan listener to auto-fill the form field when a QR code is detected
        scanner.addListener('scan', function(content) {
            console.log('QR code detected:', content);
            
            // Set form value
            qrCodeInput.value = content;
            
            // Show success message
            setStatus('QR code detected! Click the Submit button to continue.', 'success');
        });
        
        // Start camera (if available)
        Instascan.Camera.getCameras()
            .then(function(cameras) {
                if (cameras.length > 0) {
                    scanner.start(cameras[0])
                        .then(() => {
                            console.log('Camera started successfully');
                            setStatus('Camera active. Point at QR code or use manual entry above.');
                        })
                        .catch(err => {
                            console.error('Error starting camera:', err);
                            // Don't show error to user - they can use manual entry
                        });
                } else {
                    console.log('No cameras found');
                    // Don't show an error - user can use manual entry
                }
            })
            .catch(function(err) {
                console.error('Error accessing cameras:', err);
                // Don't show an error - user can use manual entry
            });
    } catch (error) {
        // If there's any error with camera initialization, just log it
        // User can still use the manual form
        console.error('Error with camera scanner:', error);
    }
    
    // Enhance the form submit with validation
    qrForm.addEventListener('submit', function(event) {
        const code = qrCodeInput.value.trim();
        
        // Validate if the QR code is one of the expected values
        const validCodes = ['amory_uni_bin', 'lafrowda_uni_bin', 'birks_uni_bin']; // Add more valid codes as needed
        
        if (!validCodes.includes(code)) {
            // Show validation message to the user
            setStatus('Invalid QR code. Please try again.', 'danger');
            event.preventDefault(); // Prevent form submission
        } else {
            setStatus('Valid QR code!', 'success');
            console.log('Submitting valid QR code:', code);
            // Auto-submit the form
            qrForm.submit();
        }
    });
});