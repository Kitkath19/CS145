import socket
import sys
import argparse
import time
import math



# Step 3.3: Continuing the program
# function was used to make the code faster
def STEP_3_3():
    global payload_size
    # separating the contents -> list format
    separated_payload = [payload[i:i+int(payload_size)] for i in range(10, len(payload), int(payload_size))]
    print(separated_payload)
    # sending of details to server
    for i in range(len(separated_payload)):
        print(separated_payload[i])
        # sequence_number = SNXXXXXXX
        # always starts at 0
        sequence_number = str(i+1)
        # checking if last payload
        if i == len(separated_payload) - 1:
            # transmission_number = LASTZ
            # 0 if not the last
            # 1 if the last
            transmission_number = "1"
        else:
            # transmission_number = LASTZ
            # 0 if not the last
            # 1 if the last
            transmission_number = "0"
        # intent_message + sequence_number + trasaction_ID + transmission_number + separated_payload
        data_packet = intent_message + "SN" + sequence_number.zfill(7) + trasaction_ID + "LAST" + transmission_number + separated_payload[i]
        # encoding the data packet
        data_packet = data_packet.encode() 
        print(data_packet)
        if sequence_number == "1":
            sock.settimeout(int(payload_size) + 1)
        try:

            # using the intent message from 2.1 send data to address
            sock.sendto(data_packet, (args.IP_address, args.port_receiver))
            # store the acknowledgement number from port
            acknowledgement_final, _ = sock.recvfrom(1024)

            acknowledgement_final = acknowledgement_final.decode()
            # print output
            print(acknowledgement_final)
        except:
            payload_size = payload_size - 10
                # repeat setep 3_3
            return STEP_3_3()




#declaration of variables that will be used throughout the code
#global filename_payload, IP_address, port_receiver, port_sender, unique_ID, trasaction_ID, intent_message


# STEP 0: Getting the Command Line Input
# angparse was used so that there can be blank parts
# blank parts will be replaced by the default value/s
# declaration of the use of parser
parser = argparse.ArgumentParser(description='Project Input Parameters.')
# adding of argument 1: -f denoting Filename of the Payload
# type is str
# default value is your_id.txt in my case your_id = 2099fba5
parser.add_argument("-f", "--filename_payload", type=str,
                    help="Filename of the Payload", default=f"2099fba5.txt")
# adding of argument 2: -a denoting IP address of the Receiver
# type is str
# default value is 10.0.7.141 (given in project specifications)                   
parser.add_argument("-a", "--IP_address", type=str,
                    help="IP address of the Receiver",  default="10.0.7.141")
# adding of argument 3: -s denoting Port number used by the receiver
# type is int
# default value is is your assigned port, in my case is 6679                    
parser.add_argument("-s", "--port_receiver", type=int,
                    help="Port number used by the receiver", default=6679)
# adding of argument 4: -c denoting Port number used by the sender
# type is int
# default value is 9000 (given in project specifications)                   
parser.add_argument("-c", "--port_sender", type=int,
                    help="Port number used by the sender", default=9000)
# adding of argument 5: -i denoting Unique ID
# type is str
# default value is your_id.txt in my case your_id = 2099fba5                    
parser.add_argument("-i", "--unique_ID", type=str,
                    help="Unique ID", default='2099fba5')
args = parser.parse_args()



# STEP 1: Dowloading Payload
# Transaction Generation/Results Server (TGRS)
# http://3.0.248.41:5000/get_data?student_id = wwwwwwww
# wwwwwww is the unique ID given in the email
# unique ID given/default: 2099fba5
# TGRS = f"http://3.0.248.41:5000/get_data?student_id={args.unique_ID}"
# note that: this is NOT needed since the payload must be uploaded before running the program
# as stated in the project specifications


# STEP 2: Initiating a Transaction
# 2.1   Intent Message IDwwwwwwww
# wwwwwwww is the unique ID given in the email
# default unique_ID = "2099fba5"
# setting up the intent message of format : ID + unique_iID
# timer for start of initiation
start_time = time.time()
# setting up the intent message of format : ID + unique_iID
intent_message = f"ID{args.unique_ID}".encode()
# 2.2   Accept Message YYYYYYY
# accept message will be printed out once it is proven 
# that there is no alive transaction after doing 2.1
# YYYYYYY is the transaction id that allows the user to check if the transmission is valid
#socket initialization
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# bind socket address to port receiver
sock.bind(('', args.port_sender))
# using the intent message from 2.1 send data to address
sock.sendto(intent_message, (args.IP_address, args.port_receiver))
# store the acknowledgement number from port
acknowledgement, __ = sock.recvfrom(1024)
# decode acknowledgement number
trasaction_ID = acknowledgement.decode()
print(trasaction_ID)



# Step 2.5: Checking if there is an existing transaction
# check if transaction ID says that there is an alive tranaction
if trasaction_ID == "Existing alive transaction":
# if there is print Existing alive transaction 
    print(trasaction_ID)
# if no live tranaction
else:
# continue on step 3
    # Step 3: Sending the Payload
    # sending the data packets
    # intent_message = IDWWWWWWWW
    # retrieve intent_message from PART 2 (un)code it
    intent_message = intent_message.decode()
    # transaction_ID = TXNYYYYYYY
    trasaction_ID = "TXN" + str(trasaction_ID) 
    # file_contents = PAYLOAD
    # open file using the path in input
    # r so that contents can be copied
    file = open(args.filename_payload, "r")
    # save file contents
    payload = str(file.read())
    print(payload)
    # STEP 3.1: Getting the rate
    # send first packet with size 10 to get rate
    # get first 10 initial letters in string
    first_packet = payload[:10]
    # send command
    # intent_message + sequence_number + trasaction_ID + transmission_number + first_packet
    data_packet = intent_message + "SN0000000" + trasaction_ID + "LAST0" + first_packet
    # encoding the data packet
    data_packet = data_packet.encode() 
    print(data_packet)
    # using the intent message from 2.1 send data to address
    sock.sendto(data_packet, (args.IP_address, args.port_receiver))
    # store the acknowledgement number from port
    acknowledgement_final, _ = sock.recvfrom(1024)
    # decode acknowledgement number
    acknowledgement_final = acknowledgement_final.decode()
    print(acknowledgement_final)
    # Step 3.2: Computing for the rate
    # timer for end of initiation -> 1st ACK printed out (part 2.2)
    end_time = time.time()
    # computing for the payload size
    payload_size = end_time - start_time 
    # time I need to use to pass all reqs
    # example time 90s
    # 90s/payload size is the rate
    payload_size = 90 / payload_size
    # getting the floor function of time
    # better to be less than more
    # if more it will not be accepted
    payload_size = math.floor(payload_size)
    print(payload_size)
    payload_size = len(payload) / payload_size
    print(payload_size)
    # Step 3.3: Continuing the program
    # separating the contents -> list format
    STEP_3_3()
