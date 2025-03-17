# Author: Joshua Money
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from leaderboard.utils import update_leaderboard
from django.contrib import messages

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
            messages.success(request, f"♻️ Great job! You have earned {points_earned} points for recycling! ♻️")
        else:
            messages.error(request, "❌ Invalid QR code. Please try again.")
            
        return redirect("qr_scan") # Redirect to the same page to clear the form
    else:
        # For GET requests, rendering QR scanning page. 
        return render(request, "qr/qr.html")