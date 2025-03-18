# Author: Joshua Money
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from leaderboard.utils import update_leaderboard

from profiles.models import Profile


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
<<<<<<< Updated upstream
            update_leaderboard(request.user, "qr_scan", points=points_earned)
            message = f"♻️Great job! You have earned {points_earned} points for recycling!♻️"
=======

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

                    profile, created = Profile.objects.get_or_create(user=request.user)
                    profile.add_points(points_earned)

                    message = f"♻️Great job! You have earned {points_earned} points for recycling!♻️"
                    # Simple redirect to result page
                    return render(request, 'qr/qr_result.html', {"message": message, "status": "success"})
                except IntegrityError:
                    message = "You've already scanned this QR code today. Come back tomorrow!"
                    return render(request, 'qr/qr_result.html', {"message": message, "status": "warning"})
>>>>>>> Stashed changes
        else:
            message = "Invalid QR code. Please try again."
            
        return render(request, 'qr/qr_result.html', {"message": message})
    else:
        # For GET requests, rendering QR scanning page. 
        return render(request, "qr/qr.html")