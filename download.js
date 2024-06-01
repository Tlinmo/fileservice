document.addEventListener('DOMContentLoaded', function() {
    const dropZone = document.getElementById('dropZone');
    const currentUser = localStorage.getItem('currentUser');

    if (!currentUser) {
        alert('Вы не авторизованы');
        window.location.href = 'index.html';
    }

    dropZone.addEventListener('dragover', function(event) {
        event.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', function(event) {
        event.preventDefault();
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', function(event) {
        event.preventDefault();
        dropZone.classList.remove('dragover');

        const files = event.dataTransfer.files;
        handleFiles(files);
    });

    function handleFiles(files) {
        const user = JSON.parse(localStorage.getItem(currentUser));
        const userFiles = JSON.parse(localStorage.getItem(currentUser + '_files')) || [];
        
        const errorMessages = [];
        const successMessages = [];

        if (user.maxFileCount && userFiles.length + files.length > user.maxFileCount) {
            errorMessages.push(`Превышено максимальное количество файлов (${user.maxFileCount})`);
        } else {
            Array.from(files).forEach(file => {
                if (user.maxFileSize && file.size / 1024 / 1024 > user.maxFileSize) {
                    errorMessages.push(`Файл ${file.name} превышает максимальный размер (${user.maxFileSize} МБ)`);
                    return;
                }

                const fileExtension = file.name.split('.').pop().toLowerCase();
                if (user.allowedExtensions && !user.allowedExtensions.includes(fileExtension)) {
                    errorMessages.push(`Файл ${file.name} имеет недопустимое расширение (${fileExtension})`);
                    return;
                }

                const reader = new FileReader();
                reader.onload = function(event) {
                    const fileContent = event.target.result;
                    userFiles.push({ name: file.name, content: fileContent });
                    localStorage.setItem(currentUser + '_files', JSON.stringify(userFiles));
                    successMessages.push(`Файл ${file.name} успешно загружен`);
                    if (successMessages.length + errorMessages.length === files.length) {
                        displayMessages(successMessages, errorMessages);
                    }
                };
                reader.readAsDataURL(file);
            });
        }

        if (successMessages.length + errorMessages.length === files.length) {
            displayMessages(successMessages, errorMessages);
        }
    }

    function displayMessages(successMessages, errorMessages) {
        const messages = [];

        if (errorMessages.length > 0) {
            messages.push('Ошибки загрузки:\n' + errorMessages.join('\n'));
        }

        if (successMessages.length > 0) {
            messages.push('Успешно загружены:\n' + successMessages.join('\n'));
        }

        if (messages.length > 0) {
            alert(messages.join('\n\n'));
        }
    }
});