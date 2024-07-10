# Schweitzer Engineering Laboratories (SEL) SEL-3505-5

The SEL-3505-5 is a real-time automation controller (RTAC) used in a wide variety of industrial control systems. These RTACs are ubiquitous in the power industry. The firmware is not available for download, but I emailed customer support from my AFIT email and asked politely for some firmware versions. They were happy to oblige and sent me three different versions, although you only need one for this lab. 

This RTAC is a text-book example of security for embedded system firmware. They did pretty much everything correctly (at least with their firmware). In order to break their security, I am providing additional data obtained via JTAG.

* rtac.upg - Raw firmware update file as received from SEL
* 0xfff00000_0xffffffff.bin - This is a raw memory dump from the device, obtained via JTAG
* upgd_extract_upg_package - This executable was extracted from a device using JTAG
* upg_decrypt.py - Starting point for you to write a Python script to decrypt the firmware

<div align="center">
<img src="./img/02.png" width="200">
</div><br/>



# Encryption Refresher

There are two main types of encryption: symmetric and asymmetric. 

Symmetric encryption uses the same key for both encryption and decryption. This form of encryption is much faster than asymmetric encryption and is used for encrypting/decrypting bulk data.

Asymmetric encryption uses a public key for one direction and a private key for the other. The public key can be shared with anyone; the private key must be kept secret. This form of encryption is used to validate the source and integrity of the data (i.e., digital signatures). It can also be used for authentication.

