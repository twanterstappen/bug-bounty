#!/usr/bin/env python3.11



import sys
import os
import time
import subprocess
import traceback
from colorama import Fore
import argparse
import json

class ReqonTool:
    def __init__(self):
        self.config_data = self.load_config()



    def run_command(self, command, cap_output, in_shell):
        command = command.split()
        subprocess.run(command,capture_output=cap_output,check=True,shell=in_shell)
        # returncode = output.returncode
        # print(returncode)
        # use decode function to convert to string
        # print('Output:',output.stdout.decode("utf-8"))


    def load_config(self):
        with open('config.json') as f:
            CONFIG_DATA = json.load(f)
        return CONFIG_DATA
        
    def write_config(self):
        config_data = \
        {   
            'Enable tools': {
                'wilcard_subdomain': [{'subfinder' : True}, {'assetfinder' : False}, {'sublist3r' : True}, {'knockpy' : False},],
            },
        }
        with open('config.json', 'w', encoding='utf-8') as config_file:
            json.dump(config_data, config_file, indent=4)
            
    ## Config Menu
    # !-------------------------------------------------------------------------------------------------------------------------------------------------! #
    # Config menu options
    def config_menu(self):
        self.run_command('clear -x', False, False)
        while True:
            print('\nOptions:')
            print('    [1] Enable/Disable tools')
            print('    [2] Show Enabled tools')
            print('    [3] Export/Import configuration')
            print('    [4] Exit program')
            # Option input
            option = input('Choose an option: ')
            if option == '1':
                self.enable_disable_tools()
            elif option == '2':
                self.show_tools()
            elif option == '3':
                self.export_import_config()
            elif option == '4':
                print('Exiting program....')
                sys.exit(0)
                
    # Show enabled/disabled tools
    def show_tools(self):
        self.run_command('clear -x', False, False)
        output = self.load_config()
        print('\nTools enabled:')
        for tools in output['Enable tools']['wilcard_subdomain']:
            if tools[list(tools.keys())[0]] == True:
                print(Fore.GREEN, '    [-] ', list(tools.keys())[0], Fore.RESET, sep='')
            else:
                print(Fore.RED, '    [-] ', list(tools.keys())[0], Fore.RESET, sep='')

    # Enable or Disable tool
    def enable_disable_tools(self):
        while True:
            self.run_command('clear -x', False, False)
            output = self.load_config()
            print('Tools enabled:')
            count = 1
            for tools in output['Enable tools']['wilcard_subdomain']:
                if tools[list(tools.keys())[0]] == True:
                    print(Fore.GREEN, f'    [{count}] ', list(tools.keys())[0], Fore.RESET, sep='')
                else:
                    print(Fore.RED, f'    [{count}] ', list(tools.keys())[0], Fore.RESET, sep='')
                count += 1
            print(Fore.YELLOW, '    [5] Exit program', Fore.RESET, sep='')
            
            tool_input = input('Choose an option: ')          
            if tool_input not in ['1', '2', '3', '4', '5']:
                print(Fore.RED, 'You need to enter a option from 1-5', Fore.RESET, sep='')
            elif tool_input == '5':
                print('Exiting current menu....')
                break
            else:
                condition = 'enable' if list(self.config_data['Enable tools']['wilcard_subdomain'][int(tool_input)].values())[0] else 'disable'
                tool = list(self.config_data['Enable tools']['wilcard_subdomain'][int(tool_input)].keys())[0]
                validate = input(f'Are you sure you want {condition} to {tool} y/n: ')
                
                if validate.lower() not in ['y', 'n']:
                    print(Fore.RED, 'Invalid! ', Fore.RESET, 'Enter y or n', sep='')
                    
                elif validate.lower() == 'y':
                    condition_print = 'Enabling' if condition == 'enable' else 'Disabling'
                    print(f'{condition_print} {tool}....')
                elif validate.lower() == 'n':
                    print('skipping....')
            time.sleep(1.5)
    # !-------------------------------------------------------------------------------------------------------------------------------------------------! #
        
        



        

        
        

        print('\nDo you want to enable or disable a tool?')

def main():
    start = time.time()
    
    # Setting the arguments
    parser = argparse.ArgumentParser(description='Bug Bounty scanner')
    config_group = parser.add_mutually_exclusive_group(required=True)
    config_group.add_argument('-D', '--domain', dest='domainname', nargs='?', const=True, type=str, help='Domain name for scanning')
    config_group.add_argument('-F', '--file', dest='filename', nargs='?', const=True, type=str, help='File with multiple domains')
    config_group.add_argument('-C', '--config', dest='config', action='store_true', help='Use a configuration file')
    # parser.add_argument('-C', '--connections', dest='connections', action='store_true', help='Displaying connections in dataset, has to be json')
    parser.add_argument('-V', '--verbose', dest='verbose', action='store_true', help='Verbose output')
    parser.add_argument('--debug', dest='debug', action='store_true', help='Debug output')
    args = parser.parse_args()
    
    args.domainname
    args.filename
    args.verbose
    VERBOSE_ERROR = args.debug
    
    
    
    ## Check operating system
    # !-------------------------------------------------------------------------------------------------------------------------------------------------! #
    # check if Windows
    if sys.platform == 'win32':
        command = 'cmd /c ver'
        try:
            o = subprocess.run(command,capture_output=True,check=True,shell=True)
        except subprocess.CalledProcessError as e:
            if VERBOSE_ERROR:
                traceback.print_exc()
            else:
                print(e)
            exit(1)
        print('Not available for Windows')
        exit(1)
            
    # Check if Linux
    elif sys.platform == 'linux' or sys.platform == 'linux2':
        command = 'hostnamectl'
        try:
            o = subprocess.run(command,capture_output=True,check=True,shell=True)
        except subprocess.CalledProcessError as e:
            if VERBOSE_ERROR:
                traceback.print_exc()
            else:
                print(e)
            exit(1)
    
    # Check if MacOS
    elif sys.platform == 'darwin':
        # Not tested for MacOS
        print('Not tested for MacOS')
        command = 'hostnamectl'
        try:
            o = subprocess.run(command,capture_output=True,check=True,shell=True)
        except subprocess.CalledProcessError as e:
            if VERBOSE_ERROR:
                traceback.print_exc()
            else:
                print(e)
            exit(1)
    # !----------------------------------------------------------------------------------------! #
    
    

    
    
    analyzer = ReqonTool()
    analyzer.config_menu()
        
    input('Press enter to exit')




            
    end = time.time()
    # print(f"\nRuntime of the program: {(end - start):.2f} seconds")
    
if __name__ == '__main__':
    main()