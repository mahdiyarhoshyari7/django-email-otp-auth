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

1. Create a virtual environment and activate it
   
python -m venv venv
venv\Scripts\activate   # On Windows
# OR
source venv/bin/activate  # On macOS/Linux


💡 Hint: Creating a virtual environment keeps all your project dependencies isolated from other Python projects on your system.

2. Install required packages

Make sure you have pip installed, then run:

pip install django python-dotenv


💡 Hint:

django is the main web framework.

python-dotenv lets you safely manage secret data (like email passwords) in a .env file.

3. Configure your email settings

To send OTP codes via email, you need to set up your SMTP credentials.
In the project’s root directory, create a new file named .env and add:

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=youremail@gmail.com
EMAIL_HOST_PASSWORD=your_app_password


💡 Hint:

For Gmail, you must enable 2-Step Verification and create an App Password.

If you’re using another provider (like Outlook or Yahoo), replace the SMTP host and port with their values.

Your .env file is hidden from GitHub thanks to .gitignore, so your credentials are safe.

4. Apply database migrations
python manage.py migrate


💡 Hint: This command creates all necessary database tables for users, OTP codes, and sessions.

5. Create a superuser (optional)
python manage.py createsuperuser


💡 Hint: This allows you to log into Django’s admin panel at http://127.0.0.1:8000/admin.

6. Run the development server
python manage.py runserver


Then open your browser and go to:

👉 http://127.0.0.1:8000/

💡 Hint:

If you’re testing email OTP locally, make sure your email credentials in .env are correct.

You can check the Django console output — it will show logs whenever an OTP email is sent.

7. Test the OTP flow

Go to the Sign Up page.

Register with a real email address.

Check your inbox — you should receive a message like:

Subject: Your OTP Code
Your One-Time Password (OTP) is: 483921


Enter the code on the verification page to complete your registration.

💡 Hint: OTPs are short-lived (e.g., 2 minutes). If it expires, you can request a new one.

8. (Optional) Customize the look

If you want to adjust styles, open your templates inside templates/accounts/ and static files in static/.
This project uses Tailwind CSS, which you can extend or modify easily.

💡 Hint: You can include your own logo, colors, and layouts without affecting authentication logic.

✅ Everything is ready!

Now your Django Email OTP Authentication system is up and running.
You can:

Sign up new users

Verify their emails with OTP

Log in securely

Reset passwords via email

🧭 User Guide (How to Use)

After you’ve installed and run the project, here’s how users can interact with the system:

🔹 Step 1: Open the website

Go to the homepage — you’ll see options to Sign Up or Log In.

🔹 Step 2: Register a new account

Click on Sign Up

Enter your email address and password

Click Submit — an OTP (One-Time Password) will be sent to your email

🔹 Step 3: Verify your email with OTP

Check your email inbox

Copy the 6-digit OTP code

Paste it into the verification form on the website

Click Verify — your account is now activated ✅

🔹 Step 4: Log in

Now you can log in using your email and password.
After entering them, the system will send another OTP to verify it’s really you.
Enter the code again to complete login.

🔹 Step 5: Reset password (if you forget)

Go to the Forgot Password page

Enter your registered email

An OTP will be sent to your email

Verify the OTP and set a new password

🧤 Security Notes

.env and db.sqlite3 are ignored by Git (not uploaded to GitHub).

Django handles password hashing automatically — no plaintext passwords are stored.

OTPs are randomly generated and expire quickly.

All sensitive data (like your Gmail password) stays local and safe.

🧠 How It Works

User signs up or logs in with an email.

System generates a unique OTP.

OTP is sent via SMTP to the user’s email.

User enters the OTP to verify their identity.

After successful verification, user gains access.

🧩 Folder Structure (Simplified)
django-email-otp-auth/
│
├── accounts/            # Authentication app
│   ├── views.py
│   ├── models.py
│   ├── forms.py
│   └── templates/accounts/
│
├── django_email_otp_auth/   # Project settings
│   └── settings.py
│
├── static/              # CSS, JS, images
├── templates/           # Global templates
├── manage.py
└── .env (not included)

💡 Purpose

This project serves as a clean, reusable foundation for any Django project requiring email-based authentication with OTP —
ideal for login systems, admin portals, or verification flows without using third-party APIs.

🧾 License

This project is open-source and available under the MIT License.

👨‍💻 Developed with ❤️ using Django and Tailwind CSS
