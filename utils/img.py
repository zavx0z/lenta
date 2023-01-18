import base64


def save_base64_string_png(path, base64_string):
    with open("imageToSave.png", "wb") as fh:
        fh.write(base64.urlsafe_b64decode(base64_string))
