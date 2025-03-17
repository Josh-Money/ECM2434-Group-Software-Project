//Author: Josh Money

//Initialize sccane on the video element
let scanner = new Instascan.Scanner({ video: document.getElementById('preview') });
scanner.addListener('scan', function (content) {
    //Populate the form field with the scanned QR code content
    document.getElementById('qr_code').value = content;
    // document.forms[0].submit(); // auto submits
});

Instascan.Camera.getCameras().then(function (cameras) {
    if (cameras.length > 0) {
        // Choose first available camera
        scanner.start(cameras[0]);
    } else {
        console.error('No cameras found.');
        alert('No cameras found. Please enter the QR code manually.');
    }
}).catch(function (e) {
    console.error(e);
    alert('Error intializing QR scanner: ' + e);
});

document.addEventListener("DOMContentLoaded", () => {
    const toast = document.querySelector('.toast');
    if (toast) {
        toast.classList.add("show");
        setTimeout(() => {
            toast.classList.remove("show");
        }, 3000); // Toast disappears after 3 seconds
    }
});