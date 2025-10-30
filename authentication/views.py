import random
from datetime import timedelta
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.crypto import get_random_string
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from .forms import SignupForm
from .models import EmailOTP


# ---------------------- tools ------------------------
def generate_otp():
    return str(random.randint(100000, 999999))


def send_otp_email(user, code=None):
    if code is None:
        code = generate_otp()

    EmailOTP.objects.update_or_create(
        user=user,
        defaults={"code": code, "created_at": timezone.now(), "last_sent": timezone.now()}
    )

    subject = "کد تأیید حساب کاربری"
    from_email = "noreply@example.com"
    to = [user.email]
    html_content = f"""
    <!DOCTYPE html>
    <html lang=\"fa\" dir=\"rtl\">
    <head><meta charset=\"UTF-8\"></head>
    <body style=\"font-family:tahoma;background:#f9f9f9;\">
      <div style=\"max-width:600px;margin:auto;background:#fff;padding:20px;border-radius:10px;text-align:center;\">
        <h3>کد تأیید شما</h3>
        <div style=\"font-size:22px;font-weight:bold;letter-spacing:3px;background:#eee;padding:10px;margin:20px 0;border-radius:5px;\">
          {code}
        </div>
        <p>این کد تا ۵ دقیقه معتبر است.</p>
      </div>
    </body>
    </html>
    """
    msg = EmailMultiAlternatives(subject, "", from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return code


# ------------------- LOGIN ------------------------
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import redirect, render

def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, "ابتدا باید خارج شوید.")
        return redirect('/')

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if not user.is_active:
                messages.error(request, "اکانت شما فعال نشده است.")
                request.session['signup_user_id'] = user.id
                request.session['signup_email'] = user.email
                return redirect('verify_otp')

            login(request, user)
            messages.success(request, "با موفقیت وارد شدید.")
            return redirect('home')
        else:
            messages.error(request, "نام کاربری یا رمز اشتباه است.")
        return redirect('login')

    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "خارج شدید.")
    return redirect('/')


# ------------------- SIGNUP ------------------------


User = get_user_model()


def signup_view(request):
    if request.user.is_authenticated:
        messages.warning(request, "ابتدا خارج شوید.")
        return redirect('/')

    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            # بررسی یوزرنیم فعال
            if User.objects.filter(username=username, is_active=True).exists():
                messages.error(request, "این نام کاربری قبلاً استفاده شده است.")
                return redirect("signup")

            # بررسی ایمیل فعال
            active_user = User.objects.filter(email=email, is_active=True).first()
            if active_user:
                messages.error(request, "این ایمیل قبلاً استفاده شده است.")
                return redirect("signup")

            # حذف کاربر نیمه‌فعال قبلی با همان ایمیل
            User.objects.filter(email=email, is_active=False).delete()

            # ایجاد کاربر جدید نیمه‌فعال
            user = User.objects.create_user(
                username=username,
                email=email,
                is_active=False
            )
            user.set_unusable_password()  # پسورد واقعی بعد از OTP ست می‌شود
            user.save()

            # ارسال OTP
            code = generate_otp()
            send_otp_email(user, code)

            # ذخیره موقت در سشن
            request.session['signup_user_id'] = user.id
            request.session['signup_email'] = email
            request.session['signup_password'] = password

            messages.success(request, "کد OTP ارسال شد.")
            return redirect('verify_otp')

        else:
            # نمایش خطاهای فرم
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
            return redirect("signup")

    else:
        form = SignupForm()

    return render(request, "accounts/signup.html", {"form": form})


