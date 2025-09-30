from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.utils.crypto import get_random_string
from django.views import View
from django.views.generic import CreateView, UpdateView, FormView
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from .models import VerificationCode
from .forms import (
    UserRegisterForm, ProfileUpdateForm,
    PasswordResetRequestForm, CodeConfirmForm, PasswordSetForm
)
from users.models import Profile


class RegisterView(CreateView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "Ro'yxatdan o'tish muvaffaqiyatli")
        return redirect('ads:list')

    def form_invalid(self, form):
        messages.error(self.request, "Xatolik: forma noto‘g‘ri to‘ldirildi ❌")
        return self.render_to_response(self.get_context_data(form=form))


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    template_name = 'users/profile.html'

    def get(self, request):
        pform = ProfileUpdateForm(instance=request.user.profile)
        return render(request, self.template_name, {'pform': pform})

    def post(self, request):
        pform = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if pform.is_valid():
            pform.save()
            messages.success(request, "Profil yangilandi ✅")
            return redirect('users:profile')
        return render(request, self.template_name, {'pform': pform})


class LoginView(View):
    template_name = 'users/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Kirish muvaffaqiyatli ✅")
            return redirect('ads:list')
        else:
            messages.error(request, "Login yoki parol xato ❌")
        return render(request, self.template_name)


def find_user_by_identifier(identifier):
    try:
        return User.objects.get(email__iexact=identifier)
    except User.DoesNotExist:
        pass
    try:
        return User.objects.get(username__iexact=identifier)
    except User.DoesNotExist:
        pass
    try:
        profile = Profile.objects.get(phone__iexact=identifier)
        return profile.user
    except Profile.DoesNotExist:
        pass
    return None


class PasswordResetRequestView(View):
    template_name = 'users/password_reset_request.html'

    def get(self, request):
        form = PasswordResetRequestForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            ident = form.cleaned_data['identifier'].strip()
            user = self.find_user_by_identifier(ident)
            if not user:
                messages.error(request, "❌ Foydalanuvchi topilmadi.")
            else:
                code = get_random_string(length=6, allowed_chars='0123456789')
                VerificationCode.objects.create(user=user, code=code, purpose='pw_reset')
                print(f"[PASSWORD RESET CODE] user={user.username} code={code}")  
                request.session['pw_reset_user_id'] = user.id
                messages.success(request, "✅ Tasdiqlash kodi terminalga chiqarildi. Kodni kiriting.")
                return redirect('users:password_reset_confirm')
        return render(request, self.template_name, {'form': form})

    def find_user_by_identifier(self, identifier):
        try:
            return User.objects.get(email__iexact=identifier)
        except User.DoesNotExist:
            pass
        try:
            return User.objects.get(username__iexact=identifier)
        except User.DoesNotExist:
            pass
        try:
            profile = Profile.objects.get(phone__iexact=identifier)
            return profile.user
        except Profile.DoesNotExist:
            return None


class PasswordResetConfirmView(View):
    template_name = 'users/password_reset_confirm.html'

    def get(self, request):
        form = CodeConfirmForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        user_id = request.session.get('pw_reset_user_id')
        if not user_id:
            messages.error(request, "Avval email yoki telefon raqam yuboring.")
            return redirect('users:password_reset_request')

        user = get_object_or_404(User, id=user_id)
        form = CodeConfirmForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code'].strip()
            vc = VerificationCode.objects.filter(user=user, purpose='pw_reset', used=False).order_by('-created_at').first()
            if not vc:
                messages.error(request, "❌ Kod topilmadi yoki ishlatilgan.")
            elif vc.is_expired():
                messages.error(request, "⌛ Kod muddati tugagan. Yangi kod oling.")
            elif vc.code != code:
                messages.error(request, "❌ Kod noto‘g‘ri.")
            else:
                vc.used = True
                vc.save()
                request.session['pw_reset_verified_user_id'] = user.id
                return redirect('users:password_reset_complete')
        return render(request, self.template_name, {'form': form})


class PasswordResetCompleteView(View):
    template_name = 'users/password_reset_complete.html'

    def get(self, request):
        user_id = request.session.get('pw_reset_verified_user_id')
        if not user_id:
            messages.error(request, "Avval kodni tasdiqlang.")
            return redirect('users:password_reset_request')

        user = get_object_or_404(User, id=user_id)
        form = PasswordSetForm(user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        user_id = request.session.get('pw_reset_verified_user_id')
        if not user_id:
            messages.error(request, "Avval kodni tasdiqlang.")
            return redirect('users:password_reset_request')

        user = get_object_or_404(User, id=user_id)
        form = PasswordSetForm(user, request.POST)
        if form.is_valid():
            form.save()
            request.session.pop('pw_reset_user_id', None)
            request.session.pop('pw_reset_verified_user_id', None)
            messages.success(request, "✅ Parol muvaffaqiyatli o‘zgartirildi!")
            return redirect('users:profile')
        return render(request, self.template_name, {'form': form})
    
    
class UserLogoutView(LogoutView):
    next_page = reverse_lazy('ads:list')