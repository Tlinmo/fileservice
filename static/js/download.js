document.addEventListener('DOMContentLoaded', function() {
    const dropZone = document.getElementById('dropZone');
    const currentUser = localStorage.getItem('currentUser');

    if (!currentUser) {
        alert('Вы не авторизованы');
        window.location.href = '/';
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
        let pendingFiles = Array.from(files);

        function processFile(file) {
            if (user.maxFileCount && userFiles.length >= user.maxFileCount) {
                errorMessages.push(`Превышено максимальное количество файлов (${user.maxFileCount})`);
                checkCompletion();
                return;
            }

            if (user.maxFileSize && file.size / 1024 / 1024 > user.maxFileSize) {
                errorMessages.push(`Файл ${file.name} превышает максимальный размер (${user.maxFileSize} МБ)`);
                checkCompletion();
                return;
            }

            const fileExtension = file.name.split('.').pop().toLowerCase();
            if (user.allowedExtensions && !user.allowedExtensions.includes(fileExtension)) {
                errorMessages.push(`Файл ${file.name} имеет недопустимое расширение (${fileExtension})`);
                checkCompletion();
                return;
            }

            const existingFileIndex = userFiles.findIndex(existingFile => existingFile.name === file.name);
            if (existingFileIndex !== -1) {
                showReplaceModal(file, existingFileIndex);
            } else {
                saveFile(file, userFiles);
            }
        }

        function saveFile(file, userFiles, index = null) {
            const reader = new FileReader();
            reader.onload = function(event) {
                const fileContent = event.target.result;
                if (index !== null) {
                    userFiles[index] = { name: file.name, content: fileContent };
                } else {
                    userFiles.push({ name: file.name, content: fileContent });
                }
                localStorage.setItem(currentUser + '_files', JSON.stringify(userFiles));
                successMessages.push(`Файл ${file.name} успешно загружен`);
                checkCompletion();
            };
            reader.readAsDataURL(file);
        }

        function checkCompletion() {
            pendingFiles.shift();
            if (pendingFiles.length > 0) {
                processFile(pendingFiles[0]);
            } else {
                displayMessages(successMessages, errorMessages);
            }
        }

        function showReplaceModal(file, index) {
            const replaceModal = document.getElementById('replaceModal');
            const replaceMessage = document.getElementById('replaceMessage');
            const confirmReplace = document.getElementById('confirmReplace');
            const cancelReplace = document.getElementById('cancelReplace');

            replaceMessage.textContent = `Файл с именем ${file.name} уже существует. Хотите заменить его?`;
            replaceModal.style.display = 'block';

            confirmReplace.onclick = function() {
                replaceModal.style.display = 'none';
                saveFile(file, userFiles, index);
            };

            cancelReplace.onclick = function() {
                replaceModal.style.display = 'none';
                errorMessages.push(`Файл ${file.name} уже существует и не был загружен`);
                checkCompletion();
            };
        }

        processFile(pendingFiles[0]);
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