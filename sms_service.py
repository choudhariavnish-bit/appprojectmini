# sms_service.py
import os
from twilio.rest import Client

# Note: In a production environment, keep these credentials in your Django settings.py or environment variables.
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', 'ACd954317eebebfc4b01a8101412d2584d')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', 'ee9347fe34539100b85a5036972f33cb')
TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER', '+917066958282')

def send_booking_sms(to_phone, customer_name, category, amount):
    """Sends a transactional confirmation SMS via Twilio API."""
    try:
        # Prevent API crashes if credentials aren't configured yet
        if "your_" in TWILIO_ACCOUNT_SID:
            print(f"[Simulation] SMS sent to {to_phone}: Hi {customer_name}, your {category} booking is confirmed! Total: ₹{amount}")
            return True

        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        message_body = (
            f"NexusReserve Confirmation\n\n"
            f"Hello {customer_name},\n"
            f"Your booking for {category} has been successfully confirmed. "
            f"Total Bill: ₹{amount}.\n\n"
            f"Thank you for choosing NexusReserve!"
        )

        message = client.messages.create(
            body=message_body,
            from_=TWILIO_PHONE_NUMBER,
            to=to_phone
        )
        return True
    except Exception as e:
        print(f"Failed to send SMS via Twilio: {e}")
        return False