from random import randint
from time import time
import base64


class ConfirmTool:

    __letters = [
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a',
        'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
        'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w',
        'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
        'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
        'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    @staticmethod
    def generateConfirmToken():
        ts = str(time()*10000).replace(".", "")
        ts = str(randint(10000, 99999)) + ts
        data = "".join(
            [ConfirmTool.__letters[int(ts[i])] for i in range(len(ts))])
        urlSafeEncodedBytes = base64.urlsafe_b64encode(data.encode("utf-8"))
        urlSafeEncodedStr = str(
            urlSafeEncodedBytes, "utf-8").replace("=", "").replace("-","")
        return urlSafeEncodedStr


if __name__ == "__main__":
    print(ConfirmTool.generateConfirmToken())
