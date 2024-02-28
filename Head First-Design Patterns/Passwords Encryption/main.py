import hashlib
from random import sample
PEPPER = bytes("new Rabbit", encoding="utf-8").hex()
users = dict()

def get_salt():
    chars = list("asdfghjklñqwertyuiopzxcvbnmQWERTYUIOPASDFGHJKLÑZXCVBNM1234567890")
    salt = "".join(sample(chars, 5))
    print(f"Salt: {salt} - bytes: {bytes(salt, encoding='utf-8').hex()}")
    return bytes(salt, encoding="utf-8").hex()

def encode_password(password):
    encoded = hashlib.md5(bytes(password, encoding="utf-8"))
    return encoded.hexdigest()

def encode_with_salt(password, salt=None):
    if not salt:
        salt = get_salt()
    pass_encoded = encode_password(f"{salt}{password}")
    return "$".join([salt, pass_encoded])

def encode_with_salt_and_pepper(password, pepper, salt=None):
    if not salt:
        salt = get_salt()
    pass_encoded = encode_password(f"{pepper}{salt}{password}")
    return "$".join([salt, pass_encoded])

def addUser(name, password):
    if name in users:
        return
    password = encode_with_salt_and_pepper(password, PEPPER)
    users[name] = password

def comparePasswords(correct, salt, newPass):
    encoded = encode_with_salt_and_pepper(newPass, PEPPER, salt)
    if encoded.split("$")[1] == correct:
        print("Login Succesful")
    else:
        print("Error, incorrect password")
    print(f"{encoded.split('$')[1]}\n{correct}")

def login(name, password):
    if name not in users:
        print("User not registered")
        return 
    salt, correctPass = users[name].split("$")
    comparePasswords(correctPass, salt, password)

 
def main():
    password = "a pass"
    encoded = encode_password(password)
    print(encoded)
    encoded_salt = encode_with_salt(password)
    print(encoded_salt)
    encoded_salt_pepper = encode_with_salt_and_pepper(password, PEPPER)
    print(encoded_salt_pepper)
    encoded = encode_password(password)
    print()
    salt = get_salt()
    encoded = encode_password(password)
    print(encoded)
    encoded_salt = encode_with_salt(password, salt)
    print(encoded_salt)
    encoded_salt_pepper = encode_with_salt_and_pepper(password, PEPPER, salt)
    print(encoded_salt_pepper)
    print("\n")
    name = "Edu"
    password = "MyPass"
    addUser(name, password)
    login(name, password)
    print()
    login(name, "myPass")
    print(users)
    
    
    
if __name__ == "__main__":
    print()
    main()
    print()