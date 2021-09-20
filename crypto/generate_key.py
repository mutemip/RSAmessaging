import random, sys, os
from . import large_prime_numbers
from . import mode_inverse


def generateKey(keySize):
    p = 0
    q = 0
    # print('Generating p prime...')
    while p == q:
        p = large_prime_numbers.generateLargePrime(keySize)
        q = large_prime_numbers.generateLargePrime(keySize)
    n = p * q
    # print('Generating e that is relatively prime to (p-1)*(q-1)...')
    while True:
        e = random.randrange(2 ** (keySize - 1), 2 ** (keySize))
        if mode_inverse.gcd(e, (p - 1) * (q - 1)) == 1:
            break
    # print('Calculating d that is mod inverse of e...')
    d = mode_inverse.findModInverse(e, (p - 1) * (q - 1))
    publicKey = (n, e)
    privateKey = (n, d)
    publicKey = ('%s,%s,%s' % (keySize, publicKey[0], publicKey[1]))
    privateKey = ('%s,%s,%s' % (keySize, privateKey[0], privateKey[1]))
    return (publicKey, privateKey)

generateKey(1024)
