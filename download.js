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
        const fileArray = Array.from(files);
        fileArray.forEach(file => {
            const reader = new FileReader();
            reader.onload = function(event) {
                const fileContent = event.target.result;
                saveFile(currentUser, file.name, fileContent);
            };
            reader.readAsDataURL(file);
        });
    }

    function saveFile(user, fileName, fileContent) {
        let userFiles = JSON.parse(localStorage.getItem(user + '_files')) || [];
        userFiles.push({ name: fileName, content: fileContent });
        localStorage.setItem(user + '_files', JSON.stringify(userFiles));
        alert('Файл успешно загружен');
    }
});