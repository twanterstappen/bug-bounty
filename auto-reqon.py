#!/usr/bin/env python3.11print



from colorama import Fore, Back, Style
import sys
import os
import time
import subprocess
import traceback
import argparse
import json
import tqdm

class Config:
    def __init__(self, config_file):
        self.config_data = self.load_config(config_file)
        self.auto_save = self.config_data['Auto_save']
        
        
    def run_command(self, command, cap_output, in_shell):
        command = command.split()
        subprocess.run(command,capture_output=cap_output,check=True,shell=in_shell)
        # returncode = output.returncode
        # print(returncode)
        # use decode function to convert to string
        # print('Output:',output.stdout.decode("utf-8"))


    def load_config(self, filename):
        if os.path.isfile(filename):
            with open(filename) as f:
                config_data = json.load(f)
        else:
            print(Fore.YELLOW, 'Config file not found, refering to default config', Fore.RESET, sep='', end='')
            for i in range(4):
                print(Fore.YELLOW, '.', Fore.RESET, sep='', end='', flush=True)
                time.sleep(0.7)
            config_data = self.default_config()

        return config_data
        
    def default_config(self):
        config_data = \
        {   
            'Auto_save': True,
            'Enable tools': {
                'wilcard_subdomain': [{'subfinder' : True}, {'assetfinder' : False}, {'sublist3r' : True}, {'knockpy' : False},]
            },
        }
        return config_data
    
    def export_config(self):
        with open('config.json', 'w') as f:
            json.dump(self.config_data, f, indent=4)
        print(Fore.GREEN, 'Config file exported', Fore.RESET, sep='', end='')
        for i in range(4):
            print(Fore.GREEN, '.', Fore.RESET, sep='', end='', flush=True)
            time.sleep(0.7)


## Config Menu
# !-------------------------------------------------------------------------------------------------------------------------------------------------! #


class ConfigMenu:
    def __init__(self, config_file):
        self.config = Config(config_file)
        self.config_data = self.config.config_data
        self.auto_save = self.config.auto_save
        
    def run_command(self, command, cap_output, in_shell):
        command = command.split()
        subprocess.run(command,capture_output=cap_output,check=True,shell=in_shell)
        # returncode = output.returncode
        # print(returncode)
        # use decode function to convert to string
        # print('Output:',output.stdout.decode("utf-8"))
            
    # Config menu options
    def config_menu(self):
        self.run_command('clear -x', False, False)
        while True:
            print('\nOptions:')
            print('    [1] Enable/Disable tools')
            print('    [2] Show Enabled tools')
            print('    [3] Export configurations')
            print('    [4] Exit program')
            # Option input
            option = input('Choose an option: ')
            if option == '1':
                self.enable_disable_tools()
            elif option == '2':
                self.show_tools()
            elif option == '3':
                self.config.export_config()
            elif option == '4':
                print('Exiting program....')
                sys.exit(0)
                
    # Show enabled/disabled tools
    def show_tools(self):
        self.run_command('clear -x', False, False)
        print('\nTools enabled:')
        for tools in self.config_data['Enable tools']['wilcard_subdomain']:
            if tools[list(tools.keys())[0]] == True:
                print(Fore.GREEN, '    [-] ', list(tools.keys())[0], Fore.RESET, sep='')
            else:
                print(Fore.RED, '    [-] ', list(tools.keys())[0], Fore.RESET, sep='')

    # Enable or Disable tool
    def enable_disable_tools(self):
        while True:
            self.run_command('clear -x', False, False)
            print('Tools Enabled or Disabled:')
            count = 1
            for tools in self.config_data['Enable tools']['wilcard_subdomain']:
                if tools[list(tools.keys())[0]] == True:
                    print(Fore.GREEN, f'    {count}. [+] ', list(tools.keys())[0], Fore.RESET, sep='')
                else:
                    print(Fore.RED, f'    {count}. [-] ', list(tools.keys())[0], Fore.RESET, sep='')
                count += 1
            print(Fore.YELLOW, f'    {count}.     Exit to menu', Fore.RESET, sep='')
            
            tool_input = int(input('Choose an option: '))
            if tool_input not in list(range(1, count+1)):
                print(Fore.RED, f'You need to enter a option from 1-{count}', Fore.RESET, sep='')
            elif tool_input == count:
                print('Exiting current menu....')
                break
            else:
                condition = f'{Fore.RED}disable{Fore.RESET}' if list(self.config_data['Enable tools']['wilcard_subdomain'][int(tool_input)-1].values())[0] else f'{Fore.GREEN}enable{Fore.RESET}'
                tool = list(self.config_data['Enable tools']['wilcard_subdomain'][int(tool_input-1)].keys())[0]
                validate = input(f'Are you sure you want to {condition} {Fore.YELLOW}{tool}{Fore.RESET} y/n: ')
                
                if validate.lower() not in ['y', 'n']:
                    print(Fore.RED, 'Invalid! ', 'Enter y or n', Fore.RESET, sep='')
                    
                elif validate.lower() == 'y':
                    self.config_data['Enable tools']['wilcard_subdomain'][int(tool_input-1)][tool] = False if self.config_data['Enable tools']['wilcard_subdomain'][int(tool_input-1)][tool] else True
                    condition_print = 'Enabling' if condition == 'enable' else 'Disabling'
                    print(Fore.YELLOW, f'{condition_print} {tool}', Fore.RESET, sep='', end='', flush=True)
                    for i in range(4):
                        print(Fore.YELLOW, '.', Fore.RESET, sep='', end='', flush=True)
                        time.sleep(0.4)
                    print('\nSaving config', sep='', flush=True)
                    self.config.export_config()
                        
                elif validate.lower() == 'n':
                    print(Fore.YELLOW, 'Skipping', Fore.RESET, sep='', end='', flush=True)
                    for i in range(4):
                        print(Fore.YELLOW, '.', Fore.RESET, sep='', end='', flush=True)
                        time.sleep(0.4)
            time.sleep(1)
            

