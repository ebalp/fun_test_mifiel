import requests
import json
from hashlib import sha256


# primero obtendremos algunos bloques

response = requests.get("https://gameathon.mifiel.com/api/v1/games/first-brightness/blocks")

blocks = json.loads(response.content)

ob = blocks[-1] #one block with a few transactions

# ahora calcularemos el hash de un bloque

def hash(v):
    return sha256(sha256(v.encode()).digest()).digest().hex()

def block_to_hash(b):
    # version|prev_block_hash|merkle_hash|target|message|nonce
    to_hash = "1|"+b['prev_block_hash']+'|'+b['merkle_hash']+'|'+b['target']+'|'+b['message']+'|'+b['nonce']
    return to_hash

# esto muestra que calcular asi el hash de un bloque b es correcto
hash(block_to_hash(ob)) == ob['hash']

# ahora calcularemos el hash de una transaccion

def input2str(inpt):
    return inpt['prev_hash']+inpt['script_sig']+str(inpt['vout'])
def output2str(output):
    return str(output['value'])+str(len(output['script']))+output['script']
def trans_to_hash(tx):
    str_for_hash = '1' + \
        str(len(tx['inputs'])) +  ''.join([input2str(inpt) for inpt in tx['inputs']]) + \
        str(len(tx['outputs'])) + ''.join([output2str(output) for output in tx['outputs']]) + \
        '0'
    return hash(str_for_hash)[::-1]

tx = ob['transactions'][0]
trans_to_hash(tx) == tx['hash']    # algo esta mal aqui <----

# ahora crearemos el merkle-tree de un conjunto de transacciones

txs = ob['transactions']
txs_hashes = [trans_to_hash(tx) for tx in txs]

def merkle_tree_root(txs):
    if len(txs) == 1:
        return txs[0]
    if len(txs)%2 == 1:
        txs = txs + [txs[-1]]
    new_hashes = []

    for i in range(0, len(txs), 2):
        new_hashes = new_hashes + [hash(txs[i]+txs[i+1])]
    return merkle_tree_root(new_hashes)

# comprobar merkle tree hash:
merkle_tree_root(txs_hashes) == ob['merkle_hash']
