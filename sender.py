import socket
import sys
import argparse
import time
import math


# the formula for this function was retrieved from lecture 11
def RTT_estimation():
# declaration of global variables
    global EstimatedRTT, DevRTT, TimeoutInterval, SampleRTT
    # part 1 - estimated RTT computation
    # check if this is the initial transactiom
    # if it is the initial
    if EstimatedRTT == 0:
    # set EstimatedRTT = RTT
    # the RTT was computed previously  RTT = (RTT_end_time - RTT_start_time)
        EstimatedRTT = SampleRTT
    # if it is not the initial
    else:
    # Lecture 11 page 18
    # “Average” of SampleRTT values must be taken; in TCP, this is called EstimatedRTT
    # EstimatedRTT updated for each new value of SampleRTT
        EstimatedRTT = (1 - 0.125) * EstimatedRTT + 0.125 * SampleRTT

    # part 2 - dev RTT computation
    # Lecture 11 page 19
    # DevRTT - estimate of how much SampleRTT typically varies from EstimatedRTT
    DevRTT = (1 - 0.25) * DevRTT + 0.25 * abs(SampleRTT - EstimatedRTT)

    # part 3 - rate update
    # Lecture 11 page 20
    # From the EstimatedRTT and DevRTT, the timeout interval is derived
    TimeoutInterval = EstimatedRTT + (4 * DevRTT)



def PARAMETER_estimation():
    # declaration of global variables
    global remaining_packets, time_taken, last_accepted_payload_size, payload_size, payload, limitation, remaining_size, TimeoutInterval, time_elapsed
    # timer for end of initiation -> per transaction to get time elapsed
    end_time = time.time()     
    # time elapsed
    time_elapsed = (end_time - start_time)
    # remaining packets to be sent
    # remaining_packets = (95 - time_elapsed) / TimeoutInterval
    remaining_packets = math.ceil(remaining_size / payload_size)
    if time_elapsed < target_time:
        target_time = target_time
    else:
        target_time = 120
    # computing for time taken
    time_taken = (remaining_packets * TimeoutInterval) + time_elapsed
    # remaining packets to be sent
    remaining_packets = math.floor((target_time - time_elapsed) / TimeoutInterval)
    
    if target_time < time_taken:
        payload_size = max(math.ceil(remaining_size / remaining_packets), last_accepted_payload_size + 1)

    if payload_size < limitation: 
        payload_size = payload_size
    else:
        payload_size = limitation - 1


# Step 3.3: Continuing the program
# function was used to make the code faster
# number of runs done
run = 1
def STEP_3_3():
    global payload_size, remaining_size, TimeoutInterval, payload, remaining_packets, TimeoutInterval, start_time, run, SampleRTT
    global last_accepted_payload_size, time_taken, limitation, time_elapsed
    # separating the contents -> list format
    separated_payload = [payload[i:i+int(payload_size)] for i in range(0, len(payload), int(payload_size))]
    print(separated_payload)
    # sending of details to server
    for i in range(len(separated_payload)):
        #print(separated_payload[i])
        # sequence_number = SNXXXXXXX
        # always starts at 0
        sequence_number = str(run)
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

        
        # timeout interval will be used in settimeout for each packet
        if TimeoutInterval != 0:
            sock.settimeout(math.ceil(int(TimeoutInterval)))

        try:
            # using the intent message from 2.1 send data to address
            sock.sendto(data_packet, (args.IP_address, args.port_receiver))
            # timer for start of initiation
            RTT_start_time = time.time() 
            # store the acknowledgement number from port
            acknowledgement_final, _ = sock.recvfrom(1024)
            # decode acknowledgement number
            acknowledgement_final = acknowledgement_final.decode()
            # print output
            print(acknowledgement_final)

            # timer for end of initiation -> 1st ACK printed out (part 2.2)
            RTT_end_time = time.time()
            # computing for the payload size (RTT)
            SampleRTT = (RTT_end_time - RTT_start_time)
            RTT_estimation()

            # for each successful upload run is incremented
            run += 1

            # update remaining size
            remaining_size = remaining_size - payload_size
            last_accepted_payload_size = payload_size
            # remaining packets to be sent
            payload = payload[int(payload_size):]
            # PARAMETER_estimation()
            # print(remaining_size)
            

        except socket.timeout:
            # remaining packets to be sent
            # remaining_packets = (95 - time_elapsed) / TimeoutInterval
            remaining_packets = math.ceil(remaining_size / payload_size)
            # computing for time taken
            time_taken = (remaining_packets * TimeoutInterval) + (TimeoutInterval + time_elapsed)

            if payload_size != last_accepted_payload_size: 
                limitation = payload_size
            else:
                limitation = len(payload)   

            # print(payload)
            payload_size -=1
            payload_size = max( payload_size, last_accepted_payload_size)
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
# timer for start of initiation
start_time = time.time()
# setting up the intent message of format : ID + unique_iID
intent_message = f"ID{args.unique_ID}".encode()
# 2.2   Accept Message YYYYYYY
# accept message will be printed out once it is proven 
# that there is no alive transaction after doing 2.1
# YYYYYYY is the transaction id that allows the user to check if the transmission is valid
# socket initialization
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
# continue on step 3
else:
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
    payload = payload.rstrip()
    

    # STEP 3.1: Initial Transaction
    # send first packet with size 1 to get rate
    # get first initial letter in string
    first_packet = payload[:1]
    # send command
    # intent_message + sequence_number + trasaction_ID + transmission_number + first_packet
    data_packet = intent_message + "SN0000000" + trasaction_ID + "LAST0" + first_packet
    # timer for start of initiation
    RTT_start_time = time.time()     
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


    # Step 3.2.1: Computing for the rate
    # timer for end of initiation -> 1st ACK printed out (part 2.2)
    RTT_end_time = time.time()
    # computing for the payload size (RTT)
    SampleRTT = (RTT_end_time - RTT_start_time)
    #print(RTT)
    # set initial EstimatedRTT to 0
    # since no transaction/runs were made
    EstimatedRTT = 0
    # set initial TimeoutInterval to 0
    # since no transaction/runs were made
    TimeoutInterval = 0
    # set initial DevRTT to 0
    # since no transaction/runs were made
    DevRTT = 0
    # set initial last payload size to 0
    # since no transaction/runs were made
    RTT_estimation()
    
    # Step 3.2.2: parameter estimation
    remaining_size = len(payload) - 1
    remaining_packets = 0
    time_taken = 0
    last_accepted_payload_size = 1
    payload_size = 1
    limitation = len(payload)
    time_elapsed = 0
    target_time = 95
    PARAMETER_estimation()
    # computing for the payload size
    #payload_size = math.floor(remaining_size / remaining_packets)
    # remove first packet from original payload
    payload = payload[1:]


    # Step 3.3: Continuing the program
    # separating the contents -> list format
    STEP_3_3()
