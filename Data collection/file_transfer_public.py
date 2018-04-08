# -*- coding: utf-8 -*-
"""
Created on Sat Apr  7 17:35:42 2018

@author: Aaron
"""


#------------------------------------------------------------------------------


import pysftp as sftp
import paramiko
import style
import re

style.enabled = True
cnopts = sftp.CnOpts()
cnopts.hostkeys = None


#------------------------------------------------------------------------------
        
    
servers = {
        'server0':{
                'ip':'',
                'platform':''
                },
        'server1':{
                'ip':'',
                'platform':''
                },
        'server2':{
                'ip':'',
                'platform':''
                },
        'server3':{
                'ip':'',
                'platform':''
                },
        'server4':{
                'ip':'',
                'platform':''
                },
        'server5':{
                'ip':'',
                'platform':''
                },
        'server6':{
                'ip':'',
                'platform':''
                },
        'server7':{
                'ip':'',
                'platform':''
                },
        'server8':{
                'ip':'',
                'platform':''
                },
        'server9':{
                'ip':'',
                'platform':''
                },
        'server10':{
                'ip':'',
                'platform':''
                },
        'server11':{
                'ip':'',
                'platform':''
                },
        'server12':{
                'ip':'',
                'platform':''
                },
        'server13':{
                'ip':'',
                'platform':''
                },
        'server14':{
                'ip':'',
                'platform':''
                },
        'server15':{
                'ip':'',
                'platform':''
                },
        'server16':{
                'ip':'',
                'platform':''
                },
        'server17':{
                'ip':'',
                'platform':''
                },
        'server18':{
                'ip':'',
                'platform':''
                },
        'server19':{
                'ip':'',
                'platform':''
                },
        'server20':{
                'ip':'',
                'platform':''
                },
        
        # Etc...
        
        }


#------------------------------------------------------------------------------


def putFilesToServer(server,filenames):
    privateKey = get_key(server)
    username = get_username(server)
    IP_address = get_IP(server)
    directory = get_dir(server)
    
    s = sftp.Connection(host=IP_address, username=username,
                        private_key=privateKey, cnopts=cnopts)
    
    for filename in filenames:
        remotePath = directory + filename
        localPath = filename
        s.put(localPath,remotePath)
    s.close()


def getFilesFromServer(server,filenames):
    privateKey = get_key(server)
    username = get_username(server)
    IP_address = get_IP(server)
    directory = get_dir(server)
    
    s = sftp.Connection(host=IP_address, username=username,
                        private_key=privateKey, cnopts=cnopts)
    
    for filename in filenames:
        remotePath = directory + filename
        localPath = filename
        s.get(remotePath,localPath)
    s.close()
    
    
#------------------------------------------------------------------------------
    
def giveCommands(server,commands):
    '''
    The parameter "commands" is either a dictionary or a list. It contains 
    commands to be passed through to the command line. If interactive commands
    are required, it is a dictionary, with each key command having its own 
    interactive commands, e.g. when a [Y/N] is prompted. When interactive 
    commands are not used, a list of commands is passed instead.
    '''
    
    privateKey = get_key(server)
    username = get_username(server)
    IP_address = get_IP(server)
    
    k = paramiko.RSAKey.from_private_key_file(privateKey)
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    print("Connecting...")
    c.connect(hostname = IP_address, username = username, pkey = k )
    print("Connected.\n")
    
    for command in commands:
        print("Executing", style.cyan(command))
        stdin , stdout, stderr = c.exec_command(command)
        if type(commands) == dict and commands[command]:
            for interactiveCommand in commands[command]:
                print(interactiveCommand)
                stdin.write(interactiveCommand)
                stdin.write('\n')
                stdin.flush()
        if 'nohup' in command.split():
            c.close()
            print("Closed.")
        else:
            print("Output:",style.magenta(stdout.read().decode()))
            print("Errors:",style.red(stderr.read().decode()))
            c.close()


#------------------------------------------------------------------------------
    

def get_key(server):
    if servers[server]['platform'] == 'DigitalOcean':
        return 'PATH_TO_DIGITAL_OCEAN_KEY'
    elif servers[server]['platform'] == 'AWS':
        return 'PATH_TO_AWS_KEY'
    
    
def get_IP(server):
    return servers[server]['ip']


def get_username(server):
    if servers[server]['platform'] == 'DigitalOcean':
        return 'DIGITAL_OCEAN_USERNAME'
    elif server['platform'] == 'AWS':
        return 'AWS_USERNAME'
    
    
def get_dir(server):
    if servers[server]['platform'] == 'AWS':
        return 'AWS_WORKING_DIRECTORY'
    else:
        return 'DIGITAL_OCEAN_WORKING_DIRECTORY'
    

#------------------------------------------------------------------------------
        
    
def get_serverNum(server_name):
    return re.findall(r'\d+', server_name)[0]

    
def get_orderbook_collection_commands(server):
    serverNum = get_serverNum(server)
    commands = [
            'pip3 install ccxt --upgrade',
            'nohup python3 orderbook_hdf.py '+serverNum+' &'
            ]
    return commands


#------------------------------------------------------------------------------
    

def set_up_all_servers():
    commands = {'bash setup.sh':'y'}
    files = [
            'orderbook_hdf.py',
            'initialise_exchanges.py',
            'get_trading_symbols.py',
            'setup.sh'
            ]
    for server in servers:
        putFilesToServer(server,files)
        giveCommands(server,commands)
        print(server,"set up successfully.")
        
        
def run_program_on_all_servers():
    for server in servers:
        commands = get_orderbook_collection_commands(server)
        giveCommands(server,commands)
        
        
#------------------------------------------------------------------------------
        

if __name__ == '__main__':
    set_up_all_servers()
    run_program_on_all_servers()
    

#------------------------------------------------------------------------------