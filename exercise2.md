# CubeSpace CW0057 Reaction Wheel
Reaction wheels (RW) are satellite components that adjust orientation. By spinning the RW, the satellite spins in the opposite direction, allowing the satellite to be precisely oriented by controlling RW that are mounted on different axes.

The CubeSpace CW0057 RW vendor documentation indicates that this device runs with bare-metal firmware consisting of a bootloader and a control program.

Our job is to figure out how this device works so that we can implement our own rootkit.

Needed items:
- Linux tools:
  - vbindiff -> compare files
  - crc32 -> generate crc32 values
- Hex Editor -> analyze/modify files
- bootloader [.hex / .cs] -> vendor provided firmware
- controlprog [.hex / .cs] -> vendor provided firmware

### Linux Setup
<details closed>
<summary>Linux Tools Setup</summary>
To install Vbindiff, open up a terminal and run the following:

```bash
sudo apt install vbindiff
```
To install crc32, open up a terminal and run the following:
```bash
sudo apt install libarchive-zip-perl
```
</details>

## File Analysis Instructions
We start this process by gathering as much information as we can from the vendor documentation. Everything they tell us is something we don't have to discover for ourselves.

1. According to the vendor, the device runs on bare metal. What does this tell us about the firmware?
   <details closed>
   <summary>Hint</summary>
   There is no space on this embedded system to host an OS, so we can't expect code that must be interpreted by an OS.
   </details>
   <br>
   <details closed>
   <summary>Answer</summary>
   We expect the firmware to be a raw binary file (.bin) -> This allows it to run 'as-is' on a processor which is typical for bare metal applications.
   </details>
<br>

2. We have been given access to a .hex file and a .cs file for the bootloader and control program. The hex file is a relatively common format, but the .cs file is a format created by the vendor. Based on our analysis above, we expect the RW to need a .bin file, so what would be a logical guess for the design of the .cs file?
    <details closed>
    <summary>Answer</summary>
    The .cs file is most likely a .bin file -> it may or may not be modified in some way.
    </details>
    <br>

3. How can we test our assumption about the .cs file?
    <details closed>
    <summary>Hint</summary>
    The .hex format is commonly used as an intermediate step for compiling/flashing instructions onto bare metal devices.
    </details>
    <br>
    <details closed>
    <summary>Answer</summary>
    We can convert the .hex to .bin and then compare our .bin to the .cs file.
    </details>
    <br>

4. Open a terminal in the same location as your .hex file. Run the following command to generate a .bin from the .hex file:
   ```bash
   objcopy --input-target=ihex --output-target=binary controlprog.hex cpfromhex.bin
   ```
<br>

5. Now we want to compare the files side-by-side in our hex editor. Look for patterns, what do you notice?
   <details closed>
   <summary>Hint</summary>
   Look near byte 0x70 in the .cs
   </details>
   <br>
   <details closed>
   <summary>Answer</summary>
   Start of .bin:
   <br>
   <img width="740" height="110" alt="image" src="fromHexClip.png" />
   <br>
   Byte 73 of .cs:
   <br>
   <img width="740" height="282" alt="image" src="csClip.png" />
   </details>
<br>

6. It appears that the .cs is a .bin file with a header. We can confirm this by removing the header and saving it separately.

   Highlight the first 0x72 bytes in your hex editor and delete them -> save the file as 'cptrim.bin'.

   **Note: If you use a VS Code extension as your hex editor this may not work the first time. Close out VS code, re-open controlprog.cs and repeat the process. Sometimes VS Code corrupts the new file while saving it as a .bin.**

   Repeat the process, but this time save only the header as 'cphead.bin'.

7. Now that we have our trimmed file, we can use vbindiff to verify if we have any differences between our cpfromhex.bin and our cptrim.bin. Open a terminal in the same folder as your files and run the following:

   ``` bash
   vbindiff cptrim.bin cpfromhex.bin
   ```
   What do you see?
   <details closed>
    <summary>Answer</summary>
    The files are the same. Pressing RET to find next difference goes to the end of the file.
    <br>
    <img width="959" height="990" alt="image" src="vbindiff.png" />
    <br>
    We have now proven that our .cs is a .bin file with a header. Next we'll analyze the header.
   </details>

