import zipfile

from zip_steganography.constans import ENC


def unhide_msg(file_name):
    with zipfile.ZipFile(file_name, 'a') as zip_file:
        msg = b''
        for file_path in zip_file.namelist():
            msg += zip_file.getinfo(file_path).comment
        msg += zip_file.comment
    msg = msg.decode(ENC)
    return msg


if __name__ == "__main__":
    msg = unhide_msg("../../files/kotki.zip")
    print(msg)