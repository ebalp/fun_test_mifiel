from hashlib import sha256
import time

try:
    message = sys.argv[1] 
    difficulty = sys.argv[2] 
except:
    message = 'Hello, world!'
    difficulty = 3

def hash(v, n):
    return sha256(sha256((v+str(n)).encode()).digest()).digest().hex()


start = time.time()
nonce = 0

while hash(message, nonce)[:difficulty] != '0'*difficulty:
    nonce += 1
 
print('Finished after {} Seconds'.format(round(time.time() - start,6)))
print('PoW Hash: {}'.format(hash(message, nonce)))
print('Nonce used: {}'.format(nonce))