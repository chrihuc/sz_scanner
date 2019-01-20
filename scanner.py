import os
from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM, gethostname
import threading
from threading import Timer
from datetime import date
import time
from time import localtime,strftime
import subprocess

import paho.mqtt.client as mqtt
import constants
import json

PORT_NUMBER = 5010
SIZE = 1024
hostName = gethostbyname( '')#gethostname() )
mySocket = socket( AF_INET, SOCK_DGRAM )
mySocket.bind( (hostName, PORT_NUMBER) )

scanner = subprocess.Popen(["/usr/bin/scanimage", "--list-devices"], stdout=subprocess.PIPE).communicate()[0]
scanner = str(scanner)[8:30]

while os.system("sudo mount -a") <> 0:
    time.sleep(10)

print scanner

print os.system("sudo systemctl start saned.socket")

scan_folder = ["Arzt/", "Bank/", "Wohnung/", "Arbeit/", "KFZ/", "Reisen/", "Shopping/", "sonstiges/", "Schule/", "Dokumente/", "Verwaltung/", "Archive/"]

def check_folder(location):
    if not os.path.exists(location):
        os.makedirs(location)
        os.chmod(location, 0777)

def scan(folder, color=True, mail=False, adress="", druck=False):
    zeit =  time.time()
    filent = "~/" + str(strftime("%Y-%m-%d-%H-%M-%S",localtime(zeit))) +".tif"
    if isinstance(folder, (int, long)):
        filenp = "~/MIsc/Autoscan/" + scan_folder[folder] + str(strftime("%Y-%m-%d-%H-%M-%S",localtime(zeit))) +".jpg"
    else:
        path = "/home/pi/MIsc/Autoscan/" + folder + "/"
        check_folder(path)
        filenp = path + str(strftime("%Y-%m-%d-%H-%M-%S",localtime(zeit))) +".jpg"
    if color:
        exectext = "scanimage -d '"+ scanner +"' --format=tiff --resolution 300dpi --mode Color 2>&1 > " + filent
    else:
        exectext = "scanimage -d '"+ scanner +"' --format=tiff --resolution 300dpi 2>&1 > " + filent
#    print exectext
    os.system(exectext)
    #exectext = "tiff2pdf -z -j " + filent + " -o " + filenp
    exectext = "convert " + filent + " " + filenp
#    print exectext
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


mqtt.Client.connected_flag=False
client = None
topics = ["Command/" + constants.name + "/#"]
ipaddress = constants.mqtt_.server
port = 1883

def connect(ipaddress, port):
    global client
    zeit =  time.time()
    uhr = str(strftime("%Y-%m-%d %H:%M:%S",localtime(zeit)))
    client = mqtt.Client(constants.name +'_scan_' + uhr, clean_session=False)
    assign_handlers(on_connect, dis_con, on_message)
    client.username_pw_set(username=constants.mqtt_.user,password=constants.mqtt_.password)
    client.connect(ipaddress, port, 60)
#    client.loop_start()
    client.loop_forever()

def assign_handlers(connect, disconnect, message):
    """
    :param mqtt.Client client:
    :param connect:
    :param message:
    :return:
    """

    global client
    client.on_connect = connect
    client.on_disconnect = disconnect
    client.on_message = message

def dis_con (*args, **kargs):
    print("disconnected")

def on_connect(client_data, userdata, flags, rc):
    global client, topics
    if rc==0 and not client.connected_flag:
        client.connected_flag=True #set flag
        print("connected OK")
        for topic in topics:
            client.subscribe(topic)
    elif client.connected_flag:
        pass
    else:
        print("Bad connection Returned code=",rc)

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    retained = msg.retain
    message = str(msg.payload.decode("utf-8"))
    try:
        m_in=(json.loads(message)) #decode json data
        print(m_in)
        if m_in['Name'] == "STOP" and not retained:
            os.system("sudo killall python")
            #pass
        elif 'Device' in m_in.keys():
#           TODO threaded commands and stop if new comes in
            if (m_in.get('Device')=='Vm1ZIM1SCA1DO01'):
                data = m_in.get('Name')
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
                else:
                    scan(data)
    except:
        pass


while constants.run:
    time.sleep(10)
