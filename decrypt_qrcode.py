import html.parser
import qrcode

encrypted_data = 'UA;&lt;7'
key = b'mysecretkey'

encrypted_data = str.encode(html.unescape(encrypted_data))

def decrypt_data(encrypted_data, key):
    """Decrypt the data using XOR encryption and a given key"""
    data = bytearray(len(encrypted_data))
    key_len = len(key)
    for i in range(len(encrypted_data)):
        data[i] = encrypted_data[i] ^ key[i % key_len]
    return bytes(data)

decrypted_data= (decrypt_data(encrypted_data, key).decode())
print(decrypted_data)


def generate_qr_code(id):
    key = b'mysecretkey'
    qr = qrcode.QRCode(version=3,
                       box_size=5,
                       border=3,)
    qr.add_data(id)
    qr.make()
    img = qr.make_image(fill_color="#fffde9",
                        back_color="black")
    img.save(f'passes/QRcode/{id}.png', format='PNG')


generate_qr_code(decrypted_data)
