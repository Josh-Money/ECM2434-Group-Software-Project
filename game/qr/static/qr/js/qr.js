//Author: Josh Money

document.addEventListener('DOMContentLoaded', function() {
    // Get DOM elements
    const preview = document.getElementById('preview');
    const scanStatus = document.getElementById('scanStatus');
    const qrForm = document.getElementById('qrForm');
    const qrCodeInput = document.getElementById('qr_code');
    
    if (preview) {
        preview.style.width = '100%';
        preview.style.maxWidth = '400px';
        preview.style.height = 'auto';
        preview.style.margin = '0 auto';
        preview.style.display = 'block';
        preview.setAttribute('playsinline', 'true');
        preview.setAttribute('autoplay', 'true');
        preview.setAttribute('muted', 'true');
    }
    
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
        
        const container = preview.parentNode;
        container.parentNode.insertBefore(cameraButton, container);
    }
    
    // Valid QR codes
    const validCodes = ['amory_uni_bin', 'lafrowda_uni_bin', 'birks_uni_bin'];
    
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
    
    // Check if QR code is valid and submit form if it is
    function processQrCode(content) {
        if (validCodes.includes(content)) {
            qrCodeInput.value = content;
            
            setStatus('Valid QR code detected! Submitting...', 'success');
            
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
            
            Instascan.Camera.getCameras()
                .then(function(cameras) {
                    if (cameras.length > 0) {
                        console.log('Available cameras:', cameras.map(c => c.name || 'unnamed camera'));
                        
                        // Default to first camera
                        let selectedCamera = cameras[0];
                        
                        if (isMobileDevice()) {
                            for (let i = 0; i < cameras.length; i++) {
                                if (cameras[i].name && cameras[i].name.toLowerCase().includes('back')) {
                                    console.log('Selected back camera by name');
                                    selectedCamera = cameras[i];
                                    break;
                                }
                            }
                            
                            if (cameras.length === 2 && selectedCamera === cameras[0]) {
                                console.log('Two cameras found, selecting the second one');
                                selectedCamera = cameras[1];
                            }
                        }
                        
                        console.log('Selected camera:', selectedCamera.name || 'unnamed camera');
                        
                        scanner.start(selectedCamera)
                            .then(function() {
                                setStatus('Camera active. Point camera at a QR code.', 'info');
                                // Hide the button once camera is active
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
    
    qrForm.addEventListener('submit', function(event) {
        const code = qrCodeInput.value.trim();
        
        if (!code) {
            setStatus('Please scan a QR code or enter a valid code.', 'warning');
            event.preventDefault(); // Prevent empty submission
            return;
        }
        
        if (!validCodes.includes(code)) {
            setStatus('Invalid QR code. Please try again.', 'danger');
            event.preventDefault(); // Prevent form submission
        } else {
            setStatus('Valid QR code!', 'success');
            console.log('Submitting valid QR code:', code);
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