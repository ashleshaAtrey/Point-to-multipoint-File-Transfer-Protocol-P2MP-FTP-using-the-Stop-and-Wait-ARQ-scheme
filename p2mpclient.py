import socket
import threading
import shlex
import os
import platform
import datetime
import time
import sys
import errno


def main():
    global ack
    j4=0
    ack=0
    x=1
    
    port=sys.argv[-3]
    filename=sys.argv[-2]
    MSS= int(sys.argv[-1])
    nservers=[w for w in sys.argv[1:-3]]
    #print filename
    dataheader='0101010101010101'
    f = open(filename,'r') # opening for [r]eading as [b]inary
    conn=0
    flag=True
    data=""
    dif1=0
    dif=0
    while flag:
            bdata=""
            seqno='{:032b}'.format(x)
            while (len(data)!=MSS):
                hdata=f.read(1)
                if(hdata==""):
                    break   
                data=data+hdata   
            bdata=''.join('{:08b}'.format(x) for x in bytearray(data))
            if(data==""):
                flag=False
                f.close()
                with open("c3-test3",'a') as fs1:
                    fs1.write(dif+ os.linesep)
                    fs1.close()
                break
            #print bdata
            MSSheader='{:016b}'.format(MSS)
            fdata=seqno+dataheader+MSSheader+bdata
            if ((len(fdata) % 16) !=0):
                fdata=fdata+"00000000"
            if ((len(fdata) % 32) !=0):
                fdata=fdata+"0000000000000000"
            
            a=0
            b=16
            fadd=0
            z=16
            i=""
            j=""
            while (z<=(len(fdata))):
                add=0
                i=fdata[a:z]
                j=fdata[z:(z+b)]
                add=int(i,2)+int(j,2)
                e1=0
                f1=""
                fd=""
                f2=""
                f3=""
                f4=""
                if (add>65535):
                    fd='{:016b}'.format(add)
                    f1=fd[1:17]
                    e1= int(f1,2)
                    e1=e1+1
                    fadd=fadd+e1
                    if (fadd>65535):
                        f2='{:016b}'.format(fadd)
                        f3=f2[1:17]
                        f4= int(f3,2)
                        f4=f4+1
                        fadd=f4
                else:
                    fadd=fadd+add
                    if (fadd>65535):
                        f2='{:016b}'.format(fadd)
                        f3=f2[1:17]
                        f4= int(f3,2)
                        f4=f4+1
                        fadd=f4 
                a=z+b
                z=z+b+b
            #print fadd
            checksum='{:016b}'.format(fadd)
            #print checksum
            ch=0
            newstr=list(checksum)
            for ch in range(0,len(newstr)):
                if newstr[ch]=='0':
                    newstr[ch]='1'
                else:
                    newstr[ch]='0'
                ch=ch+1 
            checksum="".join(newstr)
            #print checksum
            
            datatosend=fdata+checksum
            
            sport= int(port)
            conn=conn+1
            flag4=True
            
            starts1=int(round(time.time() * 1000))
            
            for de in nservers:
                thread1=threading.Thread(target=rdtsend, args=(datatosend,de,sport,))
                thread1.daemon=True
                thread1.start()
            
            while (flag4):
                    #print 'inside'
                    if(conn==ack):
                        flag4=False
                        #print ack
            
            if (not thread1.isAlive()):
                stops1=int(round(time.time() * 1000))
                diff=stops1-starts1
                dif1=diff+dif1
                dif=str(dif1)
               
            data=""
            cdata=""
            x=x+1
       
    
    
def rdtsend(datatosend,sip,sport):
    flag5=True
    while flag5:
        flag6=True
        while flag6:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            global ack
            y=""
            i=0
            j=0
            icount=0
            #print datatosend
            s.sendto(datatosend,(sip,sport))
            #print "Data sent"
            seq=datatosend[0:32]
            seqint=int(seq,2)
            #print seqint
            while(True):
                try:
                    s.settimeout(0.1) 
                    y,ser=s.recvfrom(64)
                    #print "Waiting for timeout"
                    if y!="":
                        break
                except socket.timeout:
                    print (" Timeout Received, Sequence Number: "+ str(seqint)) 
                    break
     
            if y !="":  
                if y[0:32]==seq:
                    if y[32:48]=='0000000000000000':
                        if y[48:64]=='1010101010101010':
                            ack=ack+1
                            #print "ack received" 
                            flag2=True
                            s.close()
                            return
            
                else:
                    h1=int(seq,2)
                    h2=int(y[0:32],2)
                    if (h2==(h1-1)):
                        #print "prev ACK  received"
                        if y[32:48]=='0000000000000000':
                            if y[48:64]=='1010101010101010':
                                s.close()
                                break
                                
                    else:
                        s.close()
                        #print "Rare case ACK received but not current nor previous"
                        break
            else:
                s.close()
                #print "ACK not received timeout"
                break
                    
    


if __name__=="__main__":

    main()
