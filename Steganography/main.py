from pathlib import Path
import zip_steganography as zs

DATA_PATH = Path(__file__).parent.joinpath("files")

ZIP_PATH = DATA_PATH.joinpath("kotki.zip")
MSG = "Ala ma wiadomosci i klucze"
EXE_PATH = DATA_PATH.joinpath("helloworld.exe")

zs.hide_msg(ZIP_PATH, MSG, zs.Constans.COMM)
msg = zs.show_msg(ZIP_PATH, zs.Constans.COMM)
print(msg)

zs.hide_exe_in_zip(EXE_PATH, ZIP_PATH, zs.Constans.END)
zs.run_exe_from_zip(ZIP_PATH, zs.Constans.END)


