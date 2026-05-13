from cryptography.fernet import Fernet
import argparse
import os


# creates and saves a new encryption key
def generateKey():

    key = Fernet.generate_key()

    with open("secret.key", "wb") as keyFile:
        keyFile.write(key)

    print("Key generated successfully.")
    print("Saved as secret.key")


# loads the existing key from file
def loadKey():
    return open("secret.key", "rb").read()


# encrypts a file using the saved key
def encryptFile(fileName):

    # check if the file exists first
    if not os.path.exists(fileName):
        print("File does not exist.")
        return

    key = loadKey()
    fernet = Fernet(key)

    # read original file data
    with open(fileName, "rb") as file:
        originalData = file.read()

    # encrypt the file contents
    encryptedData = fernet.encrypt(originalData)

    encryptedFileName = fileName + ".enc"

    # save encrypted output
    with open(encryptedFileName, "wb") as encryptedFile:
        encryptedFile.write(encryptedData)

    print("File encrypted successfully.")
    print(f"Saved as: {encryptedFileName}")


# decrypts an encrypted file
def decryptFile(fileName):

    if not os.path.exists(fileName):
        print("File does not exist.")
        return

    key = loadKey()
    fernet = Fernet(key)

    # read encrypted data
    with open(fileName, "rb") as encryptedFile:
        encryptedData = encryptedFile.read()

    # try decrypting the file
    try:
        decryptedData = fernet.decrypt(encryptedData)

    except:
        print("Decryption failed.")
        return

    # remove .enc extension after decryption
    if fileName.endswith(".enc"):
        outputFile = fileName[:-4]
    else:
        outputFile = "decrypted_" + fileName

    # write decrypted contents back to a file
    with open(outputFile, "wb") as decryptedFile:
        decryptedFile.write(decryptedData)

    print("File decrypted successfully.")
    print(f"Saved as: {outputFile}")


def main():

    parser = argparse.ArgumentParser(
        description="Simple File Encryption Tool"
    )

    # choose what mode to run
    parser.add_argument(
        "mode",
        choices=["generate", "encrypt", "decrypt"],
        help="Mode to run"
    )

    # optional file argument
    parser.add_argument(
        "file",
        nargs="?",
        help="File to encrypt or decrypt"
    )

    args = parser.parse_args()

    # generate encryption key
    if args.mode == "generate":
        generateKey()

    # encrypt file
    elif args.mode == "encrypt":

        if not args.file:
            print("Please provide a file to encrypt.")
            return

        encryptFile(args.file)

    # decrypt file
    elif args.mode == "decrypt":

        if not args.file:
            print("Please provide a file to decrypt.")
            return

        decryptFile(args.file)


if __name__ == "__main__":
    main()