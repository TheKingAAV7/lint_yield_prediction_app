#include <iostream>
#include <cstdint>

using namespace std;

using ull = uint64_t;

// Modular exponentiation: base^exp mod mod
ull mod_pow(ull base, ull exp, ull mod) {
    ull result = 1;
    base %= mod;
    while (exp > 0) {
        if (exp % 2 == 1) {
            result = (__int128)result * base % mod;
        }
        base = (__int128)base * base % mod;
        exp /= 2;
    }
    return result;
}

// Diffie-Hellman Participant
class DHParticipant {
public:
    ull p, g, priv, pub;
    DHParticipant(ull prime, ull gen) : p(prime), g(gen), priv(0), pub(0) {
        priv = (rand() % (p - 2)) + 2;  // Random private 2 to p-2
        pub = mod_pow(g, priv, p);
    }
    ull compute_shared(ull other_pub) {
        return mod_pow(other_pub, priv, p);
    }
};

// Simulate normal DH exchange
void normal_dh() {
    ull p = 23, g = 5;
    DHParticipant alice(p, g);
    DHParticipant bob(p, g);
    
    ull alice_key = alice.compute_shared(bob.pub);
    ull bob_key = bob.compute_shared(alice.pub);
    
    cout << "=== Normal Diffie-Hellman Exchange ===" << endl;
    cout << "Public params: p=" << p << ", g=" << g << endl;
    cout << "Alice private: " << alice.priv << ", public A=" << alice.pub << endl;
    cout << "Bob private: " << bob.priv << ", public B=" << bob.pub << endl;
    cout << "Alice computed key: " << alice_key << endl;
    cout << "Bob computed key: " << bob_key << endl;
    cout << (alice_key == bob_key ? "✓ Shared key matches!" : "✗ Mismatch!") << endl << endl;
}

// Simulate MITM attack
void mitm_attack() {
    ull p = 23, g = 5;
    DHParticipant alice(p, g);
    DHParticipant bob(p, g);
    DHParticipant eve(p, g);
    
    // Eve intercepts: Alice's A -> Eve sends E to Bob
    // Bob's B -> Eve sends B to Alice (relays to Alice)
    ull alice_key = alice.compute_shared(bob.pub);  // Alice gets B (from Eve relay)
    ull bob_key = bob.compute_shared(eve.pub);      // Bob gets E
    ull eve_alice_key = eve.compute_shared(bob.pub); // Eve with Alice's view (B)
    ull eve_bob_key = eve.compute_shared(alice.pub); // Eve with Bob's view (A)
    
    cout << "=== Man-In-The-Middle Attack ===" << endl;
    cout << "Public params: p=" << p << ", g=" << g << endl;
    cout << "Alice private: " << alice.priv << ", public A=" << alice.pub << endl;
    cout << "Bob private: " << bob.priv << ", public B=" << bob.pub << endl;
    cout << "Eve private: " << eve.priv << ", public E=" << eve.pub << endl;
    cout << "Attack Flow:" << endl;
    cout << "- Alice sends A to 'Bob' (intercepted by Eve)" << endl;
    cout << "- Eve sends E to Bob (impersonates Alice)" << endl;
    cout << "- Bob sends B to 'Alice' (intercepted by Eve)" << endl;
    cout << "- Eve sends B to Alice (impersonates Bob)" << endl;
    cout << "Alice computed key (with relayed B): " << alice_key << endl;
    cout << "Bob computed key (with E): " << bob_key << endl;
    cout << "Eve's key with Alice: " << eve_alice_key << endl;
    cout << "Eve's key with Bob: " << eve_bob_key << endl;
    cout << "Alice/Bob keys match? " << (alice_key == bob_key ? "Yes (but wrong!)" : "No") << endl;
    cout << "Eve controls both sides: Can decrypt Alice<->Eve and Bob<->Eve traffic." << endl;
    cout << "✗ Attack successful - No authentication!" << endl;
}

int main() {
    srand(42);  // Seed for reproducibility
    normal_dh();
    mitm_attack();
    return 0;
}