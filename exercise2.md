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

1. 
<img width="1340" height="722" alt="image" src="https://github.com/user-attachments/assets/6e873574-d533-441b-ba0b-2e2f26ff52ab" />



5. <img width="1228" height="715" alt="image" src="https://github.com/user-attachments/assets/67dd4b50-a8ee-4064-a181-86b5cfb92471" />
<img width="418" height="303" alt="image" src="https://github.com/user-attachments/assets/a85733d1-0b0e-4684-b701-f2f794d4de52" />
Hint: <img width="766" height="561" alt="image" src="https://github.com/user-attachments/assets/f8defaf1-57a5-42b2-b994-f6f8b7c7464a" />

6. <img width="756" height="568" alt="image" src="https://github.com/user-attachments/assets/c0b51b8b-bac9-458f-9bc7-f14c067bd0b9" />
<img width="399" height="183" alt="image" src="https://github.com/user-attachments/assets/d5bc5907-f7a5-4630-996a-c4e28e69a5ea" />

7. <img width="1173" height="150" alt="image" src="https://github.com/user-attachments/assets/c771ef50-a748-44ae-8c33-258a8da03b82" />

8. <img width="776" height="617" alt="image" src="https://github.com/user-attachments/assets/5d26a0b9-5815-494c-b574-ed9e0d2c20a2" />
Answer: <img width="451" height="260" alt="image" src="https://github.com/user-attachments/assets/271fc480-15bf-440d-9b36-19855985f3dc" />


10. <img width="576" height="516" alt="image" src="https://github.com/user-attachments/assets/507dbe00-9923-465c-b05e-6809c2c5b04e" />
<img width="652" height="149" alt="image" src="https://github.com/user-attachments/assets/0f586351-6fe3-4321-912b-ebfd6da85247" />


11. 










