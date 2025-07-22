# CubeSpace Reaction Wheel

## .CS Header



## Ghidra Set-Up
Requirments: Install Ghidra if it isn't already on your machine, then install prefered Hex editor. I will be using ImHEX.
1. Ghidra Windows: [https://github.com/NationalSecurityAgency/ghidra/releases]. Linux: [snap install ghidra]
2. ImHEX [https://imhex.werwolv.net/]

Set-Up
1. First rename the Reaction Wheel Firmware to control_program.cs and make a copy called control_program_copy.cs
2. Once you have Ghidra installed open it via the terminal by typing ```ghidra``` or the windows run script in the unzipped file.
   <img width="680" height="462" alt="image" src="https://github.com/user-attachments/assets/d39750fc-1508-4805-b085-6aa038377e7b" />
3. Once Ghidra is started click on the file tab in the top left and then click import file. Navigate to the location of your control_program_copy.cs and add it to Ghidra.
4. On the resulting window click on the three dots located to the right of the lnaguage box.
   <img width="663" height="346" alt="image" src="https://github.com/user-attachments/assets/e456fc8b-87b5-4685-8196-ad021d692d1f" />
5. What compiler have we identified the binary to be compiled by? What Endian? Use filter to narrow/search results.
   <details closed>
   <summary>Answer</summary>
   <br>
   <img width="546" height="377" alt="image" src="https://github.com/user-attachments/assets/be796647-9323-402a-a15e-a92e04c00d3c" />
   </details>
6. Select the options button in the bottom right of the windo after you have selected the correct language.
   <img width="533" height="297" alt="image" src="https://github.com/user-attachments/assets/c03c44dc-7536-4ecb-a4eb-c525fa3d362d" />
7. What are we inspecting? What's the base address? Ho much space does the header take up? How long is the resulting program(Ghidra will give you this)?
   <details closed>
   <summary>Answer</summary>
   <br>
   <img width="548" height="422" alt="image" src="https://github.com/user-attachments/assets/d25c14f1-4076-4788-b331-2189884d1cd3" />
   </details>


   


## Reverse Engineering

