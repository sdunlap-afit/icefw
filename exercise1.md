

# Rockwell Automation 1756-L61

The 1756-L61 is a CPU module for the ControlLogix series of PLCs. It is used in a wide variety of industrial control systems. The firmware is stored in a flash chip and is updated over the network. I have provided three different versions of the firmware for the 1756-L61. These were simply downloaded from Rockwell's website. You will need to analyze them and answer the questions above.

* PN-49503.bin - version 16.56
* PN-49505.bin - version 16.80
* PN-69415.bin - version 18.11

<div align="center">
<img src="./img/01.png" width="200">
</div><br/>


## Questions

1. What processor architecture is the firmware compiled for?
1. What high-level language (i.e., NOT assembly) was used to write all/most of the firmware source code?
1. Is the majority of the firmware encrypted, compressed, or neither?
1. Is there a file system in the firmware?
1. Where are the checksum and crc stored in the firmware?



## Instructions

Open a terminal and navigate to the directory with the firmware files.

    ```bash
    cd firmware_lab_files
    ```

1. What processor architecture is the firmware compiled for?

    You can use the `strings` command to look for compiler information in the firmware. Look for strings that indicate the compiler or the processor architecture.

    ```bash
    strings PN-49503.bin | less
    ```

    You can also use the `binwalk` tool to look for common processor architectures.

    ```bash
    binwalk -A PN-49503.bin
    ```


1. Is the majority of the firmware encrypted, compressed, or neither?

    There are many ways to check for this. One way is to use the `strings` command to look for human-readable strings in the firmware. If you see a lot of garbage characters, the firmware is likely compressed or encrypted. If you see a lot of human-readable strings, it's probably not compressed or encrypted.

    ```bash
    strings PN-49503.bin | less
    ```

    You can also use the `binwalk` tool to look for common compression and encryption signatures.

    ```bash
    binwalk PN-49503.bin
    ```

    You can also check the entropy of the firmware to see if it is compressed or encrypted. Compressed or encrypted content will have very high entropy (basically a flat line on the graph).
    
    ```bash
    binwalk -E PN-49503.bin
    ```


