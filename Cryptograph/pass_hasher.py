import argon2
import qrcode

def hash_password(password):
    # Hash the password using Argon2
    hasher = argon2.PasswordHasher()
    hashed_password = hasher.hash(password)
    return hashed_password

def generate_qr_code(data, output_file):
    # Generate a QR code from the data
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Create an image from the QR code
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the image to a file
    img.save(output_file)

if __name__ == "__main__":
    # Get password input
    password = input("Enter the text to hash: ")

    # Hash the password using Argon2
    hashed_password = hash_password(password)
    print("Hashed Password:", hashed_password)

    # Generate a QR code containing the hashed password
    qr_code_data = f"Username:{input('Username:')}"
    output_file = "hashed_password_qr.png"
    generate_qr_code(qr_code_data, output_file)

    print(f"QR code containing the hashed password saved to {output_file}")