# !-------------------------------------------------------------------------------------------------------------------------------------------------! #
    

def main():
    start = time.time()
    

    ascii_text = f"""   
   ,---,                           ,----..                              
  '  .' \                         /   /   \                             
 /  ;    '.              ,--,    /   .     :       ,---.         ,---,  
:  :       \           ,'_ /|   .   /   ;.  \     '   ,'\    ,-+-. /  | 
:  |   /\   \     .--. |  | :  .   ;   /  ` ;    /   /   |  ,--.'|'   | 
|  :  ' ;.   :  ,'_ /| :  . |  ;   |  ; \ ; |   .   ; ,. : |   |  ,"' | 
|  |  ;/  \   \ |  ' | |  . .  |   :  | ; | '   '   | |: : |   | /  | | 
'  :  | \  \ ,' |  | ' |  | |  .   |  ' ' ' :   '   | .; : |   | |  | | 
|  |  '  '--'   :  | : ;  ; |  '   ;  \; /  |   |   :    | |   | |  |/  
|  :  :         '  :  `--'   \  \   \  ',  . \   \   \  /  |   | |--'   
|  | ,'         :  ,      .-./   ;   :      ; |   `----'   |   |/       
`--''            `--`----'        \   \ .'`--"             '---'        
                                   `---`"""
    temp = ''
    count = 0

    print(ascii_text)
    print(f"Author:   {Back.BLACK}Twan Terstappen{Back.RESET}")
    print(f"Date:     {Back.BLACK}2024-03-28{Back.RESET}")
    print(f"Version:  {Back.BLACK}1.0{Back.RESET}\n\n")
    
    time.sleep(2)

                
            

    

    
    
    # Setting the arguments
    parser = argparse.ArgumentParser(description='Bug Bounty scanner')
    config_group = parser.add_mutually_exclusive_group(required=True)
    config_group.add_argument('-D', '--domain', dest='domainname', nargs='?', const=True, type=str, help='Domain name for scanning')
    config_group.add_argument('-F', '--file', dest='filename', nargs='?', const=True, type=str, help='File with multiple domains')
    config_group.add_argument('-CC', '--change-config', dest='changeconfig', action='store_true', help='Change configuration')
    # parser.add_argument('-C', '--connections', dest='connections', action='store_true', help='Displaying connections in dataset, has to be json')
    parser.add_argument('-CF', '--config-file', dest='configfile', nargs='?', const=True, type=str, help='Load config file')
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
    
    

    
    if args.configfile:
        config_file = args.configfile
    else:
        config_file = 'config.json'
    analyzer = ConfigMenu(config_file)
    analyzer.config_menu()
        
    input('Press enter to exit')




            
    end = time.time()
    # print(f"\nRuntime of the program: {(end - start):.2f} seconds")
    
if __name__ == '__main__':
    main()