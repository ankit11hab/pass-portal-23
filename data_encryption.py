



def decrypt_data(encrypted_data, key):
    """Decrypt the data using XOR encryption and a given key"""
    data = bytearray(len(encrypted_data))
    key_len = len(key)
    for i in range(len(encrypted_data)):
        data[i] = encrypted_data[i] ^ key[i % key_len]
    return bytes(data)

# Encrypt data


# Decrypt data
decrypted_data = decrypt_data(encrypted_data, key)
print(decrypted_data) # Output: b'Hello World'
