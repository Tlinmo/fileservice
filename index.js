document.getElementById('loginButton').addEventListener('click', function(event) {
    event.preventDefault();
    
    const loginName = document.getElementById('name').value;
    const loginPassword = document.getElementById('password').value;
    const loginError = document.getElementById('loginError');

    if (!loginName || !loginPassword) {
        loginError.textContent = 'Введите логин и пароль';
        return;
    }

    const storedUser = localStorage.getItem(loginName);

    if (storedUser) {
        const user = JSON.parse(storedUser);
        if (user.password === loginPassword) {
            alert('Вы успешно вошли в систему');
            // Сохраняем информацию о текущем пользователе
            localStorage.setItem('currentUser', loginName);
            localStorage.setItem('currentUserRole', user.role);
            // Перенаправление на страницу загрузки файлов или админ панели
            if (user.role === 'admin') {
                window.location.href = 'admin.html';
            } else {
                window.location.href = 'download.html';
            }
        } else {
            loginError.textContent = 'Неверный пароль';
        }
    } else {
        loginError.textContent = 'Пользователь не найден';
    }
});
