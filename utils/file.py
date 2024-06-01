import shutil
import os
import gzip
import tempfile

from fastapi import UploadFile
from cryptography.fernet import Fernet

from microservice.settings import settings
from microservice.settings import UPLOAD_DIRECTORY


def _path_to_file(file_type: str, filename: str, user_id: int) -> str:
    _directory = f"{UPLOAD_DIRECTORY}/{user_id}/{file_type}/"

    if not os.path.exists(_directory):
        os.makedirs(_directory)

    return os.path.abspath(_directory + str(filename))


def delete(filename: str):
    os.remove(filename)


# Сжатие файла
def compress_file(filename: str):
    with open(filename, "rb") as f:
        data = f.read()
        with gzip.open(f"{filename}.gz", "wb") as f_out:
            f_out.write(data)
            os.remove(filename)
            return f"{filename}.gz"


# Чтение сжатого файла
def _read_compress_file(filename: str):
    with gzip.open(filename, "rb") as f:
        file_content = f.read()
        return file_content


# Шифрование файла
def encrypt_file(filename: str):
    cipher = Fernet(settings.encrypt_key)
    with open(filename, "rb") as f:
        data = f.read()
        encrypted_data = cipher.encrypt(data)
        with open(f"{filename}.encrypted", "wb") as f_out:
            f_out.write(encrypted_data)
            os.remove(filename)
            return f"{filename}.encrypted"

# Чтение зашифрованного файла
def _read_encrypt_file(filename: str):
    cipher = Fernet(settings.encrypt_key)

    with open(f"{filename}", "rb") as f:
        encrypted_data = f.read()
        decrypted_data = cipher.decrypt(encrypted_data)

    return decrypted_data


#  Чтение зашифрованного сжатого файла
def _read_encrypt_compress_file(filename: str):
    cipher = Fernet(settings.encrypt_key)

    with open(filename, "rb") as f:
        encrypted_data = f.read()
        decrypted_data = cipher.decrypt(encrypted_data)

    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(decrypted_data)
        temp_file_path = temp_file.name

    with gzip.open(temp_file_path, "rb") as f:
        data = f.read()
        return data


def _read_file(filename: str):
    with open(filename, 'rb') as f:
        data = f.read()
        return data

# Юзаем это для того что бы читать файлы и радуемся
def reader(filename: str):
    file_type = filename.split(".")
    file_type = 'gz.encrypted' if file_type[-2:] == ['gz', 'encrypted'] else file_type[-1]
    
    match file_type:
        case "gz":
            return _read_compress_file(filename)
        case "encrypted":
            return _read_encrypt_file(filename)
        case "gz.encrypted":
            return _read_encrypt_compress_file(filename)
        case _:
            return _read_file(filename)

# Сохранение файла
def save(
    file: UploadFile,
    user_id: int,
    size_limit: int,
    zipped: bool = True,
    encrypted: bool = False,
    quality: int = 100,
):
    file_type = file.filename.split(".")[-1]

    directory = _path_to_file(file_type, file.filename, user_id)

    with open(directory, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    file_size = os.path.getsize(directory) / 1000 / 1000
    if file_size > size_limit and size_limit != -1:
        return -1
    
    if zipped:
        filename = compress_file(directory)
    if encrypted:
        filename = encrypt_file(filename)
        

    return {
        "file_size": file_size,
        "path": filename,
    }
