import socket
import argparse
import time
import math


# Step 3.3: Continuing the program
# function was used to make the code faster
def STEP_3():
    # declaration of global variables to be used in this function
    global payload_size, remaining_size, TimeoutInterval, payload, remaining_packets, start_time, run, SampleRTT
    global last_accepted_payload_size, time_taken, limitation, time_elapsed, original, sent_packets
    global EstimatedRTT, DevRTT, TimeoutInterval, SampleRTT
    # checking if the length of sent packets is less than the original packet length
    while sent_packets <= original:


        # separating the contents -> list format
        separated_payload = payload[sent_packets: sent_packets + int(payload_size)]
        # sequence_number = SNXXXXXXX
        # always starts at 0
        sequence_number = str(run)
        # checking if last payload
        if sent_packets + payload_size >= original:
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
        data_packet = intent_message + "SN" + sequence_number.zfill(7) + trasaction_ID + "LAST" + transmission_number + separated_payload
        # encoding the data packet
        data_packet = data_packet.encode() 
        print(data_packet)
        # using the intent message from 2.1 send data to address
        sock.sendto(data_packet, (args.IP_address, args.port_receiver))

        # run when socket does NOT time out
        try:
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

            # 3.1   RTT Estimation
            # run RTT estimation

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

            # timeout interval will be used in settimeout for each packet
            if TimeoutInterval != 0:
                sock.settimeout(math.ceil(TimeoutInterval))
                

            # for each successful upload run is incremented
            run += 1
            # updating the total of send packets
            sent_packets = sent_packets + payload_size
            # setting the last_accepted_payload_size to the payload_size
            last_accepted_payload_size = payload_size


            # 3.2   Parameter Estimation
            # time spent since the start of initiation
            time_elapsed = time.time() - start_time
            # time left to send the remaining payload
            rem_time = target_time - time_elapsed
            # compute for the remaining data to be sent
            rem_data = original - sent_packets
            # divide the data into packets
            rem_packets = math.ceil(rem_data / payload_size)
            # compute for the estimate time it will take
            time_taken = time_elapsed + (rem_packets * TimeoutInterval)
            # divide the data into packets
            rem_packets = math.floor(rem_time / TimeoutInterval)
            # chceking if it will exceed the target time of 95s
            # if it is greater
            if time_taken > target_time:
            # checking which size is greater so that it can try to reach the target time
                payload_size = max( math.ceil(rem_data / rem_packets), last_accepted_payload_size + 1 )
                # checking if the size is greater than the limit set previously
                # if it is less
                if payload_size < limitation:
                # set the current payload size as the size
                    payload_size = payload_size 
                # if it is more
                else:
                # lessen the limit and set it to the payload size so it can reach the target time
                    payload_size = limitation - 1
            

        # when the socket time outs
        except socket.timeout:
            # remaining packets to be sent
            # remaining_packets = (95 - time_elapsed) / TimeoutInterval
            remaining_packets = math.ceil((original - sent_packets) / payload_size)
            # computing for time taken
            time_taken = (remaining_packets * TimeoutInterval) + (TimeoutInterval + time_elapsed)
            
            # getting the boundaries of the payload
            if payload_size != last_accepted_payload_size:
            # setting the uper bound to the payload size
                limitation = payload_size
            # setting the uper bound to the total payload size
            else:
                limitation = original

            # computing which payload is bigger
            # using the payload in the next run
            payload_size = max(payload_size - 1, last_accepted_payload_size)
            # repeat setep 3
            return STEP_3()



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
# timer for start of initiation
start_time = time.time()
# decode acknowledgement number
trasaction_ID = acknowledgement.decode()
print(trasaction_ID)

# 2.3   Checking if there is an existing transaction
# check if transaction ID says that there is an alive tranaction
if trasaction_ID == "Existing alive transaction":
# if there is print Existing alive transaction 
    print(trasaction_ID)
# if no live tranaction
else:
# Step 3: Sending the Payload

    # sending the Payload
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
    
    # RTT_estimation variables
    # set initial EstimatedRTT to 0
    # since no transaction/runs were made
    # computes for the EstimatedRTT
    EstimatedRTT = 0
    # set initial TimeoutInterval to 0
    # since no transaction/runs were made
    # computes for the TimeoutInterval
    TimeoutInterval = 0
    # set initial DevRTT to 0
    # since no transaction/runs were made
    # computes for the DevRTT
    DevRTT = 0
    

    # PARAMETER_estimation variables
    
    remaining_size = len(payload)
    original = len(payload)
    limitation = original
    remaining_packets = 0
    time_taken = 0
    last_accepted_payload_size = 0
    payload_size = 1
    time_elapsed = 0
    target_time = 95
    sent_packets = 0


    # STEP_3 variables
    # set run to 0
    # since no transaction/runs were made
    # computes for the total number of runs made
    run = 0
    STEP_3()
