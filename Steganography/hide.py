from zipfile import ZipFile


class MyZipFileHide(ZipFile):
    def __init__(self, message_to_hide, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._message = message_to_hide

    def close(self):
        """Close the file, and for mode 'w', 'x' and 'a' write the ending
        records."""
        if self.fp is None:
            return

        if self._writing:
            raise ValueError("Can't close the ZIP file while there is "
                             "an open writing handle on it. "
                             "Close the writing handle before closing the zip.")

        try:
            with self._lock:
                self.fp.seek(self.start_dir)
                if self._message[0] == "/":
                    raise RuntimeError('"\\" is illegal at the beggining of message')
                self.fp.write(bytes("X", encoding='utf-8'))
                self.fp.write(self._message)
                shift = len(self._message)
                self.fp.seek(self.start_dir+shift)
                self.start_dir += shift + 1
                self.fp.seek(self.start_dir)
                self._write_end_record()
        finally:
            fp = self.fp
            self.fp = None
            self._fpclose(fp)


def hide_txt(msg, filename):
    msg = bytes(msg, encoding='utf-8')
    with MyZipFileHide(msg, filename, 'a') as _:
        pass


if __name__ == "__main__":
    message = input("Wprowadź wiadomość do zakodowania (bez polskich znaków)>> ")
    file_path = input("Wprować nazwę lub ścieżkę do pliku .zip >> ")
    hide_txt(message, file_path)
    print("Wiadomość ukryta")





