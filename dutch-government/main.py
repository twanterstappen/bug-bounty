#!/usr/bin/env python3.11



import sys
import os
import time
import subprocess
import traceback

VERBOSE = False

def command():
    command = 'cls'.split()
    output = subprocess.run(command,capture_output=True,check=True,shell=True)
    returncode = output.returncode
    print(returncode)
    # use decode function to convert to string
    print('Output:',output.stdout.decode("utf-8"))


def main():
    if sys.platform == 'win32':
        command = 'cls'
        try:
            subprocess.run(command,check=True,shell=True)
        except subprocess.CalledProcessError as e:
            if VERBOSE:
                traceback.print_exc()
            else:
                print(e)
            exit(1)
    elif sys.platform == 'linux' or sys.platform == 'linux2':
        command = 'clear'
        try:
            subprocess.run(command,check=True,shell=True)
        except subprocess.CalledProcessError as e:
            if VERBOSE:
                traceback.print_exc()
            else:
                print(e)
            exit(1)
            
        
        
        
        # subprocess.call(['echo', 'sadf'], shell=True) 
        
        # try:
        #     if os.system('cls') != 0:
        #         print('test')
        #     # subprocess.run(['cls'], check=False)
        # except:
        #     print('test')
            
            
            
    
if __name__ == '__main__':
    main()