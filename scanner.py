import os
from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM, gethostname
import threading
from threading import Timer
from datetime import date
import time
from time import localtime,strftime
import subprocess

PORT_NUMBER = 5010
SIZE = 1024
hostName = gethostbyname( '')#gethostname() )
mySocket = socket( AF_INET, SOCK_DGRAM )
mySocket.bind( (hostName, PORT_NUMBER) ) 

scanner = subprocess.Popen(["/usr/bin/scanimage", "--list-devices"], stdout=subprocess.PIPE).communicate()[0]
scanner = str(scanner)[8:30]

print scanner

scan_folder = ["Arzt/", "Bank/", "Wohnung/", "Arbeit/", "KFZ/", "Reisen/", "Shopping/", "sonstiges/", "Schule/", "Dokumente/", "Verwaltung/", "Archive/"]

def scan(folder, color, mail, adress, druck):
    zeit =  time.time()
    filent = "~/" + scan_folder[folder] + str(strftime("%Y-%m-%d-%H-%M-%S",localtime(zeit))) +".tif"
    filenp = "~/MIsc/Autoscan/" + scan_folder[folder] + str(strftime("%Y-%m-%d-%H-%M-%S",localtime(zeit))) +".jpg"
    if color:
        exectext = "scanimage -d '"+ scanner +"' --format=tiff --resolution 300dpi --mode Color 2>&1 > " + filent
    else:
        exectext = "scanimage -d '"+ scanner +"' --format=tiff --resolution 300dpi 2>&1 > " + filent
    print exectext
    os.system(exectext)
    #exectext = "tiff2pdf -z -j " + filent + " -o " + filenp
    exectext = "convert " + filent + " " + filenp
    os.system(exectext)
    exectext = "rm " + filent
    os.system(exectext)
    if mail:
        time.sleep(5)
        exectext = "uuencode '"+filenp+"' 'scan.jpg' | mailx -s 'Scan' '" +  adress + "'"
        os.system(exectext)
    if druck:
        time.sleep(5)
        #lpr =  subprocess.Popen("/usr/bin/lpr", stdin=subprocess.PIPE)
        #lpr.stdin.write(filenp)  
        exectext = "cat '"+filenp+"' | lpr"
        os.system(exectext)        

while True:
        (data,addr) = mySocket.recvfrom(SIZE)
        isdict = False
        try:
            data_ev = eval(data)
            if type(data_ev) is dict:
                isdict = True
        except Exception as serr:
            isdict = False 
        if isdict:
            if (data_ev.get('Device')=='Vm1ZIM1SCA1DO01'):
                data = data_ev.get('Name')
                print data
                if (data == "scan1"):
                    scan(0,True,False, "", False)
                elif (data == "scan2"):
                    scan(1,True,False, "", False)
                elif (data == "scan3"):
                    scan(2,True,False, "", False)
                elif (data == "scan4"):
                    scan(3,True,False, "", False)
                elif (data == "scan5"):
                    scan(4,True,False, "", False)
                elif (data == "scan6"):
                    scan(5,True,False, "", False)
                elif (data == "scan7"):
                    scan(6,True,False, "", False)
                elif (data == "scan8"):
                    scan(7,True,True, "chrihuc@gmail.com", False)
                elif (data == "scan9"):
                    scan(7,True,True, "84sabina@gmail.com", False)     
                elif (data == "scan10"):
                    scan(7,False,False, "", True)   
                elif (data == "scan11"):
                    scan(7,True,False, "", True)      
                elif (data == "scan12"):
                    scan(8,True,False, "", False)
                elif (data == "scan13"):
                    scan(9,True,False, "", True)      
                elif (data == "scan14"):
                    scan(10,True,False, "", False)  
                elif (data == "scan15"):
                    scan(11,True,False, "", False)              
                elif (data == "scan16"):
                    scan(7,True,False, "", False) 
                elif (data == "scan_color"):
                    scan(7,True,False, "")      
           
