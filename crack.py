import hashlib
import itertools
import time
from tqdm import tqdm

def hash_password(password, algorithm="md5"):
    if algorithm == "md5":
        return hashlib.md5(password.encode()).hexdigest()
    elif algorithm == "sha1":
        return hashlib.sha1(password.encode()).hexdigest()
    elif algorithm == "sha256":
        return hashlib.sha256(password.encode()).hexdigest()
    return hashlib.md5(password.encode()).hexdigest()

def dictionary_attack(hash_to_crack, wordlist_path, algorithm="md5"):
    print(f"[+] Starting Dictionary Attack on {algorithm}...")
    try:
        with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as file:
            for line in tqdm(file, desc="Trying passwords"):
                password = line.strip()
                if hash_password(password, algorithm) == hash_to_crack.lower():
                    return password
    except FileNotFoundError:
        print("[-] Wordlist not found!")
    return None

if __name__ == "__main__":
    print("=== PyCrack - Password Cracker ===\n")
    target_hash = input("Enter target hash: ").strip()
    mode = input("1. Dictionary\n2. Brute Force\nChoose: ").strip()
    algo = input("Hash type (md5/sha1/sha256): ").lower()

    if mode == "1":
        wordlist = input("Wordlist path: ")
        result = dictionary_attack(target_hash, wordlist, algo)
    else:
        print("Brute force - testing short passwords...")
        charset = "abcdefghijklmnopqrstuvwxyz0123456789"
        result = None
        start = time.time()
        for length in range(1, 5):
            for candidate in itertools.product(charset, repeat=length):
                pw = "".join(candidate)
                if hash_password(pw, algo) == target_hash.lower():
                    result = pw
                    break
            if result: break
        print(f"Time taken: {time.time()-start:.2f}s")

    if result:
        print(f"\n🎉 Cracked! Password: {result}")
    else:
        print("\n[-] Not found.")
