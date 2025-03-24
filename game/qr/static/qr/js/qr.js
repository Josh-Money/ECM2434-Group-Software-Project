//Author: Josh Money

document.addEventListener('DOMContentLoaded', function() {
    // Get DOM elements
    const preview = document.getElementById('preview');
    const scanStatus = document.getElementById('scanStatus');
    const qrForm = document.getElementById('qrForm');
    const qrCodeInput = document.getElementById('qr_code');
    
    const validCodes = ['amory_uni_bin', 'lafrowda_uni_bin', 'birks_uni_bin']; // Add more as needed
    
    // Set status message
    function setStatus(message, type = 'info') {
        if (scanStatus) {
            scanStatus.textContent = message;
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
    
    function processQrCode(content) {
        if (validCodes.includes(content)) {
            qrCodeInput.value = content;
            
            setStatus('Valid QR code detected! Submitting...', 'success');
            
            // Submit form after a short delay
            setTimeout(function() {
                qrForm.submit();
            }, 800);
            
            return true;
        } else {
            setStatus('Invalid QR code. Please try a valid recycling bin QR code.', 'danger');
            return false;
        }
    }
    
    function initializeCamera() {
        setStatus('Camera initializing... Please wait.', 'info');
        
        try {
            let scannerDivId = 'qr-reader';
            let scannerDiv = document.getElementById(scannerDivId);
            
            if (!scannerDiv) {
                if (preview.tagName.toLowerCase() === 'video') {
                    scannerDiv = document.createElement('div');
                    scannerDiv.id = scannerDivId;
                    scannerDiv.style.width = '100%';
                    preview.parentNode.replaceChild(scannerDiv, preview);
                } else {
                    scannerDiv = preview;
                    scannerDiv.id = scannerDivId;
                }
            }
            
            // Initialize HTML5 QR code scanner
            const html5QrCode = new Html5Qrcode(scannerDivId);
            const config = { 
                fps: 10, 
                //qrbox: { width: 250, height: 250 },
                showTorchButtonIfSupported: false,
                showZoomSliderIfSupported: false,
                hideQrCodeScannerOnSuccess: true,
                rememberLastUsedCamera: true
            };
            
            // Start scanning
            html5QrCode.start(
                { facingMode: "environment" }, // Use back camera
                config,
                (decodedText) => {
                    // Success callback - QR code detected
                    console.log('QR code detected:', decodedText);
                    const valid = processQrCode(decodedText);
                    
                    // Stop scanning if valid QR code found
                    if (valid) {
                        html5QrCode.stop().then(() => {
                            console.log('Scanner stopped after valid code');
                        }).catch((err) => {
                            console.error('Error stopping scanner:', err);
                        });
                    }
                },
                (errorMessage) => {
                    // Error callback - mostly ignored during scanning
                    // We don't want to log every frame error
                }
            ).then(() => {
                setStatus('Camera active. Point camera at a QR code.', 'info');
            }).catch((err) => {
                console.error('Error starting camera:', err);
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
    
    // Initialize camera on page load
    initializeCamera();
});