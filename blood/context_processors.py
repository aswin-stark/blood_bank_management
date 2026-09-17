from donor.models import BloodDonate
from blood.models import BloodRequest


def pending_donations(request):
    """Expose the outstanding donation-review count to the admin layout."""
    if not request.user.is_authenticated:
        return {
            'pending_donation_count': 0,
            'pending_blood_request_count': 0,
        }

    return {
        'pending_donation_count': BloodDonate.objects.filter(status='Pending').count(),
        'pending_blood_request_count': BloodRequest.objects.filter(status='Pending').count(),
    }