## .CS Header Analysis
Before we dive in to the header analysis, we should consider what information we expect to find.

1. Discussion Questions:
   <details closed>
    <summary>What do we already know about the operation of this device?</summary>
    It runs bare metal code for a processor
   </details>
   <details closed>
    <summary>How does a processor interpret instructions?</summary>
    It reads commands sequentially, editing data and following jumps as they're encountered -> It doesn't 'think' big-picture, it only understands the current instruction.
   </details>
   <details closed>
    <summary>Would this file work if it were stored incorrectly?</summary>
    No -> If the file is not located precisely where it should be in memory, the processor will not run the program correctly.
   </details>
   <br>
2. Limited by the constraints of bare metal programming, what kind of questions does the header need to answer to successfully load this program?
   <details closed>
    <summary>Hint</summary>
    The bootloader itself is running on bare metal and is responsible for receiving and loading the control program.
   </details>
   <br>
   <details closed>
    <summary>Answer</summary>
    - How big is this file? <br>
    - How do I know I have the right file? <br>
    - Where does this file go? <br>
    - What other information could be useful for the creator to save? <br>
   </details>
   <br>
3. Let's start looking at the header: The very first byte is 0x72.
   <details closed>
    <summary>Have we seen this number before? Where?</summary>
    When we trimmed the file.
   </details>
   <details closed>
    <summary>What do we think this field is?</summary>
    Header length.
   </details>
   <details closed>
    <summary>How big is this field? Do people prefer odd or even numbers?</summary>
    It is most likely not a single-byte field, probably 2 bytes given that it's a smaller number.
   </details>
   <details closed>
    <summary>What does the layout of this field tell us?</summary>
    Assuming a 2x byte field -> this data is stored little-endian.
   </details>
   <br>
4. This header is for a device from a company that manufactures a wide range of space components. If your main focus is making money, one of your key goals is to minimize costs. Reusing code is very good for saving time/money -> how would you develop a header if you wanted to use it across many different devices, including some that aren't designed yet?

   <details closed>
    <summary>Answer</summary>
    Use Padding. You can reserve space for future growth while also fixing locations for data fields.
    <br> What data value does CubeSpace use for padding? -> 00
   </details>
   <br>

5. Moving on to the next data bytes, we see 70 03 03:
   <details closed>
    <summary>Do we think this is the whole field?</summary>
     People like even numbers -> We probably need to include the trailing 00 in this field.
   </details>
   <details closed>
    <summary>How should we read this number?</summary>
     Assuming little-endian -> 00030370.
   </details>
   <details closed>
    <summary>Have we seen this number? Based on what we've already seen, what's a good guess for this field?</summary>
    We've already seen a header length, it would make sense to have a data length field.
   </details>
   <details closed>
    <summary>How can we check this assumption?</summary>
    Refer to vbindiff screenshot above, the final line of the cptrim file is 00030370. (The first byte is located at 00000000, so the file is this long even though the last data byte is at address 0003036f).
   </details>
   <br>

6. We have now found two length fields. The vendor documentation briefly describes that there is a check for file integrity and size as a safety measure to prevent overflowing the processor memory with an invalid control program.

   How would we ensure file integrity?
   
   <details closed>
    <summary>Hint</summary>
    There are multiple possible methods, so 'guess and check' is a valid technique for trying them all -> however, we already told you above with the 'needed tools'.
   </details>
   <details closed>
    <summary>Answer</summary>
    Cyclic Redundancy Check (CRC). We won't cover the details of how it works here, but it is a technique for checking if a file was transmitted/stored correctly.
   </details>
   <br>
   <details closed>
    <summary>Is this a valid method of data security?</summary>
    NO! We will exploit this weakness later in the exercise.
   </details>
   <br>
   Let's figure out what value we should be looking for -> what file should we focus on?
   <details closed>
    <summary>Hint</summary>
    We need to find a crc, but is the header necessary for the program to run?
   </details>
   <details closed>
   <summary>Answer</summary>
    The header is only used for helping the bootloader load the program into the processor memory -> we need to find the crc for our cptrim.bin file.
   </details>
   <br>
   Open up a terminal and run the following:

   ```bash
   crc32 'filename'
   ```
   What is our output?
   <details closed>
   <summary>Answer</summary>
    <img width="735" height="85" alt="71AD7106" src="crc.png" />
   </details>
