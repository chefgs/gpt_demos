import os

def xor_encrypt_decrypt(input_file, output_file, key):
    """Encrypt or decrypt a file using XOR encryption."""
    with open(input_file, 'rb') as f:
        file_data = f.read()

    # XOR the file data with the key
    encrypted_data = bytearray([byte ^ key for byte in file_data])

    with open(output_file, 'wb') as f:
        f.write(encrypted_data)

def main():
    # Input image file
    input_image = "input_image.jpg"
    # Encrypted file
    encrypted_image = "encrypted_image.enc"
    # Decrypted file
    decrypted_image = "decrypted_image.jpg"
    # Key for encryption and decryption (must be the same)
    encryption_key = 42  # Example key, you can choose any value 0-255

    print("Encrypting the image...")
    xor_encrypt_decrypt(input_image, encrypted_image, encryption_key)
    print(f"Image encrypted and saved as {encrypted_image}")

    print("Decrypting the image...")
    xor_encrypt_decrypt(encrypted_image, decrypted_image, encryption_key)
    print(f"Image decrypted and saved as {decrypted_image}")

if __name__ == "__main__":
    main()
