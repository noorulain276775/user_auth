from django.forms import ValidationError
from django.shortcuts import render, redirect
from accounts.forms import *
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from accounts.backend import *
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


class SignUpView(View):

    def get(self, request, *args, **kwargs):
        user_form = UserSignup()
        return render(request, 'user_signup.html', {'user_form': user_form})

    def post(self, request, *args, **kwargs):
        try:
            user_form = UserSignup(request.POST)
            if not user_form.errors:
                if user_form.is_valid():
                    phone = user_form.cleaned_data['phone']
                    password = user_form.cleaned_data['password']
                    confirm_password = user_form.cleaned_data['confirm_password']
                    first_name = user_form.cleaned_data['first_name']
                    last_name = user_form.cleaned_data['last_name']
                    phone_validity = validate_phone(phone)
                    password_validity = password_is_valid(
                        password, confirm_password)
                    if phone_validity == True:
                        if password_validity == True:
                            otp = send_otp(phone)
                            if otp is not None:
                                request.session['otp'] = otp
                                request.session['phone'] = phone
                                request.session['first_name'] = first_name
                                request.session['last_name'] = last_name
                                request.session['password'] = password
                                return redirect('otp')
                            else:
                                return redirect('signup')
                        else:
                            messages.error(
                                request, 'Please enter the password again')
                            return redirect('signup')
                    else:
                        messages.error(
                            request, 'Phone number is not in valid format')
                        return redirect('signup')
                else:
                    messages.error(
                        request, 'Form is invalid, please fill it again')
                    return redirect('signup')
            else:
                messages.error(request, 'Form is not valid, PLease fill it again')
                return redirect('signup')
        except:
            return ValidationError("An error occured while signing up")


class OTPView(View):

    def get(self, request, *args, **kwargs):
        if request.META.get('HTTP_REFERER') != 'http://127.0.0.1:8000/':
            return redirect('signup')
        otp_form = OTP_Form()
        return render(request, 'otp.html', {'otp_form': otp_form})

    def post(self, request, *args, **kwargs):
        try:
            otp = request.session.get('otp')
            first_name = request.session.get('first_name')
            last_name = request.session.get('last_name')
            password = request.session.get('password')
            phone = request.session.get('phone')
            otp_form = OTP_Form(request.POST)
            if otp_form.is_valid():
                get_otp = otp_form.cleaned_data['otp']
                if get_otp == otp:
                    user = MyUser.objects.create_user(
                        phone=phone, password=password, first_name=first_name, last_name=last_name)
                    user.save()
                    otp_entry = OTP.objects.create(user_id=user, otp=otp)
                    otp_entry.save()
                    delete_session(request)
                    messages.success(
                        request, 'Your account has been created')
                    return redirect('login')
                else:
                    messages.error(request, 'Incorrect OTP')
                    return redirect('otp')
            else:
                messages.error(request, 'Please enter the OTP again')
                return redirect('otp')
        except:
            messages.error(request, 'Please try signing up again')
            return redirect('signup')


class LoginView(View):

    def get(self, request, *args, **kwargs):
        loginform = UserLoginForm()
        return render(request, 'signin.html', {'loginform': loginform})

    def post(self, request, *args, **kwargs):
        try:
            loginform = UserLoginForm(request.POST)
            if loginform.is_valid():
                phone = loginform.cleaned_data['phone']
                password = loginform.cleaned_data['password']
                user = authenticate(phone=phone, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home', id=user.id)
                else:
                    messages.error(request, "Invalid phone or password.")
                    return redirect('login')
            else:
                messages.error(request, "Invalid phone or password.")
                return redirect('login')
        except:
            messages.error(request, "Please try agin")
            return redirect('login')


# Reset Password section

class ResetPasswordPhoneView(View):
    def get(self, request, *args, **kwargs):
        if request.META.get('HTTP_REFERER') != 'http://127.0.0.1:8000/login/':
            return redirect('login')
        reset_form = Reset_Password_phones_Form()
        return render(request, 'phone.html', {'reset_form': reset_form})

    def post(self, request, *args, **kwargs):
        try:
            reset_form = Reset_Password_phones_Form(request.POST)
            if reset_form.is_valid():
                phone = reset_form.cleaned_data['phone']
                if validate_phone(phone) == True:
                    user = MyUser.objects.filter(phone=phone).first()
                    if user:
                        otp = send_otp(phone)
                        request.session['otp'] = otp
                        request.session['phone'] = phone
                        return redirect('otp_reset')
                    else:
                        messages.error(request, "This phone number is not registered ")
                        return redirect('login')
                else:
                    messages.error(request, "The phone is not in valid format (923xxxxxxxxx)")
                    return redirect('login')   
            else:
                messages.error(request, "Please fill again.")
                return redirect('login')
        except:
            messages.error(request, "Please try agin")
            return redirect('login')


class ResetPasswordOTPView(View):

    def get(self, request, *args, **kwargs):
        if request.META.get('HTTP_REFERER') != 'http://127.0.0.1:8000/phone/':
            return redirect('login')
        otp_form = OTP_Form()
        return render(request, 'otp.html', {'otp_form': otp_form})

    def post(self, request, *args, **kwargs):
        try:
            otp = request.session.get('otp')
            otp_form = OTP_Form(request.POST)
            if otp_form.is_valid():
                get_otp = otp_form.cleaned_data['otp']
                if get_otp == otp:
                    request.session.pop('otp')
                    return redirect('password_reset')
                else:
                    messages.error(request, 'Incorrect OTP')
                    return redirect('otp')
            else:
                messages.error(request, 'Please enter the OTP again')
                return redirect('otp')
        except:
            messages.error(request, 'Please enter the OTP again')
            return redirect('otp')


class ResetPasswordView(View):
    def get(self, request, *args, **kwargs):
        if request.META.get('HTTP_REFERER') != 'http://127.0.0.1:8000/otp_reset/':
            return redirect('login')
        password_reset = ResetPassword()
        return render(request, 'reset_password.html', {'password_reset': password_reset})

    def post(self, request, *args, **kwargs):
        try:
            password_reset = ResetPassword(request.POST)
            if password_reset.is_valid():
                new_password = password_reset.cleaned_data['new_password']
                confirm_password = password_reset.cleaned_data['confirm_password']
                phone= request.session.get('phone')
                valid_password = password_is_valid(
                    new_password, confirm_password)
                if valid_password == True:
                    user = MyUser.objects.filter(phone=phone).first()
                    user.set_password(new_password)
                    user.save()
                    messages.success(request, "Password changed successfully. ")
                    return redirect('login')
                else:
                    messages.error(request, "Both passwords do not match")
                    return redirect('login')
            else:
                messages.error(request, "Invalid phone or password.")
                return redirect('login')
        except:
            messages.error(request, "Please try agin")
            return redirect('login')


class UserLogout(LoginRequiredMixin, View):
    def get(self, request):
        login_url = 'login/'
        logout(request)
        messages.success(request, "You have been logged out successfully")
        return redirect('login')


class HomeView(LoginRequiredMixin, View):
    def get(self, request, id):
        login_url = 'login/'
        user = MyUser.objects.filter(id=id).first()
        return render(request, "home.html", {"first_name": user.first_name, "last_name": user.last_name})
