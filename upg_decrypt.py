#!/usr/bin/env python3

# This script is based on a StackOverflow answer.
# https://stackoverflow.com/questions/35042164/how-to-decrypt-using-blowfish-in-pycrypto

# Install 
# sudo apt install -y python3-pycryptodome

# Import stuff here
from Cryptodome.Cipher import Blowfish

# Adjust these paths depending on where you put the files
input_filename  = 'sel3505/rtac.upg'
output_filename = 'sel3505/decrypted.bin'



# Read in the entire raw file ('rb' for reading binary file)
ciphertext = open(input_filename, 'rb').read()







# TODO: Implement the decryption here
msg = 'You forgot to code stuff'







open(output_filename, 'wb').write(msg)
