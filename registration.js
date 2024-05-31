document.getElementById('registerButton').addEventListener('click', function () {
    const registerName = document.getElementById('registerName').value;
    const registerPassword = document.getElementById('registerPassword').value;

    if (registerName && registerPassword) {
        const user = {
            username: registerName,
            password: registerPassword
        };

        // Проверка, существует ли пользователь
        if (localStorage.getItem(registerName)) {
            alert('Пользователь с таким именем уже существует');
        } else {
            localStorage.setItem(registerName, JSON.stringify(user));
            alert('Регистрация прошла успешно');
            window.location.href = 'index.html';
        }
    } else {
        alert('Введите логин и пароль');
    }
});