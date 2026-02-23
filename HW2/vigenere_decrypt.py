import collections
import math

# Expected English letter frequencies
ENGLISH_FREQ = [
    0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015, 0.06094,
    0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749, 0.07507, 0.01929,
    0.00095, 0.05987, 0.06327, 0.09056, 0.02758, 0.00978, 0.02360, 0.00150,
    0.01974, 0.00074
]

ciphertext = (
    "TTEUMGQNDVEOIOLEDIREMQTGSDAFDRCDYOXIZGZPPTAAITUCSIXFBXYSUNFESQRHISAFHRTQRVS"
    "VQNBEEEAQGIBHDVSNARIDANSLEXESXEDSNJAWEXAODDHXEYPKSYEAESRYOETOXYZPPTAAITUCRYBETHXUFINR"
)

print("Ciphertext length:", len(ciphertext), "\n")

# --- STEP 1: KASISKI EXAMINATION (FIND REPETITIONS) ---
print("=== Step 1: Finding Repetitions (Kasiski Test) ===")
def find_repetitions(text, min_len=3):
    reps = collections.defaultdict(list)
    for length in range(min_len, len(text) // 2):
        for i in range(len(text) - length + 1):
            seq = text[i:i+length]
            reps[seq].append(i)
            
    filtered = {}
    for seq, positions in reps.items():
        if len(positions) > 1:
            distances = [positions[j] - positions[j-1] for j in range(1, len(positions))]
            # Keep only the longest isolated sequences for cleaner output
            is_sub = False
            for oseq in reps.keys():
                if len(oseq) > len(seq) and seq in oseq and len(reps[oseq]) == len(positions):
                    is_sub = True
                    break
            if not is_sub:
                filtered[seq] = (positions, distances)
    return filtered

def get_factors(n, min_f=2, max_f=20):
    return [i for i in range(min_f, min(n + 1, max_f + 1)) if n % i == 0]

reps = find_repetitions(ciphertext)
print(f"{'Sequence':<12} {'Positions':<20} {'Distance':<12} {'Factors (2-20)'}")
print("-" * 65)
for seq, (pos, dists) in sorted(reps.items(), key=lambda x: -len(x[0])):
    if len(seq) >= 3:
        factors = get_factors(dists[0])
        print(f"{seq:<12} {str(pos):<20} {dists[0]:<12} {factors}")
print()

# --- STEP 2: INDEX OF COINCIDENCE ---
print("=== Step 2: Index of Coincidence (Confirming Key Length) ===")
def calc_ic(text):
    n = len(text)
    if n <= 1: return 0
    freqs = collections.Counter(text)
    return sum(f * (f - 1) for f in freqs.values()) / (n * (n - 1))

print(f"IC of entire ciphertext: {calc_ic(ciphertext):.4f}\n")
print(f"{'Key Length':<12} {'Avg IC':<12} {'Assessment'}")
print("-" * 40)
for p in range(2, 16):
    ics = [calc_ic(ciphertext[i::p]) for i in range(p)]
    avg_ic = sum(ics) / p
    assessment = "possible" if avg_ic > 0.053 else ""
    print(f"{p:<12} {avg_ic:.4f}       {assessment}")
print()

# --- STEP 3: FREQUENCY ANALYSIS (MUTUAL IC) ---
print("=== Step 3: Frequency Analysis (Recovering n=5 key letters) ===")
period = 5
key_letters = []

for i in range(period):
    group = ciphertext[i::period]
    freqs = collections.Counter(group)
    group_len = len(group)
    
    # Calculate fi: fraction of each letter in the group
    f = {chr(k+65): freqs.get(chr(k+65), 0) / group_len for k in range(26)}
    
    print(f"Group {i} ({group_len} chars)")
    print(f"  Letters: {group}")
    
    # Print frequency counts
    freq_str = " ".join([f"{char}:{count}" for char, count in sorted(freqs.items())])
    print(f"  Frequencies: {freq_str}\n")
    print(f"  {'Shift i':<10} {'Key Letter':<12} {'φ(i)'}")
    print(f"  {'-'*10} {'-'*12} {'-'*10}")
    
    shift_results = []
    # Test all 26 possible shifts
    for g in range(26):
        phi = 0
        for char_code in range(26):
            # p_(i-g)
            idx = (char_code - g) % 26
            phi += f[chr(char_code+65)] * ENGLISH_FREQ[idx]
        shift_results.append((g, chr(g+65), phi))
    
    # Sort by highest φ(i) descending
    shift_results.sort(key=lambda x: -x[2])
    
    for g, letter, phi in shift_results[:5]:
        print(f"  {g:<10} {letter:<12} {phi:.4f}")
        
    best_shift = shift_results[0]
    key_letters.append(best_shift[1])
    print(f"\n  → Key letter for position {i}: {best_shift[1]} (shift = {best_shift[0]})\n")

recovered_key = "".join(key_letters)
print(f"Recovered Key: {recovered_key}\n")

# --- STEP 4: DECRYPTION ---
print("=== Step 4: Decryption ===")
def decrypt_vigenere(ct, key):
    res = []
    for i, char in enumerate(ct):
        shift = ord(key[i % len(key)]) - 65
        dec_char_code = ((ord(char) - 65 - shift) % 26) + 65
        res.append(chr(dec_char_code))
    return "".join(res)

print("Key:", recovered_key)
print("Decrypted text (raw):")
print(decrypt_vigenere(ciphertext, recovered_key))
