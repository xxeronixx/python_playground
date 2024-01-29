from pyzbar.pyzbar import decode
import cv2
import os

def read_salt_from_image(image_file, salt_length):
    image_file = os.path.expanduser(image_file)
    if not os.path.exists(image_file):
        print(f"Error: The file '{image_file}' does not exist.")
        return None
    img = cv2.imread(image_file)
    if img is None:
        print(f"Error: Unable to read the image at '{image_file}'.")
        return None
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Extract salt from the least significant bit of each pixel channel
    salt_binary = ""
    bits_read = 0
    for i in range(img_rgb.shape[0]):
        for j in range(img_rgb.shape[1]):
            for k in range(img_rgb.shape[2]):
                salt_binary += str(img_rgb[i, j, k] & 1)
                bits_read += 1
                if bits_read == salt_length * 8:  # Stop when you have enough bits
                    break
            if bits_read == salt_length * 8:
                break
        if bits_read == salt_length * 8:
            break

    # Convert binary salt to bytes
    salt_bytes = int(salt_binary, 2).to_bytes((len(salt_binary) + 7) // 8, byteorder='big')

    # Read the QR code from the image using pyzbar
    qr_code_data = decode(img_rgb)

    if qr_code_data:
        # Extract the QR code data
        qr_data = qr_code_data[0].data.decode("utf-8")
        return qr_data, salt_bytes
    else:
        return None, None

if __name__ == "__main__":
    # Provide the full absolute path to the QR code image
    image_file = "qr_code_image.png"
    # Set the length of salt you want to extract in bytes
    salt_length = 16
    # Read salt from the saved image
    qr_code_data, read_salt= read_salt_from_image(image_file, salt_length)
    if qr_code_data:
        print("QR Code Data:", qr_code_data)
        print("Read Salt:", read_salt.hex())
    else:
        print("No QR Code found or couldn't decode.")
