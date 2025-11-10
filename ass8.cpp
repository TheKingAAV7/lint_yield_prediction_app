// assignment8
#include <iostream>
#include <vector>
#include <string>
#include <bitset>
#include <iomanip>  // ✅ for setw()

using namespace std;

// Simple 8x8 grayscale image (cover)
vector<vector<int>> cover_image = {
    {100, 150, 200, 50, 75, 125, 175, 225},
    {120, 160, 210, 60, 80, 130, 180, 230},
    {140, 170, 220, 70, 90, 140, 190, 240},
    {110, 155, 205, 55, 85, 135, 185, 235},
    {130, 165, 215, 65, 95, 145, 195, 245},
    {150, 175, 225, 75, 105, 155, 205, 255},
    {160, 185, 235, 85, 115, 165, 215, 250},
    {180, 195, 245, 95, 125, 175, 225, 255}
};

// --- Embed message in LSB ---
vector<vector<int>> embed_lsb(const vector<vector<int>>& img, const string& msg) {
    vector<vector<int>> stego = img;
    string bits;

    // Convert message to bitstream
    for (char c : msg) {
        bitset<8> b(c);
        bits += b.to_string();
    }
    bits += "00000000";  // Null terminator

    size_t bit_idx = 0;  // ✅ Changed to size_t to match bits.size()
    for (int i = 0; i < 8 && bit_idx < bits.size(); ++i) {
        for (int j = 0; j < 8 && bit_idx < bits.size(); ++j) {
            int pixel = stego[i][j];
            int bit = bits[bit_idx++] - '0';
            stego[i][j] = (pixel & ~1) | bit;  // Set LSB
        }
    }
    return stego;
}

// --- Extract message from LSB ---
string extract_lsb(const vector<vector<int>>& stego_img) {
    string bits;

    for (int i = 0; i < 8; ++i)
        for (int j = 0; j < 8; ++j)
            bits += (stego_img[i][j] & 1) + '0';

    string msg;
    for (size_t i = 0; i + 8 <= bits.size(); i += 8) {
        bitset<8> b(bits.substr(i, 8));
        char c = static_cast<char>(b.to_ulong());
        if (c == '\0') break;  // Stop at null terminator
        msg += c;
    }
    return msg;
}

// --- Print image matrix ---
void print_image(const vector<vector<int>>& img, const string& label) {
    cout << label << ":" << endl;
    for (const auto& row : img) {
        for (int p : row)
            cout << setw(4) << p;  // ✅ setw now recognized
        cout << endl;
    }
    cout << endl;
}

// --- Main Program ---
int main() {
    string secret = "SECRET";

    cout << "Original Cover Image (8x8 Grayscale):" << endl;
    print_image(cover_image, "Cover");

    auto stego_image = embed_lsb(cover_image, secret);
    cout << "Stego Image (Message '" << secret << "' hidden in LSB):" << endl;
    print_image(stego_image, "Stego");

    cout << "=== Transmission over Unsecured Network ===" << endl;
    cout << "Stego Image sent... (Attacker sees only stego, no secret visible)" << endl;

    string extracted = extract_lsb(stego_image);
    cout << "=== Extraction at Receiver ===" << endl;
    cout << "Extracted Message: " << extracted << endl;
    cout << "Integrity: " << (extracted == secret ? "Verified ✅ (No Tampering)" : "Failed ❌") << endl;

    return 0;
}