# Demonstrate how SHA-1 hashing ensures message integrity during transmission

import hashlib

def generate_hash(message: str) -> str:
    """Generate SHA-1 hash for the given message."""
    return hashlib.sha1(message.encode()).hexdigest()

def transmit_message(message: str, alter: bool = False) -> str:
    """
    Simulate message transmission over a network.
    Set alter=True to simulate message tampering during transit.
    """
    if alter:
        message += "!"  # Simulate attacker altering message
    return message

def verify_integrity(original_hash: str, received_message: str) -> bool:
    """Verify if the received message is the same as the original (by comparing hashes)."""
    received_hash = generate_hash(received_message)
    print("\n[Receiver]")
    print("Received Message:", received_message)
    print("Recomputed SHA-1 Hash:", received_hash)
    
    if original_hash == received_hash:
        print("\n✅ Integrity Verified — Message not altered during transmission.")
        return True
    else:
        print("\n❌ Integrity Failed — Message was modified during transmission!")
        return False

# ------------------ MAIN PROGRAM ------------------

print("=== SHA-1 Message Transmission Integrity Check ===")

# Step 1: Sender inputs a message
message = input("\nEnter the message to send: ")

# Step 2: Sender generates SHA-1 hash
sender_hash = generate_hash(message)

print("\n[Sender]")
print("Original Message:", message)
print("Generated SHA-1 Hash:", sender_hash)

# Step 3: Simulate transmission
# (Set alter=True to simulate an attack or corruption)
transmitted_message = transmit_message(message, alter=True)

# Step 4: Receiver verifies message integrity
verify_integrity(sender_hash, transmitted_message)