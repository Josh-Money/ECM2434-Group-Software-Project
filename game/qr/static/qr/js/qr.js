// Author: Josh Money

document.addEventListener('DOMContentLoaded', function() {
    const preview = document.getElementById('preview');
    const scanStatus = document.getElementById('scanStatus');
    const qrForm = document.getElementById('qrForm');
    const qrCodeInput = document.getElementById('qr_code');

    if (preview) {
        preview.innerHTML = '';
        preview.style.width = '100%';
        preview.style.maxWidth = '300px';
        preview.style.minHeight = '250px';
        preview.style.margin = '0 auto 80px';
        preview.style.display = 'block';
        preview.style.border = '1px solid #ddd';
        preview.style.borderRadius = '4px';
        preview.style.position = 'relative';
        preview.style.overflow = 'hidden';
    }

    function isMobileDevice() {
        return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    }

    let cameraButton = null;
    if (isMobileDevice()) {
        cameraButton = document.createElement('button');
        cameraButton.textContent = 'Activate Camera';
        cameraButton.className = 'btn btn-primary mb-3';
        cameraButton.type = 'button';
        cameraButton.style.width = '100%';
        cameraButton.style.maxWidth = '300px';
        cameraButton.style.padding = '10px';
        cameraButton.style.margin = '0 auto 15px';
        cameraButton.style.display = 'block';

        const container = preview.parentNode;
        container.parentNode.insertBefore(cameraButton, container);
    }

    const validCodes = ['amory_uni_bin', 'lafrowda_uni_bin', 'birks_uni_bin'];

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

            setTimeout(function() {
                qrForm.submit();
            }, 800);

            return true;
        } else {
            setStatus('Invalid QR code. Please try a valid recycling bin QR code.', 'danger');
            return false;
        }
    }

    let html5QrCodeScanner = null;

    function initializeCamera() {
        setStatus('Camera initializing... Please wait.', 'info');

        try {
            if (html5QrCodeScanner) {
                html5QrCodeScanner.clear();
            }
            
            const html5QrCode = new Html5Qrcode(preview.id);
            
            Html5Qrcode.getCameras().then(cameras => {
                if (cameras && cameras.length) {
                    let cameraId = cameras[0].id;
                    for (let camera of cameras) {
                        if (camera.label && (camera.label.toLowerCase().includes('back') || camera.label.toLowerCase().includes('rear'))) {
                            cameraId = camera.id;
                            break;
                        }
                    }
                    
                    const config = {
                        fps: 10,
                        qrbox: { width: 150, height: 150 },
                        aspectRatio: 1.0
                    };
                    
                    html5QrCode.start(
                        cameraId, 
                        config,
                        (decodedText) => {
                            console.log(`QR Code detected: ${decodedText}`);
                            html5QrCode.stop();
                            processQrCode(decodedText);
                        },
                        (errorMessage) => {
                            // Ignore errors during scanning
                        }
                    ).then(() => {
                        if (cameraButton) cameraButton.style.display = 'none';
                        setStatus('Camera active. Point camera at a QR code.', 'info');
                        
                        setTimeout(() => {
                            const videoElement = document.querySelector(`#${preview.id} video`);
                            if (videoElement) {
                                videoElement.style.width = '100%';
                                videoElement.style.height = 'auto';
                                videoElement.style.maxHeight = '250px';
                                videoElement.style.borderRadius = '4px';
                                videoElement.style.display = 'block';
                            }
                            
                            const canvasElements = document.querySelectorAll(`#${preview.id} canvas`);
                            canvasElements.forEach(canvas => {
                                canvas.style.maxWidth = '100%';
                                canvas.style.maxHeight = '250px';
                            });
                            
                            const scannerUIElements = document.querySelectorAll('.html5-qrcode-element');
                            scannerUIElements.forEach(element => {
                                element.style.position = 'relative';
                                element.style.maxWidth = '300px';
                                element.style.margin = '0 auto';
                            });
                        }, 500);
                    }).catch((err) => {
                        console.error("Error starting camera:", err);
                        setStatus('Error starting camera. Please try a different browser.', 'danger');
                    });
                    
                    html5QrCodeScanner = html5QrCode;
                } else {
                    setStatus('No cameras found. Please try a different device.', 'danger');
                }
            }).catch(err => {
                console.error("Camera access error:", err);
                setStatus('Error accessing camera. Please allow camera access and refresh.', 'danger');
            });
        } catch (err) {
            console.error("Camera init error:", err);
            setStatus('Error initializing camera. Please refresh.', 'danger');
        }
    }

    qrForm.addEventListener('submit', function(event) {
        const code = qrCodeInput.value.trim();
        
        if (!code) {
            setStatus('Please scan a QR code or enter a valid code.', 'warning');
            event.preventDefault();
            return;
        }
        
        if (!validCodes.includes(code)) {
            setStatus('Invalid QR code. Please try again.', 'danger');
            event.preventDefault();
        } else {
            setStatus('Valid QR code!', 'success');
            console.log('Submitting valid QR code:', code);
        }
    });

    if (isMobileDevice()) {
        if (cameraButton) {
            setStatus('Click "Activate Camera" to begin scanning QR codes', 'info');
            cameraButton.addEventListener('click', function() {
                initializeCamera();
            });
        }
    } else {
        initializeCamera();
    }
});
