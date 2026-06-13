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

def brute_force_attack(hash_to_crack, max_length=6, algorithm="md5"):
    print(f"[+] Starting Brute Force (max length: {max_length})...")
    print("[!] This can be slow for longer lengths.\n")
    
    charset = "abcdefghijklmnopqrstuvwxyz0123456789"
    start_time = time.time()
    
    for length in range(1, max_length + 1):
        print(f"[*] Trying length {length}...")
        total = len(charset) ** length
        for candidate in tqdm(itertools.product(charset, repeat=length), total=total, desc=f"Len {length}"):
            password = "".join(candidate)
            if hash_password(password, algorithm) == hash_to_crack.lower():
                print(f"\n[+] PASSWORD CRACKED: {password}")
                print(f"[+] Time taken: {time.time() - start_time:.2f} seconds")
                return password
    return None

if __name__ == "__main__":
    print("=== PyCrack - Password Cracker ===\n")
    target_hash = input("Enter target hash: ").strip().lower()
    mode = input("1. Dictionary Attack\n2. Brute Force Attack\nChoose (1/2): ").strip()
    algo = input("Hash type (md5/sha1/sha256) [md5]: ").lower() or "md5"

    if mode == "1":
        wordlist = input("Wordlist path [rockyou.txt]: ") or "rockyou.txt"
        result = dictionary_attack(target_hash, wordlist, algo)
    else:
        max_len = int(input("Max length to try (4-7 recommended): ") or "6")
        result = brute_force_attack(target_hash, max_length=max_len, algorithm=algo)

    if result:
        print(f"\n🎉 SUCCESS! Password is: {result}")
    else:
        print("\n[-] Password not found.")
