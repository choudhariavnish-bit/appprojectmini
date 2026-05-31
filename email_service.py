import smtplib
import os
from email.message import EmailMessage

def send_booking_email(receiver_email, customer_name, category, pdf_path, amount=0):
    msg = EmailMessage()
    msg['Subject'] = f'NexusReserve Booking Confirmation - {category}'
    msg['From'] = "pratikgorade826@gmail.com"  # 👈 Replace with your real Gmail address
    msg['To'] = receiver_email

    # Plain text fallback
    msg.set_content(f"""
Hello {customer_name},

Your {category} booking is confirmed.
Amount: r.{amount}

Please find your invoice attached.
Thank you for choosing NexusReserve.
""")

    # HTML Email Layout
    msg.add_alternative(f"""\
<html>
  <body style="font-family: Arial; background-color:#f5f5dc; padding:20px;">
    <div style="max-width:600px; margin:auto; background:white; padding:20px; border-radius:10px;">
      <h2 style="color:#556B2F;">NexusReserve Booking Confirmation</h2>
      <p>Hello <b>{customer_name}</b>,</p>
      <p>Your <b>{category}</b> booking is <b>CONFIRMED</b>.</p>
      <p><b>Amount:</b> r.{amount}</p>
      <p>Your invoice is attached with this email.</p>
      <hr>
      <p style="font-size:12px; color:gray;">Thank you for choosing NexusReserve.</p>
    </div>
  </body>
</html>
""", subtype='html')

    # Attach PDF attachment payload safely
    if pdf_path and os.path.exists(pdf_path):
        with open(pdf_path, 'rb') as f:
            msg.add_attachment(
                f.read(),
                maintype='application',
                subtype='pdf',
                filename=os.path.basename(pdf_path)
            )
    else:
        print(f"[WARNING] PDF attachment not found at {pdf_path}. Proceeding with message only.")

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            # 💡 Your generated string is injected below as the authentication token (no spaces)
            smtp.login("pratikgorade826@gmail.com", "iwxadryzithmhztw") 
            smtp.send_message(msg)
        print("[SUCCESS] Email sent successfully via SMTP!")
        return True
    except Exception as e:
        print(f"[ERROR] SMTP Email delivery failed: {e}")
        return False