import random
import hashlib

def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def mod_inverse(a, m):
    for i in range(1, m):
        if (a * i) % m == 1:
            return i
    return None

def generate_keypair():
    p = q = 1
    while not is_prime(p):
        p = random.randint(100, 1000)
    while not is_prime(q) or p == q:
        q = random.randint(100, 1000)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = random.randint(2, phi - 1)
    while gcd(e, phi) != 1:
        e = random.randint(2, phi - 1)
    d = mod_inverse(e, phi)
    return (e, n), (d, n)

def rsa_encrypt(message, public_key):
    e, n = public_key
    return [pow(ord(char), e, n) for char in message]

def rsa_decrypt(encrypted_message, private_key):
    d, n = private_key
    return ''.join([chr(pow(char, d, n)) for char in encrypted_message])

def generate_signature(message, private_key):
    hashed_message = hashlib.sha256(message.encode()).hexdigest()
    return rsa_encrypt(hashed_message, private_key)

def verify_signature(message, signature, public_key):
    hashed_message = hashlib.sha256(message.encode()).hexdigest()
    decrypted_signature = rsa_decrypt(signature, public_key)
    return decrypted_signature == hashed_message

print("Generating keys for X (sender) and Y (receiver)...")
public_key_X, private_key_X = generate_keypair()
public_key_Y, private_key_Y = generate_keypair()

message = input("\nEnter message from X → Y: ")

encrypted_message = rsa_encrypt(message, public_key_Y)
signature = generate_signature(message, private_key_X)

print("\nEncrypted Message:", encrypted_message)
print("Signature:", signature)

try:
    pr_x = "test"
    de = rsa_decrypt(encrypted_message, pr_x)
    print("Z trying to read message:", de)
except:
    print("Z (attacker) failed to decrypt message — not authorized.")

decrypted_message = rsa_decrypt(encrypted_message, private_key_Y)
is_valid = verify_signature(decrypted_message, signature, public_key_X)

print("\nReceiver Side:")
print("Decrypted Message:", decrypted_message)
if is_valid:
    print("Signature Verified — Message Integrity and Authenticity Confirmed.")
else:
    print("Signature Invalid — Message may have been tampered.")

