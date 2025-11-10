import socket
import random
import time
import math


def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y


def mod_inverse(e, phi):
    gcd, x, _ = extended_gcd(e, phi)
    if gcd != 1:
        raise ValueError("Inverse doesn't exist")
    return x % phi


def find_coprime(phi):
    while True:
        e = random.randint(2, phi - 1)
        if gcd(e, phi) == 1:
            return e


class Receiver:
    def __init__(self, d, n):
        self.d = d
        self.n = n

    def decrypt(self, cipherText):
        start_time = time.perf_counter()  # Using high-resolution timer
        decrypted_text = pow(cipherText, self.d, self.n)
        decryption_time = time.perf_counter() - start_time  # End time
        return decrypted_text, decryption_time


def main():
    p = int(input("Enter first Prime Number: "))
    q = int(input("Enter second Prime Number: "))
    if not (is_prime(p) and is_prime(q)):
        print("Both p & q must be prime")
        return
    n = p * q
    phi = (p - 1) * (q - 1)
    e = find_coprime(phi)
    d = mod_inverse(e, phi)
    print(f"Generated Public Key: (e={e}, n={n})")
    print(f"Generated Private Key: (d={d}, n={n})")
    receiver = Receiver(d, n)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', 65432))
        s.listen()
        print("Receiver: Waiting for connection from Sender...")
        conn, addr = s.accept()
        with conn:
            print(f"Receiver: Connected by {addr}")
            public_key = f"{e},{n}"
            conn.sendall(public_key.encode())
            print("Receiver: Public Key is sent to Sender")
            data = conn.recv(1024)
            if data:
                cipherText = int(data.decode())
                print(f"Receiver: Ciphertext received: {cipherText}")
                decrypted_text, decryption_time = receiver.decrypt(cipherText)
                print(f"Receiver: Decrypted Text is: {decrypted_text}")
                print(f"Decryption Time is: {decryption_time:.6f} seconds")


if __name__ == "__main__":
    main()
