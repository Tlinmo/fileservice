document.getElementById('registerButton').addEventListener('click', function () {
    const registerName = document.getElementById('registerName').value;
    const registerPassword = document.getElementById('registerPassword').value;
    const registerRole = document.getElementById('registerRole').value;
    const registerError = document.getElementById('registerError');

    if (!registerName || !registerPassword) {
        registerError.textContent = 'Введите логин и пароль';
        return;
    }

    if (registerPassword.length < 4 || registerPassword.length > 10) {
        registerError.textContent = 'Пароль должен содержать от 4 до 10 символов';
        return;
    }

    const user = {
        username: registerName,
        password: registerPassword,
        role: registerRole
    };

    // Проверка, существует ли пользователь
    if (localStorage.getItem(registerName)) {
        registerError.textContent = 'Пользователь с таким именем уже существует';
    } else {
        localStorage.setItem(registerName, JSON.stringify(user));
        alert('Регистрация прошла успешно');
        window.location.href = '/';
    }
});