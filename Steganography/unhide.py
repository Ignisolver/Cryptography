from zipfile import ZipFile


class MyZipFileUnHide(ZipFile):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.msg = ""
        with self._lock:
            self.fp.seek(self.start_dir)
            message = b''
            end_byte = b'X'
            last = b''
            while True:
                pos = self.fp.tell()
                letter = self.fp.read(1)
                self.fp.seek(pos-1)
                if letter != end_byte:
                    message += letter
                    last = letter
                else:
                    if last == b"/":
                        message += letter
                        continue
                    else:
                        break
            self.msg = message.decode('utf-8')[:0:-1]


def unhide_msg(filename):
    with MyZipFileUnHide(filename, 'r') as file:
        msg = file.msg
    return msg


if __name__ == "__main__":
    file_path = input("Wprować nazwę lub ścieżkę do pliku .zip >> ")
    print("Odczytana wiadomość:", unhide_msg(file_path))