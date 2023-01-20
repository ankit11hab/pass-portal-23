from Crypto.Cipher import AES
import base64

# AES 'pad' byte array to multiple of BLOCK_SIZE bytes


def pad(byte_array):
    BLOCK_SIZE = 16
    pad_len = BLOCK_SIZE - len(byte_array) % BLOCK_SIZE
    return byte_array + (bytes([pad_len]) * pad_len)

# Remove padding at end of byte array


def unpad(byte_array):
    last_byte = byte_array[-1]
    return byte_array[0:-last_byte]


def encrypt(key, message, iv):
    """
    Input String, return base64 encoded encrypted String
    """

    byte_array = message.encode("UTF-8")

    padded = pad(byte_array)

    # generate a random iv and prepend that to the encrypted result.
    # The recipient then needs to unpack the iv and use it.
    # iv = os.urandom(AES.block_size)
    cipher = AES.new(key.encode("UTF-8"), AES.MODE_CBC, iv.encode())
    encrypted = cipher.encrypt(padded)
    # Note we PREPEND the unencrypted iv to the encrypted message
    return base64.b64encode(encrypted).decode("UTF-8")+base64.b64encode(iv.encode("UTF-8")).decode("UTF-8")


def decrypt(key, message):
    """
    Input encrypted bytes, return decrypted bytes, using iv and key
    """

    # byte_array = base64.b64decode(message)

    iv = base64.b64decode(message[-24:])
    # encrypted message is the bit after the iv
    messagebytes = base64.b64decode(message[0:-24])

    cipher = AES.new(key.encode("UTF-8"), AES.MODE_CBC, iv)

    decrypted_padded = cipher.decrypt(messagebytes)

    decrypted = unpad(decrypted_padded)

    return decrypted.decode("UTF-8")

# def callencrypt():

# def main():

#     key = "0123456789123456"
#     iv = "0123456789123456"
#     rollno = "1234"
#     fee_id = "78M65"
#     amount = "20"
#     dataToEncrypt = rollno+"|"+fee_id+"|"+amount
#     encrypted = encrypt(key, dataToEncrypt, iv)
#     print(decrypt(key, encrypted))


# main()