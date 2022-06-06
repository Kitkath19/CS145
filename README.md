# CS145 Project 1
This project was made by Kathryn Cantor from Lab-2 of CS145 A.Y.2021-2022B.
The program created is an implementation of the sender side of a protocol. The network protocol 
used in tis project is a pipelined protocol built on top of UDP. The goal is for the payload of
the sender to reach the receiver of the test server. The program is created in Python 3.


# Level of implementation: 4


# Files Included
- sender.py - sender code to be used throughout the project
  - command: python3 sender.py -f /home/ubuntu/CS145/2099fba5.txt -a 10.0.7.141 -s 9000 -c 6679 -i 2099fba5 
- packet_tracing.py - Wireshark/Tshark tracefile generator used in the project
  - command: python3 packet_tracing.py
  
  
# Project Implementation

1. Open 2 (two) terminals
  - Terminal A: running the sender code
  - Terminal B: running the packet tracing code (wireshark/tshark)
2. Connect to the AWS serve
  - SSH in the terminal using the command: ssh -i "<key>" ubuntu@<PUBLIC IP address>
  - in my case it is: ssh -i "kdlc.pem" ubuntu@<PUBLIC IP address>
3. Connect to GitHub
  - once connected always do a "git pull" to update the files in the current directory
4. Download the Payload
  - for each run a new payload must be generated
  - link: http://3.0.248.41:5000/get_data?student_id=2099fba5
5. Update the 2099fba5.txt file in GitHub
  - once updated type in "git pull" in one of the terminals
  - you are ready to implement the project
(6) Send in the command to Terminal B first, make sure you do this first
  - command: python3 packet_tracing.py
(7) Once, tracefile is being generated, Send in the command to Terminal A
  - command: python3 sender.py -f /home/ubuntu/CS145/2099fba5.txt -a 10.0.7.141 -s 9000 -c 6679 -i 2099fba5 
          -f    filename of the payload
          -a    IP address of the receiver
          -s    port used by the receiver
          -c    port used by the sender
          -i    unique ID
(8) After a few minutes (approx.80-95 seconds) the program will end.
  - check http://3.0.248.41:5000/transactions is the transaction ID is present and it was a successful
  - tracefile will be placed in the current directory
(9) "git push" so that you can access the tracefile
(10) for additional experiments, go back to step 3

  

# Links
  documentation video: 
