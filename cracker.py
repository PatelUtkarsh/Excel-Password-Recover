import time
from random import randint
import msoffcrypto
import io
import pandas as pd
import itertools
import string

class Cracker:
    __passwords: list[str] = []
    __filename: str = ""
    __verbose: bool = True

    def __init__(self, filename, verbose):
        self.__filename = filename
        self.__verbose = verbose
        characters = string.ascii_letters + string.digits + '@#.'
        # characters = string.digits
        # Generate and process each combination one by one
        for le in range(1, 13):
            for combination in itertools.product(characters, repeat=le):
                password_guess = ''.join(combination)
                if self.__verbose:
                    print(f"Trying {password_guess}...")
                guess = self.decrypt(str(password_guess))
                if (guess):
                    self.success(password_guess)
                    return
        self.end()

    def decrypt(self, password) -> bool:
        try:
            decrypted = io.BytesIO()
            with open(self.__filename, "rb") as f:
                file = msoffcrypto.OfficeFile(f)
                file.load_key(password=password)
                file.decrypt(decrypted)
            return True
        except:
            return False

    def read_decrypted_file(self, correct_password) -> None:
        """Prints locked file information in the terminal."""
        decrypted = io.BytesIO()
        with open(self.__filename, "rb") as f:
            file = msoffcrypto.OfficeFile(f)
            file.load_key(password=correct_password)
            file.decrypt(decrypted)
        df = pd.read_excel(decrypted)
        print(df)

    def end(self) -> None:
        print(f"No password found :(")

    def success(self, password) -> None:
        print(f"CRACKED: {password}")
        self.read_decrypted_file(password)
        print("Good luck on your interview!")


# if __name__ == "__main__":
#     newCracker = Cracker()

