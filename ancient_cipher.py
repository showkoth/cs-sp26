def ancient_cipher(cipher_text, origin_text):
    if len(cipher_text) != len(origin_text):
        return False
    
    cipher_freq = {}
    origin_freq = {}
    # Count frequency of each character in both strings
    for char in cipher_text:
        cipher_freq[char] = cipher_freq.get(char, 0) + 1
    
    for char in origin_text:
        origin_freq[char] = origin_freq.get(char, 0) + 1

    return sorted(cipher_freq.values()) == sorted(origin_freq.values())

if __name__ == "__main__":
    result = ancient_cipher("JWPUDJSTVP", "VICTORIOUS")
    if result:
        print("YES")
    else:
        print("NO")