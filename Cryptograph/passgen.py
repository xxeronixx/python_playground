import random
import string
import hashlib


def generate_password(input_word, length=12):
    # Use SHA-256 hash of the input word as the seed
    seed = int(hashlib.sha256(input_word.encode()).hexdigest(), 16)
    random.seed(seed)

    # Define character sets for different types of characters
    uppercase_letters = string.ascii_uppercase
    lowercase_letters = string.ascii_lowercase
    digits = string.digits
    symbols = string.punctuation

    # Combine character sets
    all_characters = uppercase_letters + lowercase_letters + digits + symbols

    # Ensure at least one character from each set
    password = (
            random.choice(uppercase_letters) +
            random.choice(lowercase_letters) +
            random.choice(digits) +
            random.choice(symbols)
    )

    # Generate the rest of the password
    for _ in range(length - 4):
        password += random.choice(all_characters)

    # Shuffle the password to make it more secure
    password_list = list(password)
    random.shuffle(password_list)
    password = ''.join(password_list)

    return password


if __name__ == "__main__":
    input_word = input("Enter the input word: ")
    password_length = int(input("Enter the desired password length: "))

    generated_password = generate_password(input_word, password_length)

    print("Generated Password:", generated_password)

# Generated Password: 9iu)v3hf9B-V