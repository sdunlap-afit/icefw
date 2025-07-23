# CubeSpace Reaction Wheel

## .CS Header



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
5. Once Ghidra is started click on the file tab in the top left and then click import file. Navigate to the location of your control_program_copy.cs and add it to Ghidra.

   <img width="611" height="515" alt="image" src="https://github.com/user-attachments/assets/e0521068-e23c-4815-bc36-5eef08c63c82" />

7. On the resulting window click on the three dots located to the right of the lnaguage box.
   <img width="663" height="346" alt="image" src="https://github.com/user-attachments/assets/e456fc8b-87b5-4685-8196-ad021d692d1f" />
8. What compiler have we identified the binary to be compiled by? What Endian? Use filter to narrow/search results.
   <details closed>
   <summary>Answer</summary>
   <br>
   <img width="546" height="377" alt="image" src="https://github.com/user-attachments/assets/be796647-9323-402a-a15e-a92e04c00d3c" />
   </details>
9. Select the options button in the bottom right of the window after you have selected the correct language.
   <img width="533" height="297" alt="image" src="https://github.com/user-attachments/assets/c03c44dc-7536-4ecb-a4eb-c525fa3d362d" />
10. What are we inspecting? What's the base address? Ho much space does the header take up? How long is the resulting program(Ghidra will give you this)?
   <details closed>
   <summary>Answer</summary>
   <br>
   <img width="548" height="422" alt="image" src="https://github.com/user-attachments/assets/d25c14f1-4076-4788-b331-2189884d1cd3" />
   </details>
11. Clcik Okay/Accept on all the resulting prompts then double click on your uploaded file. Click YES on the prompt asking if you want to analyze now and YES on the list options that it provides.
### Now we want to add parts of the program that we don't have to the memory map.
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
   
7. Fill in the details and click add for each section you would like to add to the Memory Map. If you had a file you wanted to add you would select File Bytes at the bottom and navigate to the file you would like to include in that space in memory(Useful to add bootloader or other sections fo code).
    <img width="488" height="381" alt="image" src="https://github.com/user-attachments/assets/6f6524f1-00c7-49ea-9f40-db7c050957c5" />
   
8. Select the Alaysis tab at the top and select Analyze All Open, click Accept/YES on the following prompts to analyze your code with this new memory addition.
    <img width="1222" height="360" alt="image" src="https://github.com/user-attachments/assets/aa975df7-e737-4464-8d7a-948129c7da94" />
9. <b>Congratualtions now you can begin Reverse Engineering the Firmware!!</b>
</details>


   


## Reverse Engineering

