import qrcode
from PIL import Image, PngImagePlugin
import argon2
import secrets
from sqlalchemy import create_engine, Column, Integer, String, LargeBinary
from sqlalchemy.orm import sessionmaker, declarative_base
from io import BytesIO
from getpass import getpass
import numpy as np

# SQLAlchemy setup
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(255))
    password = Column(String(255))
    hashed_password = Column(String(255))
    qr_code_image = Column(LargeBinary)

# Generate QR Code with Input Text
def generate_qr_code(input_text):
    qr = qrcode.QRCode(
        version=3,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=2,
    )
    qr.add_data(input_text)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

    # Save image to BytesIO buffer
    img_buffer = BytesIO()
    img.save(img_buffer, format="PNG")

    return img_buffer.getvalue()

# Embed Salt into Image Metadata
def embed_salt_into_image(image_data, salt):
    # Open the image using PIL
    img = Image.open(BytesIO(image_data))

    # Convert image to numpy array
    img_array = np.array(img)

    # Flatten the salt into a binary string
    salt_binary = ''.join(format(byte, '08b') for byte in salt)

    # Embed each bit of the salt into the least significant bit of each pixel channel
    salt_index = 0
    for i in range(img_array.shape[0]):
        for j in range(img_array.shape[1]):
            for k in range(img_array.shape[2]):
                img_array[i, j, k] &= 0b11111110  # Clear the LSB
                img_array[i, j, k] |= int(salt_binary[salt_index])  # Set the LSB with the salt bit
                salt_index = (salt_index + 1) % len(salt_binary)

    # Create a new image from the modified array
    img_with_salt = Image.fromarray(img_array)

    # Save the image to BytesIO buffer
    img_buffer = BytesIO()
    img_with_salt.save(img_buffer, format="PNG")

    return img_buffer.getvalue(), salt

# Store Hash, QR Code Image, and Salt in Database
def store_in_database(username, password, hashed_password, qr_code_image_data):
    # Connect an SQL database
    engine = create_engine('mysql+pymysql://user:pass@localhost/database')

    # Create the table (only create_all if the table doesn't exist, otherwise, you may skip it)
    Base.metadata.create_all(engine)

    # Create a session to interact with the database
    Session = sessionmaker(bind=engine)
    session = Session()

    # Insert data into the Users table
    user = User(username=username, password=password, hashed_password=hashed_password, qr_code_image=qr_code_image_data)
    session.add(user)
    session.commit()
    print(f"User '{user.username}' added to database.")


if __name__ == "__main__":
    # Example input data
    username = input("User:")
    value_to_hash = getpass("Password Key:")
    site = input("Site:")

    # Generate a random salt
    generated_salt = secrets.token_bytes(16)

    # Hash the password using Argon2 with the generated salt
    hasher = argon2.PasswordHasher()
    hashed_password = hasher.hash(value_to_hash.encode(), salt=generated_salt)

    # Generate QR code with including the input text
    qr_code_image_data = generate_qr_code(f'{username}:{site}')

    # Embed salt into QR code image metadata
    qr_code_image_data_with_salt, embedded_salt = embed_salt_into_image(qr_code_image_data, generated_salt)
    with open(f"{username}-{site}.png", "wb") as file:
        file.write(qr_code_image_data_with_salt)

    # Store hash, QR code image, and salt in the database
    store_in_database(username, site, hashed_password, qr_code_image_data_with_salt)
