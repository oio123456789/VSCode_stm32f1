

import subprocess
import os
import sys
import string

if __name__ == '__main__':

    if(len(sys.argv) > 1):
        #path = sys.argv[1]
        os.chdir(sys.argv[1])
    else:
        exit()
    # for i in range(0, len(sys.argv)):
        #print(" "+sys.argv[i]+"\r\n")
    subprocess.run(
        "openocd.exe -f settings/stlink-v2.cfg -f settings/stm32f1x.cfg", shell=True)
    exit()
