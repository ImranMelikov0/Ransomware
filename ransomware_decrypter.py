import os
from cryptography.fernet import Fernet, InvalidToken
import optparse


def get_input():
    parse_object = optparse.OptionParser()
    parse_object.add_option("-k", "--key", dest="secret_key", help="Enter Key!")
    (user_input, arguments) = parse_object.parse_args()
    if not user_input.secret_key:
        parse_object.error("You must provide the decryption key using -k or --key.")
    return user_input.secret_key


def list_files_to_process(exclude_files):
    files = []
    for file in os.listdir():
        if file in exclude_files:
            continue
        if os.path.isfile(file):
            files.append(file)
    return files


def decrypt_file(file, secret_key):
    try:
        with open(file, "rb") as the_file:
            contents = the_file.read()

        try:
            content_decrypted = Fernet(secret_key).decrypt(contents)
        except InvalidToken:
            print(f"[ERROR] The provided key for {file} is incorrect. Skipping this file.")
            return False

        with open(file, "wb") as the_file:
            the_file.write(content_decrypted)

        print(f"[SUCCESS] {file} decrypted successfully.")
        return True

    except Exception as e:
        print(f"[ERROR] An error occurred while decrypting {file}: {str(e)}")
        return False

def main():
    exclude_files = ["ransomware.py", "ransomware_decrypted.py","secret.key"]

    files = list_files_to_process(exclude_files)
    print(f"Files to process: {files}")

    secret_key = get_input()

    for file in files:
        decrypt_file(file, secret_key)

if __name__ == "__main__":
    main()
