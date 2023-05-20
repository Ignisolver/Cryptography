from zip_steganography.before_end_record.hide import hide_msg as h_in_end
from zip_steganography.before_end_record.unhide import unhide_msg as uh_in_end
from zip_steganography.in_comments.hide_in_comments import hide_msg as h_in_com
from zip_steganography.in_comments.unhide_from_comments import unhide_msg as uh_in_com
from zip_steganography.constans import Constans


def hide_msg(file_name, message, method):
    match method:
        case Constans.END:
            h_in_end(message, file_name)
        case Constans.COMM:
            h_in_com(file_name, message)


def show_msg(file_name, method):
    match method:
        case Constans.END:
            msg = uh_in_end(file_name)
        case Constans.COMM:
            msg = uh_in_com(file_name)
    return msg

