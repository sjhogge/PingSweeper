import os
import platform
import logging
import threading
import time
import concurrent.futures
import sys
import argparse

from datetime import datetime
from getIP import get_ip_address
from getIP import validate_ip

def ping_addr(net2, ip, ping1):
    addr = net2 + str(ip)
    comm = ping1 + addr
    response = os.popen(comm)
    # print('Scanning: ' + addr)
   
    for line in response.readlines():
        if (line.count("TTL=")):
           print(addr, "--> Live")

def main():

    parser = argparse.ArgumentParser(description='This ping sweeper will give you the option to ping a range of IP addresses on the subnet you choose.')
    parser.add_argument('new_ip', action='store')
    parser.add_argument('-a', action='store_true', default=False, dest='sweep_all', help='Sweep the whole subnet')


    current_addr = get_ip_address()
    print("It looks like your current address is: ", current_addr)
    new_addr = input("Would you like to use the subnet of your current address?(y/n)   ")

    if (new_addr == "y") or (new_addr == "Y"):
        net = current_addr
    else:    
        net = input("Enter a Network Address on the Subnet you want to scan: ")
        if not validate_ip(net):
            raise Exception('{} is not a valid IP address'.format(net))
        
    net1= net.split('.')
    a = '.'

    net2 = net1[0] + a + net1[1] + a + net1[2] + a

    #use a try to check if they are ints, also check the bounds of the start and final number
    
    ping_all = input("Would you like to sweep the whole subnet?(y/n)   ")

    if (ping_all == "y") or (ping_all == "Y"):
        st1 = 0
        en1 = 255
    else:
        st1 = int(input("Enter the Starting Number: "))
        en1 = int(input("Enter the Last Number: "))

    if en1 > 255:
        en1 = 255
    if st1 > en1:
        st1 = en1

    oper = platform.system()

    if (oper == "Windows"):
        ping1 = "ping -n 1 "
    elif (oper == "Linux"):
        ping1 = "ping -c 1 "
    else :
        ping1 = "ping -c 1 "
    
   
    start_IP = net2 + str(st1)
    stop_IP = net2 + str(en1)
    print ("----- Scanning From", start_IP, "To", stop_IP, "-----")

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,datefmt="%H:%M:%S")

    ip_range = range(st1,en1)

    t1 = datetime.now()

    with concurrent.futures.ThreadPoolExecutor(max_workers=256) as executor:
        futures = [executor.submit(ping_addr,net2,ip,ping1)
                  for ip in ip_range]

    t2 = datetime.now()
    total = t2 - t1
    print ("Scanning completed in: ",total)
        
if __name__ == "__main__":

    main()