import os
from datetime import datetime

# run tshark in the terminal
# command: python3 packet.py
# for 130 seconds and save the output to a file
def run_Wireshark_tshark():
    # set filename to the current date time
    file_name = f"{datetime.now().strftime('%H-%M-%S')}"
    # save as wireshark file
    os.system(f"touch {file_name}.pcap")
    os.system(f"chmod o=rw {file_name}.pcap")
    # run tshark for 130 seconds
    os.system(f"sudo tshark -a duration:130 -w {file_name}.pcap")

run_Wireshark_tshark()
