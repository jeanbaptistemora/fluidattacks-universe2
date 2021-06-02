import re


def escape(text: str) -> str:
    """Escape characters from an string object.
    Which are known to make a Redshift statement fail.
    """
    str_obj = str(text)
    str_obj = re.sub("\x00", "", str_obj)
    str_obj = str_obj.replace("\\", "\\\\")
    str_obj = str_obj.replace('"', '""')
    str_obj = str_obj.replace("'", "\\'")

    return str_obj
