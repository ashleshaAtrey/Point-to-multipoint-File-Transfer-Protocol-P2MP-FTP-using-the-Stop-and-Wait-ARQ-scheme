import socket
import datetime
import time
import sys
import random

def main():
    port=int(sys.argv[1])
    filename=sys.argv[2]
    prob=float(sys.argv[3])
    preseqno='{:032b}'.format(0)
    ServHost,ServPort="localhost",port
    flag=True
    flag2=False
    
    while flag:
        fdata=""
        serv=""
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((ServHost, ServPort))
        #print "Waiting for incoming connections..."
        fdata,serv = s.recvfrom(10240)
        #print fdata
        var1=fdata[:32]
        var2="0000000000000000"        
        var3="1010101010101010"
            
        if flag2==True:
            preint=int(preseqno,2)
            ad=int(var1,2)
            if ad==preint+2:
                preint=preint+1
                preseqno='{:032b}'.format(preint)
            
        flag2=False
        #int.from_bytes(os.urandom(8), byteorder="big") / ((1 << 64) - 1)
        r = random.random()
        
        if r<=prob:     #prob p
            gh=int(var1,2)
            gh1=str(gh)
            print ("Packet loss, sequence number ="+ gh1)
            s.close()
        else:
            #print "Inside checksum"
            prein=int(preseqno,2)
            prein=prein+1
            string1='{:032b}'.format(prein)
            if var1==string1:
                a=0
                b=16
                fadd=0
                z=16
                i=""
                j=""
                while (z<=(len(fdata)-16)):
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
                fa=fdata[len(fdata)-16:len(fdata)]
                #print fa
                fa1=int(fa,2)
                fa2=fa1+fadd
                if (fa2>65535):
                                    f2='{:016b}'.format(fa2)
                                    f3=f2[1:17]
                                    f4= int(f3,2)
                                    f4=f4+1
                                    fa2=f4  
                checksum='{:016b}'.format(fa2)
                
                #print "checksum Calculated"
                #print checksum
                if checksum=="1111111111111111":
                        #print "ack sending "
                        flag2=True
                        tosend=var1+var2+var3
                        s.sendto(tosend, serv)
                        s.close()
                        data1=fdata[48:64]
                        length=int(data1,2)*8
                        data=fdata[64:(64+length)]
                        #print data
                        string_blocks = (data[i:i+8] for i in range(0, len(data), 8))
                        string = ''.join(chr(int(char, 2)) for char in string_blocks)
                        with open(filename,'a') as f:
                            f.write(string)
                            f.close()
                else:
                    badack=preseqno+var2+var3
                    s.sendto(badack,serv)
                    s.close()
                    #print int(preseqno,2)
                    #print "ACK failed"
                    
            else:
                s.close()
                #print "ACK not receive"
            
    
    
if __name__=="__main__":

    main()
