# Author: Joshua Money
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from leaderboard.utils import update_leaderboard
from django.utils import timezone
from django.db import IntegrityError
from .models import QRScan

# Create your views here.
@login_required
def scan_qr(request):

    today = timezone.now().date()

    if request.method == "POST":
    # Retrieve the QR code content from POST data
        qr_code_content = request.POST.get("qr_code", "").strip()

        # Validate QR code
        valid_qr_codes = {
            "amory_uni_bin": 20,
            "lafrowda_uni_bin": 20,
            "birks_uni_bin": 20, # key: QR code string, value: points awarded
        }

        if qr_code_content in valid_qr_codes:
            points_earned = valid_qr_codes[qr_code_content]

            already_scanned_today = QRScan.objects.filter(
                user=request.user,
                scan_date=today,
                qr_code=qr_code_content,
            ).exists()
            
            if already_scanned_today:
                message = "You've already scanned this QR code today. Come back tomorrow!"
                return render(request, 'qr/qr_result.html', {"message": message, "status": "warning"})
            else:
                try: 
                    QRScan.objects.create(
                        user=request.user,
                        scan_date=today,
                        qr_code = qr_code_content,
                        points_earned=points_earned
                    )
                    update_leaderboard(request.user, "qr_scan", points=points_earned)
                    message = f"♻️Great job! You have earned {points_earned} points for recycling!♻️"
                    # Redirect with parameters for mascot message
                    return redirect(f'/qr/result?points_earned={points_earned}&activity=qr_scan&status=success&message={message}')
                except IntegrityError:
                    message = "You've already scanned this QR code today. Come back tomorrow!"
                    return render(request, 'qr/qr_result.html', {"message": message, "status": "warning"})
        else:
            message = "Invalid QR code. Please try again."
            return render(request, 'qr/qr_result.html', {"message": message, "status": "error"})
    else:
        # For GET requests, rendering QR scanning page. 
        return render(request, "qr/qr.html")

@login_required
def qr_result(request):
    message = request.GET.get('message', '')
    status = request.GET.get('status', '')
    return render(request, 'qr/qr_result.html', {"message": message, "status": status})