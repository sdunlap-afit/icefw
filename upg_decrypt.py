#!/usr/bin/env python3

# This script is based on a StackOverflow answer.
# https://stackoverflow.com/questions/35042164/how-to-decrypt-using-blowfish-in-pycrypto

# Install 
# pip install pycryptodome

# Import stuff here


# Read in the raw file ('rb' for reading binary file)
ciphertext = open('rtac.upg', 'rb').read()


# TODO: Implement the decryption here
decrypted = 'You forgot to code stuff'







open('decrypted.bin', 'wb').write(decrypted)