<br>

7. Based on what we've seen so far, it's reasonable to expect even-byte little-endian data fields for the rest of our header. Looking at the next 4 bytes, we see 00 40 01 08 -> 08014000.
   <details closed>
   <summary>Do we see this number anywhere?</summary>
   No. It's too big to be a location in our program -> time to step away from the code files for a minute.
   </details>
   <br>
   We still haven't confirmed anything about the hardware on the reaction wheel -> we will do that now.
   <details closed>
   <summary>Open the Case</summary>
   We see the following:
   <br>
   <img width="800" height="765" alt="image" src="RWInternal.png" />   
   </details>
   <details closed>
   <summary>What kind of processor do we have?</summary>
   It's an STM32L452CEU3.
   </details>
   <details closed>
   <summary>What should we do now?</summary>
   Google it and find a data sheet!

   Looking it up we learn that it is an ARM processor with 512kB of flash memory.

   <img width="537" height="347" alt="image" src="STMlookup.png" />

   Our data sheet also conveniently contains a memory map for the processor:

   <img width="830" height="380" alt="image" src="STMmemory.png" />
   </details>
   <details closed>
   <summary>Given everything we just learned, what is that data field?</summary>
   It's a write address, telling the bootloader where to save this program in the processor memory.
   </details>
<br>

8. We've found some critical data fields that we will need later, can you identify the next few fields in the header? What are the values?
   <details closed>
   <summary>Hint</summary>
   We wouldn't expect endianness to change, and people typically like even numbers when working with binary data.
   </details>
   <details>
   <summary>Answer</summary>
   Assuming 4 byte fields, the next three fields contain the data 0x03, 0x01, and 0x30. These fields are followed by some padding identied by multiple bytes of 00.
   </details>
   <details>
   <summary>Do we know what these fields are?</summary>
   It's possible that these are a version number or some other kind of internal 'note' for the person that created the header. We don't have any conclusive evidence of these field identities.
   </details>
   <br>

9. Next, we finally encounter some bytes that make sense as a string!
   <details>
   <summary>What does the first string tell us?</summary>
   This string identifies the intended device that the program is meant to run on. The cube wheel is the vendor's name for a reaction wheel.
   </details>
   <details>
   <summary>What does the second string tell us?</summary>
   This string identifies the file type. This file is a control program.
   </details>
   <details>
   <summary>What is the length of these data fields?</summary>
   There are 32 bytes between the start of each string and the start of the first data following the strings -> It's reasonable to assume each string is either a 16 byte string followed by 16 bytes of padding, or a 32 byte string, we can't know for sure.
   </details>
   <details>
   <summary>Why include these fields?</summary>
   This is speculation -> The vendor is likely utilizing a common header for all firmware on all devices they make. These data fields allow for a programmer to quickly ID what file they have open. The fact that these strings are stored in a readable layout (instead of little-endian) supports the idea that these data fields are primarily meant for people.
   </details>
   <br>

10. Following our strings, we have a few more bytes to interpret. We mentioned earlier that it's best to gather as much information from the vendor as possible to save time. To that end, we connected our RW to the vendor software and started clicking around and stumbled across build numbers and version numbers that match these bytes -> This led us to the conclusion that the 8 bytes following the strings are build/version info.
    <details>
    <summary>Do we actually care about that?</summary>
    Not necessarily -> but identifying these data fields as the build/version numbers means that those earlier values of 0x03, 0x01, and 0x30 are something else.
    </details>
    <br>

11. Finally, we have 4 bytes remaining in our header.
<br> Is there any typical data for file creation that is missing?
    <details>
    <summary>Hint</summary>
    Every piece of work you have ever turned in (homework, job, etc) usually includes a few key pieces of information at the top of the first page. What have we not seen in this header yet?
    </details>
    <details>
    <summary>Answer</summary>
    A date. Software commonly has a 'build time' that can be stored in the compiled file. This time is generally given in seconds from a starting point: often the Unix Time Epoch of January 1st, 1970.
    </details>
    <details>
    <summary>How do we check this assumption?</summary>
    Note: Online converters make this easy. <br>
    First, we convert our data (66C884D2) into a decimal value: 1724417234
    <br>
    <img width="870" height="450" alt="image" src="buildtime.png" />
    <br>
    Then we plug this value into an epoch converter:
    <img width="800" height="290" alt="image" src="date.png" />
    </details>

