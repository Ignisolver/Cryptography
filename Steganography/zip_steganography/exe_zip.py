import base64
import subprocess
import tempfile

from zip_steganography.constans import ENC
from zip_steganography.hide_functions import hide_msg, show_msg


def hide_exe_in_zip(exe_name, zip_name, method):
    bin_exe = _read_exe(exe_name)
    str_exe_base64 = base64.b64encode(bin_exe)
    str_exe_ibm039 = str_exe_base64.decode(ENC)
    hide_msg(zip_name, str_exe_ibm039, method)


def _decode_base64_string(s):
    padding = len(s) % 4
    if padding != 0:
        s += '=' * (4 - padding)
    decoded_data = base64.b64decode(s)

    return decoded_data


def run_exe_from_zip(zip_name, method):
    exe_bytes = _load_exe_from_zip(zip_name, method)
    with tempfile.NamedTemporaryFile(suffix='.exe', delete=False) as temp_file:
        temp_file.write(exe_bytes)
    subprocess.run(temp_file.name, shell=False)
    temp_file.close()


def _load_exe_from_zip(zip_name, method):
    str_exe = show_msg(zip_name, method)
    bytes_exe = str_exe.encode(ENC)
    bin_exe = _decode_base64_string(bytes_exe)
    return bin_exe


def _read_exe(name):
    with open(name, 'rb') as file:
        all_ = file.readlines()
        return b''.join(all_)


if __name__ == "__main__":
    hide_exe_in_zip("helloworld.exe", "kotki.zip", "COMMENT")
    run_exe_from_zip("kotki.zip", "COMMENT")
