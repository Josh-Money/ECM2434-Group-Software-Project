# Author: Joshua Money
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from leaderboard.utils import update_leaderboard

# Create your views here.
@login_required
def scan_qr(request):
    if request.method == "POST":
    # Retrieve the QR code content from POST data
        qr_code_content = request.POST.get("qr_code", "").strip()

        # Validate QR code
        valid_qr_codes = {
            "recycling_uni_bin": 20, # key: QR code string, value: points awarded
        }

        if qr_code_content in valid_qr_codes:
            points_earned = valid_qr_codes[qr_code_content]
            update_leaderboard(request.user, "qr_scan", points=points_earned)
            message = f"♻️Great job! You've earned {points_earned} points for recycling!♻️"
        else:
            message = "Invalid QR code. Please try again."
            
        return render(request, 'qr/qr_result.html', {"message": message})
    else:
        # For GET requests, rendering QR scanning page. 
        return render(request, "qr/qr.html")