## .CS Header Summary
We have finished analyzing our header and have identified several key fields that we will use later. For convenience, here a summary image showing the fields we identified.
<details>
   <summary>Header Fields</summary>
   <img width="904" height="532" alt="image" src="headerMap.png" />
   </details>

## Bootloader Header Analysis
Now it's your turn! Answer the following questions using the bootloader and control program files:

1. How big is the bootloader header?
   <details>
   <summary>Answer</summary>
   0x72 bytes
   </details>
   <details>
   <summary>What can we infer about the header from this data value?</summary>
   It is probably identical to the header format we just analyzed.
   </details>
   <br>
2. How big is the bootloader file and where is it stored on our processor?
   <details>
   <summary>Answer</summary>
   It is 0x00011938 bytes, stored at 0x08000000
   </details>
   <details>
   <summary>What is noteworthy about this address?</summary>
   It is the start of flash memory on the processor.
   </details>
   <br>
3. What's the CRC for the bootloader file?
   <details>
   <summary>Answer</summary>
   B093A03E
   </details>
   <br>
4. Using the bootloader file, how can we update our analysis of the string fields?
   <details>
   <summary>Answer</summary>
   These fields contain strings greater than 16 bytes -> it makes sense to conclude the string fields are 32 bytes.
   </details>
   <br>
