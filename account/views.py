from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm


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


@login_required
def dashboard(request):
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard'})
