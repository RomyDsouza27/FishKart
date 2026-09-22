# foodkart/context_processors.py
from django.conf import settings

def razorpay_keys(request):
    return {
        'RAZORPAY_KEY_ID': settings.RAZORPAY_KEY_ID,
        'RAZORPAY_KEY_SECRET': settings.RAZORPAY_KEY_SECRET,
    }