5. Was the bootloader or the control program compiled first? (Don't use a converter for this task)
   <details>
   <summary>Answer</summary>
   These fields are identical between files except for the last byte (C0 vs D2) -> C0 is smaller than D2 -> The bootloader was compiled first, by 18 seconds.
   </details>
   <br>
6. CHALLENGE: Assuming nothing else is stored besides the bootloader and control program, what does the flash memory look like on the processor? How much total open space is available?
   <details>
   <summary>Hint</summary>
   The numbers we see in these headers are hex values, not decimal -> don't forget to convert when discussing available space. Are the bootloader and control program back-to-back in memory?
   </details>
   <details>
   <summary>Answer</summary>
   
   Bootloader: 0x08000000 -> 0x08011937<br>
   Empty: 0x08011938 -> 0x08013FFF<br>
   Control Program: 0x08014000 -> 0x0804436F<br>
   Empty: 0x08044370 -> 0x0807FFFF (reserved memory starts 0x08080000)<br>

   Available Memory:<br>
   Empty1 = 3FFF - 1938 (+1) = 26C8 = 9928 bytes<br>
   Empty2 = 7FFFF - 44370 (+1) = 3BC90 = 244880 bytes<br>
   Total = 9928 + 244880 = 254,808 bytes ~ 255 kB
   </details>
   <details>
   <summary>Follow Up Question</summary>
   Why would the bootloader and control program not be stored back-to-back?<br> -> Allows files to be updated individually. If the bootloader got 1 byte bigger, and the files were stored back-to-back, you'd have to reconfigure the entire control program too.
   </details>

## Ghidra Set-Up
<details closed>
<summary>Set-Up</summary>
<br>

Requirments: Install Ghidra if it isn't already on your machine, then install prefered Hex editor. I will be using ImHEX.
1. Ghidra Windows: [https://github.com/NationalSecurityAgency/ghidra/releases]. Linux: [snap install ghidra]
2. ImHEX [https://imhex.werwolv.net/]

### Set-Up
1. First rename the Reaction Wheel Firmware to control_program.cs and make a copy called control_program_copy.cs
2. Once you have Ghidra installed open it in Linux via the terminal by typing ```ghidra```or in Windows by double-clicking the run script in the unzipped file. <br>
   <img width="680" height="462" alt="image" src="https://github.com/user-attachments/assets/d39750fc-1508-4805-b085-6aa038377e7b" />
3. Once Ghidra is started click on the file tab in the top left and then click import file. Navigate to the location of your control_program_copy.cs and add it to Ghidra.

   <img width="611" height="515" alt="image" src="https://github.com/user-attachments/assets/e0521068-e23c-4815-bc36-5eef08c63c82" />

4. On the resulting window click on the three dots located to the right of the lnaguage box.
   <img width="663" height="346" alt="image" src="https://github.com/user-attachments/assets/e456fc8b-87b5-4685-8196-ad021d692d1f" />
5. What compiler have we identified the binary to be compiled by? What Endian? Use filter to narrow/search results.
   <details closed>
   <summary>Answer</summary>
   <br>
   <img width="546" height="377" alt="image" src="https://github.com/user-attachments/assets/be796647-9323-402a-a15e-a92e04c00d3c" />
   </details>
6. Select the options button in the bottom right of the window after you have selected the correct language.
   <img width="533" height="297" alt="image" src="https://github.com/user-attachments/assets/c03c44dc-7536-4ecb-a4eb-c525fa3d362d" />
7. What are we inspecting? What's the base address? Ho much space does the header take up? How long is the resulting program(Ghidra will give you this)?
   <details closed>
   <summary>Answer</summary>
   <br>
   <img width="548" height="422" alt="image" src="https://github.com/user-attachments/assets/d25c14f1-4076-4788-b331-2189884d1cd3" />
   </details>
8. Clcik Okay/Accept on all the resulting prompts then double click on your uploaded file. Click YES on the prompt asking if you want to analyze now and YES on the list options that it provides.<br>


### Now we want to add parts of the program that we don't have to the memory map.<br>

1. Click on the <img width="22" height="24" alt="image" src="https://github.com/user-attachments/assets/e2b1af7a-2f42-45ae-adf6-26a7e81e52e2" /> symbol on the menu loacted at the top of the Ghidra program.
    <img width="1226" height="426" alt="image" src="https://github.com/user-attachments/assets/3788ded0-d298-4358-a337-f7e2fba2dee5" />  
2. Select the Green add button located at the top right of the resulting menu.  
    <img width="1109" height="263" alt="image" src="https://github.com/user-attachments/assets/972d7072-ee1e-426f-b883-651b7bf561a9" />  
3. What are some parts of memory that could be useful? Where would we find references to these peices?  
   <details closed>
   <summary>Answer</summary>
   <br>
   <b>Communication</b>, Bootloader, Memory Writes, Memory References
   </details>
4. Now it's time for the most important part <b>Documentation!!</b>
5. Open the STM32_Doc.pdf. What would we be looking for? We discussed it just a second ago.
   <details closed>
   <summary>Answer</summary>
   <br>
   Memory Map!
   </details>
6. Crtl+F and look for the Memory Map for our chip. What sections should we add?
   <details closed>
   <summary>Answer</summary>
   <br>
   USART's(Specifically USART2), CAN
   </details>
   
7. Fill in the details and click add for each section you would like to add to the Memory Map. If you had a file you wanted to add you would select File Bytes at the bottom and navigate to the file you would like to include in that space in memory(Useful to add bootloader or other sections of code). <br>
    <img width="488" height="381" alt="image" src="https://github.com/user-attachments/assets/6f6524f1-00c7-49ea-9f40-db7c050957c5" />
   
8. Select the Alaysis tab at the top and select Analyze All Open, click Accept/YES on the following prompts to analyze your code with this new memory addition. (You can also select the C icon at the top of Ghidra to see the code decompiled in C)
    <img width="1222" height="360" alt="image" src="https://github.com/user-attachments/assets/aa975df7-e737-4464-8d7a-948129c7da94" />
9. <b>Congratualtions now you can begin Reverse Engineering the Firmware!!</b>
</details>


   


## Reverse Engineering

### Command Format
```
2 Bytes  1 Byte  Variable Bytes  2 Bytes
[Start Flag] [Command Code] [Data] [End Flag]
Example Command: 1f7f4000401c461fff
List Of Known Command Codes:
40  :Change  Speed (Speed number data is handled in IEEE 754 format)
41  :Duty  Cycle
80  :Identification
80  :Refresh  Home  Telemetry, Get  Info
81  :Serial  Number
82  :Error  Log  Index
83  :Error  Log  Entry
84 :Error  Log  Settings
85  :Current  Unix  Time
86  :Persist  Config  Diagnostic
88  :Version
89  :Boot  Status
8A :Telecommand  Acknowledge
8B :Common  Error  Codes
8C :Identification  2
B7  :Wheel  Position  Data
B8  :Wheel  Model
B9  :Wheel  Torque
BA  :Wheel  Reference  Torque
BB  :Control  Mode
BC  :Wheel  Speed
BD  :Health  Telemetry
BE  :Wheel  Data
BF  :PWM  Gain
C0  :Backup  Gain
C1  :Main  Gain
C2 :Status  Error  Flags
C3  :Wheel  Commanded  Duty  Cycle
C4  :Wheel  Reference  Speed
C5  :Motor  Power  Switch
C6  :Backup  Wheel  Codes
C7 :Stator  Data
C8  :Wheel  Reference  Speed  Ramp  Rate  Limit
```
<br>
<br>

### Instructions
1. Find the first line of code in the file. Where is it? Does it look like the program starts here?
	<details closed>
	<summary>Answer</summary>
	<br>
	Click on navigate if you haven't found it and enter the address of the first line of code.  
      <img width="1340" height="722" alt="image" src="https://github.com/user-attachments/assets/6e873574-d533-441b-ba0b-2e2f26ff52ab" />
	</details>
   
2. What are some issues an unclear start position can cause? How can this make it difficult to Reverse Engineer?
	<details closed>
	<summary>Answer</summary>
	<br>
	An unclear start position means the Ghidra can have trouble decompiling the code and walking through it. It also means that we can have issues following the control flow of the code.
	</details>
3. So what should we check if we can't follow the code from the start? What are some integral parts of the code that we can trace back to an area that allows us to insert our own jump command?
	<details closed>
	<summary>Hints</summary>
	<br>
	USART2(Check the location we added to memory map), Bootloader Jump to Firmware, **Command Code Resolution**, etc..
	</details>

4. What have you been able to find? Is there any room for a jump code insertion? What makes a good place for inserting our Jump code?
	<details closed>
	<summary>Hints</summary>
	<br>
	Look for places that we can choose ourselves whether it get's called. Possibly where we could insert custom commands.
	</details>

5. Go to the search menu at the top of Ghidra and select search for scalars from the resulting menu. Select "specific scalar" and then begin entering some of the command codes in hex. Which codes are more unique for hex? Try several of them if the first doesn't work out. What kind of code layout would be optimal for selecting the flow for differing command codes?
   <img width="1228" height="715" alt="image" src="https://github.com/user-attachments/assets/67dd4b50-a8ee-4064-a181-86b5cfb92471" />
	<img width="418" height="303" alt="image" src="https://github.com/user-attachments/assets/a85733d1-0b0e-4684-b701-f2f794d4de52" />
	
	<details closed>
	<summary>Hints</summary>
	<br>
	Switch statements are great for choosing which commands to execute! <br>
	<img width="766" height="561" alt="image" src="https://github.com/user-attachments/assets/f8defaf1-57a5-42b2-b994-f6f8b7c7464a" />
	</details>

6. Which variable does it use to jump? How does it resolve the code to the jump instruction? Take a look at the jump table and what values it holds and the location of the resulting jump. You'll have to do some math.
	<details closed>
	<summary>Hints</summary>
	<br>
	<img width="756" height="568" alt="image" src="https://github.com/user-attachments/assets/c0b51b8b-bac9-458f-9bc7-f14c067bd0b9" />
	<img width="399" height="183" alt="image" src="https://github.com/user-attachments/assets/d5bc5907-f7a5-4630-996a-c4e28e69a5ea" />
	</details>
	<details closed>
	<summary>Answer</summary>
	<br>
	From observing the index and parameter along with the resulting jump location we know that the index is found by [Command Code]-1 and the jump location is decide by ([Goal Address] – 0x08034a40)/2.
	</details>

7. Where does the 0x02B2h take you? The default case for the switch statement. This looks like a great place to insert our own command statement. Where should we make it jump to? The jump options are too short for the jump table to make it to the end of the file. Maybe there is another option?
	<details closed>
	<summary>Hints</summary>
	<br>
	Redundant Error Statements are the perfect place to insert our Jump Code.
	<img width="1173" height="150" alt="image" src="https://github.com/user-attachments/assets/c771ef50-a748-44ae-8c33-258a8da03b82" />
	</details>

8. First let's make our Jump Table jump to the last line of the redundant error statement whenever we send a command code of 09. Do the math! Right click on the correct index and click Patch Data and type the correct set of bytes to jump to the last line of our error statement (0x008034b04).  <br>
	<img width="776" height="617" alt="image" src="https://github.com/user-attachments/assets/5d26a0b9-5815-494c-b574-ed9e0d2c20a2" />
	<details closed>
	<summary>Answer</summary>
	<br>
	 <img width="451" height="260" alt="image" src="https://github.com/user-attachments/assets/271fc480-15bf-440d-9b36-19855985f3dc" />
	</details>

9. Now we need to find where we want our Jump command to navigate to. Look for an unused section of memory/code or add code onto the end of the file.
 	<details closed>
	<summary>Hint</summary>
	<br>
	Go to 0x08039828
	</details>

10. Now that we have identified the location we are going to add the code to, go back and add a ```bl``` instruction to the last line of our Redundant Error statement that we jump to. Right click on the line and select patch instruction. Then type ```bl``` in the left box and ```0x08039828``` in the right box.  <br>
<img width="576" height="516" alt="image" src="https://github.com/user-attachments/assets/507dbe00-9923-465c-b05e-6809c2c5b04e" />
<img width="652" height="149" alt="image" src="https://github.com/user-attachments/assets/0f586351-6fe3-4321-912b-ebfd6da85247" />

11. Congratulation you have successfully patched in a jump to your own instructions! Now it's time to learn how to change the way the program functions.
12. Navigate to Case 40(The set speed command 0x08034978) and look for what register/variable is used to set the speed.
 	<details closed>
	<summary>Hint</summary>
	<br>
	r4 is used to store the Float value of the speed.
	</details>

13. Let's edit what value our code sets the speed to be a constant rather then a variable. Right click on a free line of memory, preferably further down to leave room for our commands, and right click, hover over data, and then click on the float variable. Then right click again and select patch data(like we did in the previous instructions) and then set the float value to a constant, like 10 for example.
<img width="655" height="667" alt="image" src="https://github.com/user-attachments/assets/cec7b8c3-8c96-4742-a54c-3bff2db0606e" />

14. Now we want to add commands that set r4 to our intended value. Our assembler doesn't like to load 4 bytes of memory into one register in a single command so we are going to utilize the move high (```movt```) and the move low(```movw```) instructions to reference our constant. Ghidra helps you format your commands, can you figure it out?
 	<details closed>
	<summary>Answer</summary>
	<br>
	<img width="975" height="495" alt="image" src="https://github.com/user-attachments/assets/476d7130-cf70-4797-97df-6f5d65fc3ebd" />
	</details>
15. Now that we have set the value of the register to our constant we can jump to the actual set speed instructions.
 	<details closed>
	<summary>Answer</summary>
	<br>
	```bl	0x08034978```
	</details>
 16. What are we forgetting? The HEADER! We won't be able to upload the file without the header containing the file info! Now navigate to the File tab in the top left of Ghidra and select export program. Make sure the format is set to Original program in order to export it as a .cs.  <br>
	<img width="632" height="216" alt="image" src="https://github.com/user-attachments/assets/c946f86d-5ed5-4409-a7d2-433996f34ccc" />

17. Make sure to store a copy of your .cs file by compressing it into a zip folder, we'll come back to this in a bit.
    <img width="267" height="186" alt="image" src="https://github.com/user-attachments/assets/81516235-85a1-4d16-8796-21a138006a83" />

    
19. Open up ImHEX(after following the prompts) and drag your control_program.cs and your control_program_copy.cs into the editor. On your exported control_program_copy.cs left click on the first byte and select insert. You are going to want to insert the size of the header (0x72).
    <img width="778" height="713" alt="image" src="https://github.com/user-attachments/assets/16e6b8a7-84d8-43cb-86a3-cc923100fea6" />
    <img width="952" height="514" alt="image" src="https://github.com/user-attachments/assets/5e65011e-c05f-4757-ad33-9f3410e4083b" />

20. Now move over to your control_program.cs and copy the first 0x72 bytes and then past them into your control_program_copy.cs. Make sure to save the file when you are done copying the header.  <br>
    <img width="560" height="542" alt="image" src="https://github.com/user-attachments/assets/bea68643-b064-40a1-b131-31fd3bd472c8" />
    <img width="555" height="567" alt="image" src="https://github.com/user-attachments/assets/bab5d145-5d7c-4f73-abb5-f39344473d63" />

21. Remember what bytes in the header are the CRC value? Navigate into the zip folder and right click on the file. Click on the properties menu and you should see the CRC value displayed on the bottom half.  <br>
    <img width="357" height="446" alt="image" src="https://github.com/user-attachments/assets/b4e31fb2-5c8d-4f5f-8e34-cc602ae73cbb" />
    
22. Replace the CRC bytes in the header with what is displayed on your properties menu. Remember that the program operates in little endian! Save the file when you are done. Don't worry, your CRC value may different then mine depending on where we wrote the instructions and saved the float value.  <br>
 	<details closed>
	<summary>Answer</summary>
	<br>
	<img width="591" height="302" alt="image" src="https://github.com/user-attachments/assets/fcf751ec-f014-4267-a0a6-53a1c572942f" />
	</details>
    

23. Congrats! You have successfully implement your proof of concept rootkit! What other functions would we be able to develop using a more flushed out rootkit? Communicate from the device to other connected devices! Set their speed, replace firmware, override instructions., and more! Brodcasts to bootloader commands:
```
		undefined Send_UART_Cmd()  
	    r0:4           input  
	    r1:4           length  
	    r2:4           usart  
	    r0:4           end_flag  
	Send_UART_Cmd  
	    cpsid      i  
	    movw       r0, #0x98f0  
	    movt       r0, #0x803  
	    movs       length, #0x18  
	    movw       r2, #0x4400  
	    movt       r2, #0x4000  
	    movw       r5, #0x4428  
	    movt       r5, #0x4000  
	loop
	    ldrb       r3, [input, #0x0]  
	    adds       end_flag, #0x1 
	    subs       length, #0x1
	    cmp        r3, #0x1f  
	    bne        normal_send  
	    ldrb       r4, [end_flag, #0x0]  
	    cmp        r4, #0xff  
	    bne        normal_send  
	    adds       end_flag, #0x1  
	    subs       length, #0x1  
	    bl         wait_txe  
	    movs       r6, #0x1f  
	    strb       r6, [r5, #0x0] 
	    bl         wait_txe  
	    movs       r6, #0xff  
	    strb       r6, [r5, #0x0] 
	    bl         wait_tc_loop  
	    bl         send_break  
	    b          check_continue  
	normal_send  
	    bl         wait_txe  
	    strb       r3, [r5, #0x0]  
	check_continue  
	    cmp        length, #0x0  
	    bne        loop  
	    nop 
	    cpsid      i 
	    dsb        #0xf  
	    isb        #0xf  
	    bl         FUN_0801a514  
	    bx         lr  
	wait_txe  
	    ldr        r4, [r2, #0x1c]  
	    tst        r4, #0x80  
	    beq        wait_txe  
	    bx         lr  
	wait_tc_loop  
	    ldr        r4, [r2, #0x1c]  
	    tst        r4, #0x40  
	    beq        wait_tc_loop  
	    bx         lr  
	send_break  
	    movs       r7, #0x2  
	    strb       r7, [r2, #0x1c]  
	wait_break_clear  
	    ldr        r4, [r2, #0x1c]  
	    tst        r4, #0x40000  
	    bne        wait_break_clear  
	wait_for_input  
	    ldr        r4, [r2, #0x1c]  
	    tst        r4, #0x20  
	    beq        wait_for_input 
	    ldr        r4, [r2, #0x24]  
	    bl         loop 
	080398f0 1f               
	080398f1 7f              
	080398f2 06              
	080398f3 1f              
	080398f4 ff              
	080398f5 1f              
	080398f6 7f              
	080398f7 40              
	080398f8 00              
	080398f9 1f              
	080398fa ff              
	080398fb 1f              
	080398fc 7f              
	080398fd 20              
	080398fe 1f              
	080398ff ff
```








