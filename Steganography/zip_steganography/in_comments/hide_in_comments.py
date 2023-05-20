import zipfile

from zip_steganography.constans import ENC


def split_msg(msg, n):
    len_msg = len(msg)
    part_len = max(len_msg // n, 1)
    parts = [msg[i*part_len:i*part_len+part_len] for i in range(n-1)]
    parts.append(msg[(n-1)*part_len:])
    return parts


def hide_msg(file_name, msg: str):
    msg = bytes(msg, encoding=ENC)
    with zipfile.ZipFile(file_name, 'a') as zip_file:
        n_places = len(zip_file.namelist()) + 1
        msg_parts = split_msg(msg, n_places)
        for file_path, comment in zip(zip_file.namelist(), msg_parts):
            zip_file.getinfo(file_path).comment = comment

        zip_file.comment = msg_parts[-1]


if __name__ == "__main__":
    message = input("Wprowadź wiadomość do zakodowania (bez polskich znaków)>> ")
    file_path = input("Wprować nazwę lub ścieżkę do pliku .zip >> ")
    hide_msg(file_path, message)