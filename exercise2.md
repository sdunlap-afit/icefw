# Schweitzer Engineering Laboratories (SEL) SEL-3505-5

The SEL-3505-5 is a real-time automation controller (RTAC) used in a wide variety of industrial control systems. These RTACs are ubiquitous in the power industry. The firmware is not available for download, but I emailed customer support from my AFIT email and asked politely for some firmware versions. They were happy to oblige and sent me three different versions, although you only need one for this lab. 

This RTAC is a textbook example of security for embedded system firmware. They did pretty much everything correctly (at least with their firmware). To break their security, I am providing additional data obtained via JTAG.

* rtac.upg - Raw firmware update file received from SEL
* 0xfff00000_0xffffffff.bin - This is a raw memory dump from the device, obtained via JTAG
* upgd_extract_upg_package - This executable was extracted from a device using JTAG
* upg_decrypt.py - Starting point for you to write a Python script to decrypt the firmware

<div align="center">
<img src="./img/02.png" width="200">
</div><br/>


# Encryption Refresher

There are two main types of encryption: symmetric and asymmetric. 

Symmetric encryption uses the same key for both encryption and decryption. This form of encryption is much faster than asymmetric encryption and is used for encrypting/decrypting bulk data. These algorithms are often block ciphers, meaning they encrypt data in fixed-size blocks. If the last block is not the correct size, it is padded with the length of the padding. In addition to the symmetric key, many algorithms also require an initialization vector (IV). This is a random value that is used to start the encryption process. 

Asymmetric encryption uses a public key for one direction and a private key for the other. The public key can be shared with anyone; the private key must be kept secret. This form of encryption is used to validate the source and integrity of the data (i.e., digital signatures). It can also be used for authentication. Public/private keys are often stored in plain text or in a well-known format. Binwalk knows how to search for common formats like PEM and DER.


# Initial analysis

Use the tools from exercise 1 to analyze the firmware. Is the firmware encrypted and/or compressed?



# Firmware Update Utility

Using JTAG, we managed to extract memory from a physical device. In the memory dumps, we found an ELF executable responsible for conducting firmware updates. We also found some interesting sections of memory that may prove useful. The ELF and memory dump are provided in `firmware_lab_files/`. We now need to reverse-engineer this ELF file to determine how the firmware is encrypted. For this, we'll use Ghidra, a free reverse engineering tool developed by the NSA.


## Disassembling the executable

1. Open Ghidra and create a new project.
1. Import `upgd_extract_upg_package` file into the project and under `Language`, select `PowerPC` variant `default`.
1. Double-click on `upgd_extract_upg_package` to open it in CodeBrowser.
1. Select `Yes` and then `Analyze` to analyze the file.
1. Select `Window/Functions` to open the functions panel and then sort by name.
1. Look for functions starting with `EVP_`. These are likely encryption functions.
1. Select `EVP_bf_cbc` (there are two) and look for an XREF starting with `FUN_`. Double-click the XREF to jump to the call.
1. Open the decompile window and analyze the function.

    <div align="center">
    <img src="./img/ex2_01.png">
    </div><br/>

1. Open the function immediately following `EVP_bf_cbc` and use the function calls to guess what it's doing. 
1. Go back to the call immediately following `EVP_bf_cbc` and analyze the function parameters in the decompile window. Specifically, note the integer that is added to the cipher text pointer and subtracted from the length parameter. This gives us a critical clue about the firmware format.
1. There is a function call with similar parameters a few lines before the call to `EVP_bf_cbc`. Open this function and analyze it.


# Finding the encryption keys

The keys needed to validate and decrypt the firmware must be stored in the RTAC's non-volatile memory somewhere; otherwise, the device would not be able to decrypt the firmware. We have a memory dump from the device, so let's look for the keys. Depending on how the keys are stored, it could be very difficult to find them. Generally, PKI keys are easier to find than symmetric keys because they are larger and have a specific format. 

Example public key from `https://phpseclib.com/docs/rsa-keys`:

```
-----BEGIN PUBLIC KEY-----
MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAKj34GkxFhD90vcNLYLInFEX6Ppy1tPf
9Cnzj4p4WGeKLs1Pt8QuKUpRKfFLfRYC9AIKjbJTWit+CqvjWYzvQwECAwEAAQ==
-----END PUBLIC KEY-----
```

First, use strings to search for a public key that might be used to validate the firmware. We don't necessarily need this information, but it's good to know where it is stored. 

```bash
strings 0xfff00000_0xffffffff.bin | less
```

**Important note:** Engineers are predictable and tend to store associated data together. If you find one key, you may find others nearby. 

Look at the strings near the public key and see if any look like they could be symmetric keys. Additionally, try to find the IV, which is most likely stored near the symmetric key.


# Python script

With this information, we have what we need to write our own script to decrypt the firmware. Use the provided `upg_decrypt.py` as a starting point. You will need to fill in the missing code.

The first answer at the following link gives a good example of how to decrypt Blowfish in Python: 

https://stackoverflow.com/questions/35042164/how-to-decrypt-using-blowfish-in-pycrypto

Copy the required sections of the answer and update the values as needed. Don't forget the offset value we identified in the disassembly step. Once you have the script working, decrypt the firmware and analyze the new file.


# Decrypted file analysis

We can repeat our standard initial inspection with the new file. Try looking for strings and checking the entropy. Also, use `binwalk` to look for common compression signatures. 

```bash
strings decrypted.bin | less
binwalk -E decrypted.bin
binwalk decrypted.bin
```

# Extract the firmware

`binwalk` tells us that the file is a standard `tar.gz` archive. We **could** use `binwalk` to extract it, but it's easier to use `tar` directly. `tar` will extract the files into the current directory, which may be confusing. We can move the file into a temp directory before extracting it to keep everything clean.

```bash
mkdir tmp
cp decrypted.bin tmp/decrpyted.tar.gz
cd tmp
tar -xzf decrypted.tar.gz
ls
```

If all goes well, this will result in three new directories, `nor/`, `sbin/`, and `scripts/`. 

**Congrats!** Now that we have the firmware extracted, we can start analyzing it. What we do from here would depend on the specific questions we are trying to answer or the goals we are trying to achieve. You will learn more about the next steps in software reverse engineering.


# Extra credit

Analyze the extracted files and see if you can find the `upgd_extract_upg_package` file in the `nor/` directory. This will require some analysis and recursive file extraction. Hint: `fs` stands for file system.


