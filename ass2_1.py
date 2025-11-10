import socket
import time


class Sender:
    def __init__(self, e, n):
        self.e = e
        self.n = n

    def encrypt(self, plaintext):
        start_time = time.perf_counter()  # Using high-resolution timer
        cipherText = pow(plaintext, self.e, self.n)
        encryption_time = time.perf_counter() - start_time  # End time
        return cipherText, encryption_time


def main():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('localhost', 65432))
            print("Sender: Requesting public key from receiver...")
            data = s.recv(1024).decode()
            e, n = map(int, data.split(','))
            print(f"Sender: Received public key (e={e}, n={n}) from receiver")

            while True:
                try:
                    plaintext = int(input("Sender: Enter an integer plaintext to encrypt "))
                    if plaintext <= 0 or plaintext >= n:
                        raise ValueError("Plaintext must be in the range (0, n)")
                    break
                except ValueError as ve:
                    print(f"Invalid input: {ve}, Please try again")

            sender = Sender(e, n)
            cipherText, encryption_time = sender.encrypt(plaintext)
            print(f"Sender: Ciphertext is: {cipherText}")
            print(f"Encryption Time is: {encryption_time:.6f} seconds")
            s.sendall(str(cipherText).encode())
            print("Sender: Ciphertext is sent to receiver")

    except socket.error as e:
        print(f"Socket Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
