from zipfile import ZipFile

from zip_steganography.constans import ENC


class MyZipFileUnHide(ZipFile):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        with self._lock:
            self.fp.seek(self.start_dir-10)
            msg_len_info = self.fp.read(10)
            msg_len_info = msg_len_info.decode(ENC)
            msg_len = int(msg_len_info)
            self.fp.seek(self.start_dir-10-msg_len)
            b_msg = self.fp.read(msg_len)
            msg = b_msg.decode(ENC)
            self.msg = msg


def unhide_msg(filename):
    with MyZipFileUnHide(filename, 'r') as file:
        msg = file.msg
    return msg


if __name__ == "__main__":
    file_path = input("Wprować nazwę lub ścieżkę do pliku .zip >> ")
    print("Odczytana wiadomość:", unhide_msg(file_path))