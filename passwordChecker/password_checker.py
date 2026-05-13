import re
import math
import argparse
import os


# load common passwords from text file
def loadPasswordList():

    if not os.path.exists("common_passwords.txt"):
        return []

    with open("common_passwords.txt", "r", encoding="utf-8") as file:
        passwordList = file.read().splitlines()

    return passwordList


# estimate password entropy
def calculatePasswordEntropy(userPassword):

    totalCharacterSet = 0

    # lowercase letters
    if re.search(r"[a-z]", userPassword):
        totalCharacterSet += 26

    # uppercase letters
    if re.search(r"[A-Z]", userPassword):
        totalCharacterSet += 26

    # numbers
    if re.search(r"[0-9]", userPassword):
        totalCharacterSet += 10

    # special symbols
    if re.search(r"[!@#$%^&*()_+=\-`~{}\[\]:;\"'<>,.?/|]", userPassword):
        totalCharacterSet += 32

    if totalCharacterSet == 0:
        return 0

    entropyValue = len(userPassword) * math.log2(totalCharacterSet)

    return round(entropyValue, 2)


def analyzePassword(userPassword):

    passwordScore = 0
    feedbackList = []

    commonPasswords = loadPasswordList()

    passwordLength = len(userPassword)

    print("\n=================================================================")
    print("RUNNING PASSWORD SECURITY ANALYSIS")
    print("=================================================================")

    # length scoring
    if passwordLength >= 16:
        passwordScore += 3

    elif passwordLength >= 12:
        passwordScore += 2

    elif passwordLength >= 8:
        passwordScore += 1

    else:
        feedbackList.append(
            "Use at least 12-16 characters for stronger security."
        )

    # lowercase letters
    if re.search(r"[a-z]", userPassword):
        passwordScore += 1
    else:
        feedbackList.append(
            "Add lowercase letters."
        )

    # uppercase letters
    if re.search(r"[A-Z]", userPassword):
        passwordScore += 1
    else:
        feedbackList.append(
            "Add uppercase letters."
        )

    # numbers
    if re.search(r"[0-9]", userPassword):
        passwordScore += 1
    else:
        feedbackList.append(
            "Include numbers in the password."
        )

    # special characters
    if re.search(r"[!@#$%^&*()_+=\-`~{}\[\]:;\"'<>,.?/|]", userPassword):
        passwordScore += 2
    else:
        feedbackList.append(
            "Use special characters like !, @, #, or $."
        )

    # repeated character patterns
    if re.search(r"(.)\1\1", userPassword):

        feedbackList.append(
            "Avoid repeated characters or predictable patterns."
        )

    else:
        passwordScore += 1

    # check against common password database
    if userPassword.lower() in commonPasswords:

        passwordScore = max(passwordScore - 4, 0)

        feedbackList.append(
            "This password appears in a common password database."
        )

    # max score should only be 10
    if passwordScore > 10:
        passwordScore = 10

    entropyScore = calculatePasswordEntropy(userPassword)

    print(f"Password Length : {passwordLength}")
    print(f"Entropy Score   : {entropyScore} bits")
    print(f"Security Score  : {passwordScore}/10")

    print("-----------------------------------------------------------------")

    # determine security level
    if passwordScore <= 3:
        print("Security Level  : Weak")

    elif passwordScore <= 6:
        print("Security Level  : Moderate")

    elif passwordScore <= 8:
        print("Security Level  : Strong")

    else:
        print("Security Level  : Very Strong")

    print("-----------------------------------------------------------------")

    print("Password Recommendations:")

    if feedbackList:

        for feedback in feedbackList:
            print(f"- {feedback}")

    else:
        print("- Excellent password. No major weaknesses detected.")

    print("-----------------------------------------------------------------")

    print("Best Practices:")
    print("- Use different passwords for each account")
    print("- Avoid using personal information")
    print("- Consider using a password manager")
    print("- Enable multi-factor authentication")

    print("=================================================================")


def main():

    parser = argparse.ArgumentParser(
        description="Advanced Password Strength Checker"
    )

    parser.add_argument(
        "password",
        help="Password to analyze"
    )

    userInput = parser.parse_args()

    analyzePassword(userInput.password)


if __name__ == "__main__":
    main()