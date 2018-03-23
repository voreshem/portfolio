import hashlib

with open(input("The file's path is? "), "rb") as f:
    f = f.read()
    local_hash = hashlib.sha256(f).hexdigest()
remote_hash = input("The remote hash is? ")

print(local_hash); print(remote_hash)

if local_hash == remote_hash:
    print("Authentication successful!")