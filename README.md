# 📧 Django Email OTP Authentication

A simple and secure **Django authentication system** that verifies users via **One-Time Passwords (OTP)** sent to their email address.

---

## 🧩 About the Project

This project is built with **Django** and provides an authentication flow using **email-based OTP verification**.  
When a user signs up or logs in, an OTP code is sent to their registered email, which they must enter to complete verification.

---

## ✨ Features

- 🔐 Email-based signup and login verification  
- 📩 Automatic OTP generation and sending via SMTP  
- 🔁 Password reset via email OTP  
- 💻 Clean and responsive UI built with Tailwind CSS  
- 🧱 Modular structure for easy customization and scaling  
- 🧤 Secure handling of user data and environment variables  

---

## ⚙️ Technologies Used

- **Python 3.x**  
- **Django 5.x**  
- **Tailwind CSS**  
- **SQLite** (default database)  

---

## 🚀 Installation & Setup

### Install required packages

Make sure you have `pip` installed, then run:

```bash
pip install django python-dotenv
```

💡 **Hint:**  
- `django` is the main web framework.  
- `python-dotenv` lets you safely manage secret data (like email passwords) in a `.env` file.  

---

### Configure your email settings

Create a `.env` file in the project root:

```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=youremail@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
```

💡 **Hint:**  
- For Gmail, enable **2-Step Verification** and create an **App Password**.  
- For other providers, replace SMTP host/port accordingly.  
- `.env` is ignored by Git, so credentials are safe.

---

### Apply database migrations

```bash
python manage.py migrate
```

💡 **Hint:** This command creates all necessary tables for users, OTP codes, and sessions.

---

### Create a superuser (optional)

```bash
python manage.py createsuperuser
```

💡 **Hint:** Access Django admin at `http://127.0.0.1:8000/admin`.

---

### Run the development server

```bash
python manage.py runserver
```

Open your browser at:

👉 `http://127.0.0.1:8000/`

💡 **Hint:** Check Django console for OTP email logs if testing locally.

---

### Test the OTP flow

1. Go to **Sign Up**.  
2. Enter a valid email and password.  
3. Check your inbox — you should receive:

```
Subject: Your OTP Code
Your One-Time Password (OTP) is: 483921
```

4. Enter the OTP to verify your account.  

💡 **Hint:** OTPs expire quickly (e.g., 2 minutes). Request a new one if needed.

---

### (Optional) Customize the look

Edit templates in `templates/accounts/` or static files in `static/`.  

💡 **Hint:** Tailwind CSS allows easy UI customization without touching authentication logic.

---

### ✅ Everything is ready!

You can now:  
- Sign up new users  
- Verify emails with OTP  
- Log in securely  
- Reset passwords via email  

---

## 🧭 User Guide (How to Use)

**Step 1:** Open the homepage → options to Sign Up or Log In.  
**Step 2:** Register with an email → receive OTP → verify.  
**Step 3:** Log in with email/password → verify OTP.  
**Step 4:** Forgot password → request OTP → reset password.

---

## 🧤 Security Notes

- `.env` and `db.sqlite3` are ignored by Git.  
- Passwords are hashed — no plaintext storage.  
- OTPs are randomly generated and expire quickly.  
- Sensitive data stays local and secure.

---

## 🧠 How It Works

1. User signs up/logs in.  
2. System generates OTP.  
3. OTP sent via email.  
4. User enters OTP to verify.  
5. Access granted.

---

## 🧩 Folder Structure (Simplified)

```
django-email-otp-auth/
│
├── accounts/               # Authentication app
│   ├── views.py
│   ├── models.py
│   ├── forms.py
│   └── templates/accounts/
│
├── django_email_otp_auth/  # Project settings
│   └── settings.py
│
├── static/                 # CSS, JS, images
├── templates/              # Global templates
├── manage.py
└── .env (not included)
```

---

## 💡 Purpose

Clean, reusable foundation for Django projects needing **email-based OTP authentication**.  
Ideal for login systems, admin portals, or verification flows without third-party APIs.

---

## 🧾 License

MIT License — open-source.

---

👨‍💻 Developed with ❤️ using Django and Tailwind CSS
