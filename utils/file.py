import shutil
import os
import gzip
import tempfile

from fastapi import UploadFile
from cryptography.fernet import Fernet

from microservice.settings import settings
from microservice.settings import UPLOAD_DIRECTORY


def get_folder_size() -> float:
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(UPLOAD_DIRECTORY):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size / (1024**3)


def _path_to_file(file_type: str, filename, user_id: int) -> str:
    _directory = f"{UPLOAD_DIRECTORY}/{user_id}/{file_type}/"

    if not os.path.exists(_directory):
        os.makedirs(_directory)

    return os.path.abspath(_directory + str(filename))


# Сжатие файла
def compress_file(filename: str):
    with open(filename, "rb") as f:
        data = f.read()
        with gzip.open(f"{filename}.gz", "wb") as f_out:
            f_out.write(data)
            os.remove(filename)


# Чтение сжатого файла
def read_compress_file(filename):
    with gzip.open(filename, "rb") as f:
        file_content = f.read()
        return file_content

# Шифрование файла
def encrypt_file(filename):
    cipher = Fernet(settings.encrypt_key)
    with open(f"{filename}", "rb") as f:
        data = f.read()
        encrypted_data = cipher.encrypt(data)
        with open(f"{filename}.encrypted", "wb") as f_out:
            f_out.write(encrypted_data)
            os.remove(filename)
            

# Чтение зашифрованного файла
def read_encrypt_file(filename):
    cipher = Fernet(settings.encrypt_key)

    with open(f'{filename}', "rb") as f:
        encrypted_data = f.read()
        decrypted_data = cipher.decrypt(encrypted_data)
    
    return decrypted_data


def read_encrypt_compress_file(filename):
    cipher = Fernet(settings.encrypt_key)

    with open(filename, 'rb') as f:
        encrypted_data = f.read()
        decrypted_data = cipher.decrypt(encrypted_data)

    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(decrypted_data)
        temp_file_path = temp_file.name

    with gzip.open(temp_file_path, 'rb') as f:
        data = f.read()
        return data

# Сохранение файла
def save(file: UploadFile, filename: str, user_id: int, zipped: bool = True, encrypted: bool = False):

    file_type = file.headers.get("content-type")
    if file_type:
        file_type = file_type.split("/")[0]
    else:
        file_type = "more"

    directory = _path_to_file(file_type, filename, user_id)

    with open(directory, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        if zipped:
            compress_file(directory)
            directory = _path_to_file(file_type, f'{filename}.gz', user_id)
        if encrypted:
            encrypt_file(directory)
            directory = _path_to_file(file_type, f'{filename}.encrypted', user_id)

compress_file('test.txt')