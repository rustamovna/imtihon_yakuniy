from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from .models import VerificationCode
from django.utils.crypto import get_random_string
from django.utils import timezone
from .forms import UserRegisterForm, ProfileUpdateForm, PasswordResetRequestForm, CodeConfirmForm, PasswordSetForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from users.models import Profile  # yoki qaerda saqlangan bo'lsa shu path

# Create your views here.

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            messages.success(request, "Ro'yxatdan o'tish muvaffaqiyatli")
            return redirect('ads:list')
        else:
            messages.error(request, "Xatolik: forma noto‘g‘ri to‘ldirildi ❌")
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile_view(request):
    if request.method == 'POST':
        pform = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if pform.is_valid():
            pform.save()
            messages.success(request, "Profil yangilandi")
            return redirect('users:profile')
    else:
        pform = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'users/profile.html', {'pform': pform})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print("POST:", request.POST)  
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Kirish muvaffaqiyatli ✅")
            return redirect('ads:list')
        else:
            messages.error(request, "Login yoki parol xato ❌")
    return render(request, 'users/login.html')


def find_user_by_identifier(identifier):
    try:
        user = User.objects.get(email__iexact=identifier)
        return user
    except User.DoesNotExist:
        pass
    try:
        user = User.objects.get(username__iexact=identifier)
        return user
    except User.DoesNotExist:
        pass
    
    try:
        profile = Profile.objects.get(phone__iexact=identifier)
        return profile.user
    except Profile.DoesNotExist:
        pass
    return None


def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            ident = form.cleaned_data['identifier'].strip()
            user = find_user_by_identifier(ident)
            if not user:
                messages.error(request, "Foydalanuvchi topilmadi.")
            else:
                code = get_random_string(length=6, allowed_chars='0123456789')
                VerificationCode.objects.create(user=user, code=code, purpose='pw_reset')
                print(f"[PASSWORD RESET CODE] user={user.username} code={code}")
                messages.success(request, "Tasdiqlash kodi terminalga chiqarildi. Kodni kiriting.")
                request.session['pw_reset_user_id'] = user.id
                return redirect('users:password_reset_confirm')
    else:
        form = PasswordResetRequestForm()
    return render(request, 'users/password_reset_request.html', {'form': form})


def password_reset_confirm(request):
    user_id = request.session.get('pw_reset_user_id')
    if not user_id:
        messages.error(request, "Avval email/username yuboring.")
        return redirect('users:password_reset_request')

    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = CodeConfirmForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code'].strip()
            try:
                vc = VerificationCode.objects.filter(user=user, purpose='pw_reset', used=False).order_by('-created_at').first()
                if not vc:
                    messages.error(request, "Kod topilmadi yoki allaqachon ishlatilgan.")
                elif vc.is_expired():
                    messages.error(request, "Kod muddati tugagan. Yangi kod yuboring.")
                elif vc.code != code:
                    messages.error(request, "Kod noto‘g‘ri.")
                else:
                    vc.used = True
                    vc.save()
                    request.session['pw_reset_verified_user_id'] = user.id
                    return redirect('users:password_reset_complete')
            except VerificationCode.DoesNotExist:
                messages.error(request, "Kod topilmadi.")
    else:
        form = CodeConfirmForm()
    return render(request, 'users/password_reset_confirm.html', {'form': form, 'user': user})


def password_reset_complete(request):
    user_id = request.session.get('pw_reset_verified_user_id')
    if not user_id:
        messages.error(request, "Avval kodni tasdiqlang.")
        return redirect('users:password_reset_request')
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = PasswordSetForm(user, request.POST)
        if form.is_valid():
            form.save()  
            request.session.pop('pw_reset_user_id', None)
            request.session.pop('pw_reset_verified_user_id', None)
            messages.success(request, "Parolingiz muvaffaqiyatli o‘zgartirildi. Iltimos kirish qiling.")
            return redirect('users:profile')
    else:
        form = PasswordSetForm(user)
    return render(request, 'users/password_reset_complete.html', {'form': form})