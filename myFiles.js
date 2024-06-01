document.addEventListener('DOMContentLoaded', function() {
    const currentUser = localStorage.getItem('currentUser');

    if (!currentUser) {
        alert('Вы не авторизованы');
        window.location.href = 'index.html';
    }

    const fileList = document.getElementById('fileList');
    loadFiles(currentUser);

    function loadFiles(user) {
        const userFiles = JSON.parse(localStorage.getItem(user + '_files')) || [];
        fileList.innerHTML = '';
        userFiles.forEach((file, index) => {
            const li = document.createElement('li');
            li.textContent = file.name;
            li.dataset.index = index;
            li.addEventListener('click', toggleFileOptions);
            fileList.appendChild(li);
        });
    }

    function toggleFileOptions(event) {
        const li = event.currentTarget;
        const existingOptions = li.querySelector('.file-options');

        if (existingOptions) {
            existingOptions.remove();
        } else {
            showFileOptions(li, parseInt(li.dataset.index, 10));
        }
    }

    function showFileOptions(li, index) {
        const fileName = li.textContent;
        const options = document.createElement('div');
        options.classList.add('file-options');
        options.innerHTML = `
            <button onclick="downloadFile('${fileName}')">Скачать</button>
            <input type="file" id="replaceFileInput${index}" style="display:none" onchange="replaceFile(event, '${fileName}', ${index})">
            <button onclick="document.getElementById('replaceFileInput${index}').click()">Заменить</button>
            <button onclick="deleteFile(${index})">Удалить</button>
        `;
        li.appendChild(options);
    }

    window.downloadFile = function(fileName) {
        const userFiles = JSON.parse(localStorage.getItem(currentUser + '_files')) || [];
        const file = userFiles.find(file => file.name === fileName);
        if (file) {
            const a = document.createElement('a');
            a.href = file.content;
            a.download = file.name;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        } else {
            alert('Файл не найден');
        }
    };

    window.replaceFile = function(event, fileName, index) {
        const file = event.target.files[0];
        const reader = new FileReader();
        reader.onload = function(event) {
            const fileContent = event.target.result;
            let userFiles = JSON.parse(localStorage.getItem(currentUser + '_files')) || [];
            userFiles[index] = { name: fileName, content: fileContent };
            localStorage.setItem(currentUser + '_files', JSON.stringify(userFiles));
            alert('Файл успешно заменен');
            loadFiles(currentUser);
        };
        reader.readAsDataURL(file);
    };

    window.deleteFile = function(index) {
        let userFiles = JSON.parse(localStorage.getItem(currentUser + '_files')) || [];
        userFiles.splice(index, 1);
        localStorage.setItem(currentUser + '_files', JSON.stringify(userFiles));
        alert('Файл успешно удален');
        loadFiles(currentUser);
    };
});