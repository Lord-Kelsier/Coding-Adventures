import numpy as np
# notar que al hacerlo asi, podemos cambiar el orden de los caracteres y hacer nuestro propio encoding de
# base 64
BASE64CHARS = np.array(list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"))

def encode64(msg: bytes, returnAsStr=False) -> bytes: 
  if not isinstance(msg, bytes):
    raise TypeError(f"msg must be a byte array, but is type: {type(msg)}")
  remainingBits = None
  encodedMsg = ""
  for octetCount, char in enumerate(msg):
    if octetCount % 3 == 0:
      index = char >> 2
      encodedMsg += BASE64CHARS[index]
      remainingBits = char & 0b11
    elif octetCount % 3 == 1:
      index = (remainingBits << 4) + (char >> 4)
      encodedMsg += BASE64CHARS[index]
      remainingBits = char & 0xf
    elif octetCount % 3 == 2:
      index = (remainingBits << 2) + (char >> 6)
      encodedMsg += BASE64CHARS[index]
      index = char & 0x3f
      encodedMsg += BASE64CHARS[index]

  if octetCount % 3 == 0:
    index = remainingBits << 4
    encodedMsg += BASE64CHARS[index]
    remainingBits = -1
    octetCount += 1 
  if octetCount % 3 == 1:
    if remainingBits == -1:
      encodedMsg += "=="
    else:
      index = remainingBits << 2
      encodedMsg += BASE64CHARS[index] + "="
  if returnAsStr:
    return encodedMsg
  return bytes(encodedMsg, encoding = 'utf8')

def decode64(msg: bytes): 
  if not isinstance(msg, bytes):
    raise TypeError(f"msg must be a byte array, but is type: {type(msg)}")
  msgArray = np.array(list(msg))
  decodingTable = {char: idx for idx, char in enumerate(BASE64CHARS)}
  base64_char_set = set(BASE64CHARS)
  base64_char_set.add("=")
  decodedMsg = bytes()
  if len(msg) % 4 != 0:
    raise ValueError("msg isn't encoded in base 64")
  for index in range(0, len(msg), 4):
    char1 = chr(msgArray[index])
    char2 = chr(msgArray[index + 1])
    char3 = chr(msgArray[index + 2])
    char4 = chr(msgArray[index + 3])
    if char1 not in base64_char_set or \
        char2 not in base64_char_set or \
        char3 not in base64_char_set or \
        char4 not in base64_char_set:
      raise ValueError(f"word isn't encoded in base 64 {char1}-{char2}-{char3}-{char4}")
    padding = 0
    if char3 == "=":
      padding += 1
    if char4 == "=":
      padding += 1

    if padding == 0:
      char1, char2, char3, char4 = map(lambda x: decodingTable[x], (char1, char2, char3, char4))
    elif padding == 1:
      char1, char2, char3 = map(lambda x: decodingTable[x], (char1, char2, char3))
      char4 = 0
    elif padding == 2:
      char1, char2 = decodingTable[char1], decodingTable[char2]
      char3, char4 = 0, 0
    # 1st
    newCharOrd = (char1 << 2) + (char2 >> 4)
    decodedMsg += newCharOrd.to_bytes(1, "big")
    # 2nd
    if padding == 0 or padding == 1:
      newCharOrd = ((char2 & 0xf) << 4) + (char3 >> 2)
      decodedMsg += newCharOrd.to_bytes(1, "big")
    # 3rd
    if padding == 0:
      newCharOrd = ((char3 & 0b11) << 6) + char4
      decodedMsg += newCharOrd.to_bytes(1, "big")
  return decodedMsg

if __name__ == '__main__':
  import os
  
  message = b"\x11\xff\x00"
  print(f"Message: {message}\n")
  encodedMessage = encode64(message)
  print(f"Encoded: {encodedMessage}\n")
  print(f"Decoded: {decode64(encodedMessage)}")
  path = input("Path of a file: ")
  if not os.path.exists(path):
    exit()
  
  folder = os.path.dirname(path)
  fileName = os.path.basename(path).split(".")
  
  with open(path, "rb") as f:
    data = f.read()
  data = encode64(data)
  newPath = os.path.join(folder, ".".join([fileName[0] + "Encoded"] + fileName[1:]))
  with open(newPath, "wb") as f:
    f.write(data)
  data = decode64(data)
  newPath = os.path.join(folder, ".".join([fileName[0] + "Decoded"] + fileName[1:]))
  with open(newPath, "wb") as f:
    f.write(data)