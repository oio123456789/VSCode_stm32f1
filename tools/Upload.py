
import subprocess
import os
import sys
import string

if __name__ == '__main__':

    if(len(sys.argv) > 2):
        #path = sys.argv[1]
        os.chdir(sys.argv[1])
        path = sys.argv[2]
    else:
        exit()

    command = "ST-LINK_CLI.exe -P "
    command += path
    command += " -V -Rst"
    # print(command)
    subprocess.run(command, shell=True)
    exit()
