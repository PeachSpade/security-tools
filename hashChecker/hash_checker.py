import hashlib
import argparse
import os


# generate SHA256 hash for a file
def generateFileHash(fileName):

    sha256Hash = hashlib.sha256()

    try:

        with open(fileName, "rb") as file:

            # read file in chunks
            while True:

                fileChunk = file.read(4096)

                if not fileChunk:
                    break

                sha256Hash.update(fileChunk)

        return sha256Hash.hexdigest()

    except:
        return None


# compare two file hashes
def compareFiles(firstFile, secondFile):

    firstHash = generateFileHash(firstFile)
    secondHash = generateFileHash(secondFile)

    if firstHash is None or secondHash is None:
        print("Error reading one or more files.")
        return

    print("\n=================================================================")
    print("FILE HASH COMPARISON")
    print("=================================================================")

    print(f"{firstFile} SHA256:")
    print(firstHash)

    print("-----------------------------------------------------------------")

    print(f"{secondFile} SHA256:")
    print(secondHash)

    print("-----------------------------------------------------------------")

    if firstHash == secondHash:
        print("Result: Files are identical.")

    else:
        print("Result: Files do not match.")

    print("=================================================================")


def main():

    parser = argparse.ArgumentParser(
        description="SHA256 File Hash Checker"
    )

    parser.add_argument(
        "file1",
        help="First file"
    )

    parser.add_argument(
        "file2",
        nargs="?",
        help="Second optional file for comparison"
    )

    userInput = parser.parse_args()

    # check if first file exists
    if not os.path.exists(userInput.file1):
        print("First file does not exist.")
        return

    # if second file exists, compare both
    if userInput.file2:

        if not os.path.exists(userInput.file2):
            print("Second file does not exist.")
            return

        compareFiles(userInput.file1, userInput.file2)

    # otherwise just print hash of one file
    else:

        fileHash = generateFileHash(userInput.file1)

        if fileHash is None:
            print("Could not read file.")
            return

        print("\n=================================================================")
        print("SHA256 FILE HASH")
        print("=================================================================")

        print(f"File: {userInput.file1}")
        print(f"SHA256: {fileHash}")

        print("=================================================================")


if __name__ == "__main__":
    main()