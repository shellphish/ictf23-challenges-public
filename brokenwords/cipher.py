import base64
import argparse


def custom_cipher(plaintext):
    # Apply ROT16 to the plaintext
    rot16_text = ''.join([chr((ord(char) - 65 + 16) % 26 + 65) if char.isalpha() and char.isupper() else
                          chr((ord(char) - 97 + 16) % 26 + 97) if char.isalpha() and char.islower() else char
                          for char in plaintext])

    # Encode the ROT16 string using base64
    base64_text = base64.b64encode(rot16_text.encode()).decode()

    # Substitute vowels
    substitution_mapping = {'a': '🤣', 'e': '🤪', 'i': '🥶', 'o': '🤑', 'u': '😈'}
    substituted_text = ''.join([substitution_mapping[char] if char in substitution_mapping else char
                                for char in base64_text])

    return substituted_text

def custom_cipher_decrypt(ciphertext):
    substitution_mapping = {'a': '🤣', 'e': '🤪', 'i': '🥶', 'o': '🤑', 'u': '😈'}
    # Reverse vowel substitution
    reverse_substitution_mapping = {vowel: char for char, vowel in substitution_mapping.items()}
    reverse_substituted_text = ''.join([reverse_substitution_mapping[char] if char in reverse_substitution_mapping else char
                                        for char in ciphertext])

    # Decode base64
    base64_text = base64.b64decode(reverse_substituted_text.encode()).decode()

    # Reverse ROT16
    reverse_rot16_text = ''.join([chr((ord(char) - 65 - 16) % 26 + 65) if char.isalpha() and char.isupper() else
                                  chr((ord(char) - 97 - 16) % 26 + 97) if char.isalpha() and char.islower() else char
                                  for char in base64_text])

    return reverse_rot16_text


# entry point of python
if __name__ == "__main__":
    # create parser object
    parser = argparse.ArgumentParser(description="Custom cipher")

    # defining arguments for parser object
    parser.add_argument("-e", "--encrypt", type=str, help="encrypt text")
    parser.add_argument("-d", "--decrypt", type=str, help="decrypt text")

    # parse the arguments from standard input
    args = parser.parse_args()

    # check for --version or -V
    if args.encrypt:
        print(custom_cipher(args.encrypt))
    elif args.decrypt:
        print(custom_cipher_decrypt(args.decrypt))
    else:
        print("Please specify cipher or decrypt text")


