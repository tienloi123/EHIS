import smtplib
import string
import random
from email.mime.text import MIMEText


def generate_password(min_char: int = 15, max_char: int = 20):
    password_length = random.randint(min_char, max_char)
    password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(password_length))
    return password

def generate_otp(length=6):
    """
    Tạo mã OTP ngẫu nhiên với độ dài xác định (mặc định là 6).
    """
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])

async def send_email(to_email, subject, body):
    """
    Gửi email với nội dung cụ thể.
    """
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_user = 'doantienloi123@gmail.com'  # Thay bằng email của bạn
    smtp_password = 'kfmwrmymdgzcvqzy'  # Thay bằng mật khẩu ứng dụng từ Gmail

    msg = MIMEText(body, "plain", "utf-8")
    msg['Subject'] = subject
    msg['From'] = smtp_user
    msg['To'] = to_email

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Kích hoạt mã hóa TLS
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
        print(f"Email đã được gửi đến {to_email}")
    except Exception as e:
        print(f"Lỗi khi gửi email: {e}")
        raise
