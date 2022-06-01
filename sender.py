import socket
import sys
import argparse
import time
import math

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

'''
print(args.payload)
print(args.IP_address)
print(args.port_receiver)
print(args.port_sender)
print(args.id)
'''

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
# timer for end of initiation -> ACK printed out
end_time = time.time()


# Step 3: Sending the Payload
# computing for the payload size
payload_size = 10
# getting the floor function of time
# better to be less than more
# if more it will not be accepted
payload_size = math.floor(payload_size)
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
# separating the contents -> list format
separated_payload = [payload[i:i+payload_size] for i in range(0, len(payload), payload_size)]
# sending of details to server
for i in range(len(separated_payload)):
    # sequence_number = SNXXXXXXX
    # always starts at 0
    sequence_number = str(i)
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
    # using the intent message from 2.1 send data to address
    sock.sendto(data_packet, (args.IP_address, args.port_receiver))
    # store the acknowledgement number from port
    acknowledgement_final, _ = sock.recvfrom(1024)
    # decode acknowledgement number
    acknowledgement_final = acknowledgement_final.decode()
    print(acknowledgement_final)
