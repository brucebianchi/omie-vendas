import base64

def decode_base64(encoded_str):
    decoded_bytes = base64.b64decode(encoded_str)
    return decoded_bytes.decode('utf-8')

def encode_base64(original_str):
    return base64.b64encode(original_str.encode()).decode()
