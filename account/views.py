from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile
from django.contrib import messages


def user_login(request):
    # Проверка метода запроса:
    # Проверяет, является ли метод запроса POST. Это значит, что пользователь отправил данные формы для аутентификации.
    if request.method == 'POST':
        # Создание формы и проверка ее валидности:
        # Создает экземпляр формы LoginForm с данными, отправленными в запросе,
        # и проверяет, действительна ли форма (проверяет, прошли ли данные валидацию).
        form = LoginForm(request.POST)
        if form.is_valid():
            # Аутентификация пользователя:
            # Получает очищенные данные из формы
            # и аутентифицирует пользователя с использованием предоставленных имени пользователя и пароля.
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            # Проверка успешности аутентификации:
            # Проверяет, успешно ли прошла аутентификация. Если пользователь найден, продолжаем дальше.
            if user is not None:
                # Проверка активности пользователя:
                # Если пользователь активен, он логинится в систему и возвращается сообщение об успешной аутентификации.
                # Если учетная запись отключена, возвращается соответствующее сообщение.
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            # Обработка неверного логина:
            # Если аутентификация не прошла, возвращается сообщение о недействительном логине.
            else:
                return HttpResponse('invalid login')
    # Обработка GET-запроса:
    # Если метод запроса не POST, создается пустая форма для отображения на странице.
    else:
        form = LoginForm()
    # Рендеринг шаблона:
    # Отображает страницу с формой логина.
    return render(request, 'account/login.html', {'form': form})

# Эта функция отвечает за отображение панели управления для аутентифицированных пользователей.
# Декоратор @login_required:
# Этот декоратор гарантирует, что доступ к этой странице имеют только аутентифицированные пользователи.
# Если пользователь не аутентифицирован, он будет перенаправлен на страницу логина.


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Создать новый объект пользователя,
            # но пока не сохранять его
            new_user = user_form.save(commit=False)
            # Установить выбранный пароль
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Сохранить объект User
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request, 'account/template/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/template/register.html',
                  {'user_form': user_form})


@login_required
def dashboard(request):
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard'})


def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated ', 'successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})