# ------------- VERIFY OTP ----------------
def verify_otp_view(request):
    # جلوگیری از دسترسی مستقیم
    if 'reset_user_id' not in request.session and 'signup_user_id' not in request.session:
        messages.error(request, "ابتدا باید درخواست OTP بدهید.")
        return redirect('login')

    if request.method == 'POST':
        code = request.POST.get('code')
        user_id = request.session.get('reset_user_id') or request.session.get('signup_user_id')

        try:
            user = User.objects.get(id=user_id)
            otp = user.otp_code
        except (User.DoesNotExist, EmailOTP.DoesNotExist):
            messages.error(request, "کد معتبر نیست.")
            return redirect('verify_otp')

        if otp.code == code and not otp.is_expired():
            otp.delete()

            if request.session.get('otp_purpose') == "reset_password":
                messages.success(request, "کد تایید شد، رمز جدید تعیین کنید.")
                return redirect('reset_password')

            # ثبت نام
            password = request.session.get('signup_password')
            user.is_active = True
            user.set_password(password)
            user.save()
            login(request, user)
            for key in ['signup_email', 'signup_password', 'signup_user_id']:
                request.session.pop(key, None)
            messages.success(request, f"خوش آمدید {user.username}")
            return redirect('home')

        messages.error(request, "کد اشتباه یا منقضی شده است.")
        return redirect('verify_otp')

    return render(request, 'accounts/verify_otp.html')


# --------------- RESEND OTP ----------------
def resend_otp(request):
    user_id = request.session.get("signup_user_id")
    if not user_id:
        return JsonResponse({"status": "error", "message": "کاربر یافت نشد!"})

    user = User.objects.get(id=user_id)
    otp_obj, created = EmailOTP.objects.get_or_create(user=user)

    if otp_obj.last_sent and timezone.now() < otp_obj.last_sent + timedelta(minutes=2):
        remaining = (otp_obj.last_sent + timedelta(minutes=2) - timezone.now()).seconds // 60 + 1
        return JsonResponse({"status": "error", "message": f"لطفاً {remaining} دقیقه دیگر تلاش کنید."})

    send_otp_email(user)
    otp_obj.last_sent = timezone.now()
    otp_obj.save()

    return JsonResponse({"status": "success", "message": "کد جدید ارسال شد!"})


# -------------- FORGOT PASSWORD ------------
def send_password_reset_email(user, otp_code=None):
    otp_code = otp_code or generate_otp()
    subject = "بازیابی رمز عبور"
    message = f"کد تایید شما برای بازیابی رمز عبور: {otp_code}\nاین کد تا ۵ دقیقه معتبر است."
    from_email = "noreply@example.com"
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)
    return otp_code


def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email, is_active=True)
        except User.DoesNotExist:
            messages.error(request, "کاربری با این ایمیل یافت نشد.")
            return redirect('forgot_password')

        code = send_password_reset_email(user)
        EmailOTP.objects.update_or_create(
            user=user,
            defaults={'code': code, 'created_at': timezone.now()}
        )

        request.session['reset_user_id'] = user.id
        request.session['otp_purpose'] = "reset_password"
        messages.success(request, "کد تایید ارسال شد.")
        return redirect('verify_otp')

    return render(request, 'accounts/forgot_password.html')



def reset_password_view(request):
    user_id = request.session.get('reset_user_id')
    if not user_id:
        messages.error(request, "کاربر یافت نشد.")
        return redirect('forgot_password')

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, "کاربر یافت نشد.")
        return redirect('forgot_password')

    if request.method == 'POST':
        password = request.POST.get('password', '').strip()
        confirm = request.POST.get('confirm_password', '').strip()

        if not password or not confirm:
            messages.error(request, "لطفاً هر دو فیلد را پر کنید.")
            return redirect(request.path)

        if password != confirm:
            messages.error(request, "عدم تطابق رمز عبور.")
            return redirect(request.path)

        if len(password) < 6:
            messages.error(request, "رمز باید حداقل ۶ کاراکتر باشد.")
            return redirect(request.path)

        # ذخیره رمز جدید
        user.set_password(password)
        user.save()
        if hasattr(user, 'otp_code'):
            user.otp_code.delete()

        request.session.pop('reset_user_id', None)
        messages.success(request, "رمز عبور با موفقیت تغییر کرد، حالا وارد شوید.")
        return redirect('login')

    return render(request, 'accounts/reset_password.html', {'user': user})
