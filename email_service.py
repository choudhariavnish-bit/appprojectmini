import smtplib
import os
from email.message import EmailMessage

# ✅ OPTIONAL: HTML support (ADDED ONLY)
from email.utils import make_msgid

# ---------------- EXISTING FUNCTION (UNCHANGED) ---------------- #
def send_booking_email(receiver_email, customer_name, category, pdf_path):
    msg = EmailMessage()
    msg['Subject'] = f'NexusReserve Booking Confirmation: {category}'
    msg['From'] = "your-email@gmail.com"  # <--- UPDATE THIS
    msg['To'] = receiver_email
    
    msg.set_content(f"Hello {customer_name},\n\nPlease find your {category} booking receipt attached.")

    # Attach the PDF
    if os.path.exists(pdf_path):
        with open(pdf_path, 'rb') as f:
            file_data = f.read()
            msg.add_attachment(
                file_data, 
                maintype='application', 
                subtype='pdf', 
                filename=os.path.basename(pdf_path)
            )
    else:
        print(f"Error: PDF file not found at {pdf_path}")
        return False

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login("your-email@gmail.com", "your-app-password") # <--- UPDATE THIS
            smtp.send_message(msg)
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False


# ---------------- NEW UPDATED FUNCTION (ADDED ONLY) ---------------- #
def send_booking_email(receiver_email, customer_name, category, pdf_path, amount=0):
    msg = EmailMessage()
    msg['Subject'] = f'NexusReserve Booking Confirmation - {category}'
    msg['From'] = "your-email@gmail.com"
    msg['To'] = receiver_email

    # Plain text fallback
    msg.set_content(f"""
Hello {customer_name},

Your {category} booking is confirmed.

Amount: ₹{amount}

Please find your invoice attached.

Thank you for choosing NexusReserve.
""")

    # ✅ HTML EMAIL (PROFESSIONAL LOOK)
    msg.add_alternative(f"""\
<html>
  <body style="font-family: Arial; background-color:#f5f5dc; padding:20px;">
    <div style="max-width:600px; margin:auto; background:white; padding:20px; border-radius:10px;">
      <h2 style="color:#556B2F;">NexusReserve Booking Confirmation</h2>
      
      <p>Hello <b>{customer_name}</b>,</p>
      
      <p>✅ Your <b>{category}</b> booking is <b>CONFIRMED</b>.</p>
      
      <p>💰 <b>Amount:</b> ₹{amount}</p>
      
      <p>📄 Your invoice is attached with this email.</p>
      
      <hr>
      <p style="font-size:12px; color:gray;">Thank you for choosing NexusReserve.</p>
    </div>
  </body>
</html>
""", subtype='html')

    # Attach PDF
    if os.path.exists(pdf_path):
        with open(pdf_path, 'rb') as f:
            msg.add_attachment(
                f.read(),
                maintype='application',
                subtype='pdf',
                filename=os.path.basename(pdf_path)
            )
    else:
        print(f"PDF not found: {pdf_path}")
        return False

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login("your-email@gmail.com", "your-app-password")
            smtp.send_message(msg)
        print("✅ Email sent successfully")
        return True
    except Exception as e:
        print("❌ Email failed:", e)
        return False