document.getElementById('loginButton').addEventListener('click', function () {
    const loginName = document.getElementById('name').value;
    const loginPassword = document.getElementById('password').value;

    const storedUser = localStorage.getItem(loginName);

    if (storedUser) {
        const user = JSON.parse(storedUser);
        if (user.password === loginPassword) {
            alert('Вы успешно вошли в систему');
            // Сохраняем информацию о текущем пользователе
            localStorage.setItem('currentUser', loginName);
            // Перенаправление на страницу личного кабинета
            window.location.href = 'lk.html';
        } else {
            alert('Неверный пароль');
        }
    } else {
        alert('Пользователь не найден');
    }
});