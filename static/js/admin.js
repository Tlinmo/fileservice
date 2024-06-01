document.getElementById('searchUserButton').addEventListener('click', function () {
    const username = document.getElementById('username').value;
    const adminError = document.getElementById('adminError');
    const userFilesSection = document.getElementById('userFilesSection');
    const userFilesList = document.getElementById('userFilesList');
    const userSettingsSection = document.getElementById('userSettingsSection');
    const maxFileSize = document.getElementById('maxFileSize');
    const allowedExtensions = document.getElementById('allowedExtensions');
    const maxFileCount = document.getElementById('maxFileCount');

    if (!username) {
        adminError.textContent = 'Введите логин пользователя';
        return;
    }

    const storedUser = localStorage.getItem(username);

    if (storedUser) {
        const user = JSON.parse(storedUser);
        adminError.textContent = '';

        // Отображение списка файлов пользователя
        const userFiles = JSON.parse(localStorage.getItem(username + '_files')) || [];
        userFilesList.innerHTML = '';
        userFiles.forEach(file => {
            const li = document.createElement('li');
            li.textContent = file.name;
            userFilesList.appendChild(li);
        });

        // Отображение настроек пользователя
        maxFileSize.value = user.maxFileSize || '';
        allowedExtensions.value = user.allowedExtensions ? user.allowedExtensions.join(',') : '';
        maxFileCount.value = user.maxFileCount || '';

        userFilesSection.style.display = 'block';
        userSettingsSection.style.display = 'block';
    } else {
        adminError.textContent = 'Пользователь не найден';
        userFilesSection.style.display = 'none';
        userSettingsSection.style.display = 'none';
    }
});

document.getElementById('saveSettingsButton').addEventListener('click', function () {
    const username = document.getElementById('username').value;
    const maxFileSize = document.getElementById('maxFileSize').value;
    const allowedExtensions = document.getElementById('allowedExtensions').value.split(',').map(ext => ext.trim());
    const maxFileCount = document.getElementById('maxFileCount').value;

    const storedUser = localStorage.getItem(username);

    if (storedUser) {
        const user = JSON.parse(storedUser);
        user.maxFileSize = maxFileSize;
        user.allowedExtensions = allowedExtensions;
        user.maxFileCount = maxFileCount;
        localStorage.setItem(username, JSON.stringify(user));
        alert('Настройки пользователя успешно сохранены');
    } else {
        alert('Пользователь не найден');
    }
});