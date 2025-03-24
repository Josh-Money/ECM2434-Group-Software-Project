//Author: Josh Money

document.addEventListener('DOMContentLoaded', function() {
    // Get DOM elements
    console.log('1')
    const preview = document.getElementById('preview');
    const scanStatus = document.getElementById('scanStatus');
    const qrForm = document.getElementById('qrForm');
    const qrCodeInput = document.getElementById('qr_code');
    
    // Check if user is on a mobile device
    function isMobileDevice() {
        return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    }
    
    // Create camera activation button for mobile devices
    let cameraButton = null;
    if (isMobileDevice()) {
        cameraButton = document.createElement('button');
        cameraButton.textContent = 'Activate Camera';
        cameraButton.className = 'btn btn-primary mb-3';
        cameraButton.type = 'button';
        cameraButton.style.width = '100%';
        cameraButton.style.maxWidth = '400px';
        cameraButton.style.padding = '10px';
        cameraButton.style.margin = '0 auto 15px';
        cameraButton.style.display = 'block';
        preview.parentNode.insertBefore(cameraButton, preview);
    }
    
    // Valid QR codes
    const validCodes = ['amory_uni_bin', 'lafrowda_uni_bin', 'birks_uni_bin']; // Add more as needed
    
    // Set status message
    function setStatus(message, type = 'info') {
        if (scanStatus) {
            scanStatus.textContent = message;
            // Use #4CAF50 color for info messages
            if (type === 'info') {
                scanStatus.className = `alert mt-3 mb-4`;
                scanStatus.style.backgroundColor = '#4CAF50';
                scanStatus.style.color = 'white';
                scanStatus.style.border = '1px solid #4CAF50';
            } else {
                scanStatus.className = `alert alert-${type} mt-3 mb-4`;
                scanStatus.style.backgroundColor = '';
                scanStatus.style.color = '';
                scanStatus.style.border = '';
            }
            scanStatus.style.display = 'block';
        }
        console.log(`Status: ${message}`);
    }
    
    // Check if QR code is valid and submit form if it is
    function processQrCode(content) {
        if (validCodes.includes(content)) {
            // Set form value
            qrCodeInput.value = content;
            
            // Show success message
            setStatus('Valid QR code detected! Submitting...', 'success');
            
            // Submit form after a short delay
            setTimeout(function() {
                qrForm.submit();
            }, 800);
            
            return true;
        } else {
            // Show error message for invalid QR code
            setStatus('Invalid QR code. Please try a valid recycling bin QR code.', 'danger');
            return false;
        }
    }
    
    // Initialize camera and QR scanner
    function initializeCamera() {
        setStatus('Camera initializing... Please wait.', 'info');
        
        try {
            // Create scanner instance
            const scanner = new Instascan.Scanner({
                video: preview,
                mirror: false,
                backgroundScan: false,
                scanPeriod: 5 // Scan every 5ms
            });
            
            // Set up QR code detection
            scanner.addListener('scan', function(content) {
                console.log('QR code detected:', content);
                processQrCode(content);
            });
            
            // Get available cameras
            Instascan.Camera.getCameras()
                .then(function(cameras) {
                    if (cameras.length > 0) {
                        // Try to use the back camera on mobile
                        let selectedCamera = cameras[0]; // Default to first camera
                        
                        // Look for back camera on mobile devices
                        if (isMobileDevice()) {
                            for (let camera of cameras) {
                                if (camera.name && camera.name.toLowerCase().includes('back')) {
                                    selectedCamera = camera;
                                    break;
                                }
                            }
                        }
                        
                        scanner.start(selectedCamera)
                            .then(function() {
                                setStatus('Camera active. Point camera at a QR code.', 'info');
                                // Hide the button once camera is active (if on mobile)
                                if (cameraButton) {
                                    cameraButton.style.display = 'none';
                                }
                            })
                            .catch(function(err) {
                                console.error('Error starting camera:', err);
                                setStatus('Error starting camera. Please refresh.', 'danger');
                            });
                    } else {
                        setStatus('No cameras found. Please try a different device.', 'danger');
                    }
                })
                .catch(function(err) {
                    console.error('Error getting cameras:', err);
                    setStatus('Error accessing camera. Please allow camera access and refresh.', 'danger');
                });
        } catch (error) {
            console.error('Error initializing camera:', error);
            setStatus('Error accessing camera. Please refresh the page.', 'danger');
        }
    }
    
    // Enhance the form submit with validation for manual entry
    qrForm.addEventListener('submit', function(event) {
        const code = qrCodeInput.value.trim();
        
        if (!code) {
            setStatus('Please scan a QR code or enter a valid code.', 'warning');
            event.preventDefault(); // Prevent empty submission
            return;
        }
        
        if (!validCodes.includes(code)) {
            // Show validation message to the user
            setStatus('Invalid QR code. Please try again.', 'danger');
            event.preventDefault(); // Prevent form submission
        } else {
            setStatus('Valid QR code!', 'success');
            console.log('Submitting valid QR code:', code);
            // Form will submit naturally
        }
    });
    
    if (isMobileDevice()) {
        if (cameraButton) {
            // Set initial status for mobile
            setStatus('Click "Activate Camera" to begin scanning QR codes', 'info');
            
            // Add click handler
            cameraButton.addEventListener('click', function() {
                initializeCamera();
            });
        }
    } else {
        // Desktop: initialize camera on page load
        initializeCamera();
    }
});