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
import threading

style.enabled = True
cnopts = sftp.CnOpts()
cnopts.hostkeys = None


#------------------------------------------------------------------------------
        
    
servers = {
        'server0':{
                'ip':'159.65.101.168',
                'platform':'DigitalOcean'
                },
        'server1':{
                'ip':'167.99.162.43',
                'platform':'DigitalOcean'
                },
        'server2':{
                'ip':'167.99.100.11',
                'platform':'DigitalOcean'
                },
        'server3':{
                'ip':'167.99.108.24',
                'platform':'DigitalOcean'
                },
        'server4':{
                'ip':'167.99.110.121',
                'platform':'DigitalOcean'
                },
        'server5':{
                'ip':'159.89.147.221',
                'platform':'DigitalOcean'
                },
        'server6':{
                'ip':'159.89.147.195',
                'platform':'DigitalOcean'
                },
        'server7':{
                'ip':'206.189.22.57',
                'platform':'DigitalOcean'
                },
        'server8':{
                'ip':'206.189.22.59',
                'platform':'DigitalOcean'
                },
        'server9':{
                'ip':'46.101.58.236',
                'platform':'DigitalOcean'
                },
        'server10':{
                'ip':'46.101.77.22',
                'platform':'DigitalOcean'
                },
        'server11':{
                'ip':'18.236.72.99', 
                'platform':'AWS'
                },
        'server12':{
                'ip':'54.213.222.151', 
                'platform':'AWS'
                },
        'server13':{
                'ip':'35.166.218.168',
                'platform':'AWS'
                },
        'server14':{
                'ip':'54.186.161.177',
                'platform':'AWS'
                },
        'server15':{
                'ip':'54.203.23.91', 
                'platform':'AWS'
                },
        'server16':{
                'ip':'54.191.231.196',
                'platform':'AWS'
                },
        'server17':{
                'ip':'34.213.216.78',
                'platform':'AWS'
                },
        'server18':{
                'ip':'54.149.56.233',
                'platform':'AWS'
                },
        'server19':{
                'ip':'54.245.21.241',
                'platform':'AWS'
                },
        'server20':{
                'ip':'54.245.204.182', 
                'platform':'AWS'
                },
        'server21':{
                'ip':'54.214.106.194', 
                'platform':'AWS'
                },
        'server22':{
                'ip':'34.216.158.53',
                'platform':'AWS'
                },
        'server23':{
                'ip':'35.163.195.93',
                'platform':'AWS'
                },
        'server24':{
                'ip':'54.187.179.37',
                'platform':'AWS'
                },
        'server25':{
                'ip':'54.202.50.8',
                'platform':'AWS'
                },
        'server26':{
                'ip':'54.186.79.7',
                'platform':'AWS'
                },
        'server27':{
                'ip':'34.209.235.120',
                'platform':'AWS'
                },
        'server28':{
                'ip':'52.37.192.169',
                'platform':'AWS'
                },
        'server29':{
                'ip':'35.165.40.216',
                'platform':'AWS'
                },
        'server30':{
                'ip':'35.164.226.51',
                'platform':'AWS'
                }
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
    print("Moved file(s) to ",server)
    s.close()


def getFilesFromServer(server,filenames):
    privateKey = get_key(server)
    username = get_username(server)
    IP_address = get_IP(server)
    directory = get_dir(server)
    
    s = sftp.Connection(host=IP_address, username=username,
                        private_key=privateKey, cnopts=cnopts)

    for filename in filenames:
        files = s.listdir(filename)
        for file in files:
            localPath = 'raw_data/'+filename + '/' + file
            remotePath = directory + filename + '/' + file
            s.get(remotePath,localPath)
    print("Retrieved file(s) from ",server)

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
    
    print("\n\nConnecting to "+server+"...")
    c.connect(hostname = IP_address, username = username, pkey = k )
    print("Connected.\n")
    
    for command in commands:
        print("Executing", style.cyan(command))
        stdin , stdout, stderr = c.exec_command(command)
        if type(commands) == dict and commands[command]:
            for interactiveCommand in commands[command]:
                print("Entering",style.cyan(interactiveCommand))
                stdin.write(interactiveCommand)
                stdin.write('\n')
                stdin.flush()
        print("Output:",style.magenta(stdout.read().decode()))
        print("Errors:",style.red(stderr.read().decode()))
    c.close()


#------------------------------------------------------------------------------
    

def get_key(server):
    if servers[server]['platform'] == 'DigitalOcean':
        return 'C:/Users/Aaron/Desktop/Desktop stuff/SSH stuff/keyDO'
    elif servers[server]['platform'] == 'AWS':
        return 'C:/Users/Aaron/Desktop/Desktop stuff/SSH stuff/keyAWS'
    
    
def get_IP(server):
    return servers[server]['ip']


def get_username(server):
    if servers[server]['platform'] == 'DigitalOcean':
        return 'root'
    elif servers[server]['platform'] == 'AWS':
        return 'ubuntu'
    
    
def get_dir(server):
    if servers[server]['platform'] == 'AWS':
        return '/home/ubuntu/'
    else:
        return '/root/'
    

#------------------------------------------------------------------------------
        
    
def get_serverNum(server_name):
    return re.findall(r'\d+', server_name)[0]

    
def get_orderbook_collection_commands(server):
    serverNum = get_serverNum(server)
    commands = [
            #'pip3 install ccxt --upgrade',
            'nohup python3 orderbook_hdf.py '+serverNum+' > foo.out 2> foo.err < /dev/null &'
            ]
    return commands


#------------------------------------------------------------------------------
    

def set_up_one_server(server):
    files = [
            'orderbook_hdf.py',
            'initialise_exchanges.py',
            'get_trading_symbols.py',
            'setup.sh'
            ]
    serverNum = get_serverNum(server)
    commands = {'bash setup.sh':'y'}#,'mkdir orderbook'+serverNum:''}
    putFilesToServer(server,files)
    giveCommands(server,commands)
    print(server,"set up successfully.\n")


def set_up_all_servers():
    files = [
            'orderbook_hdf.py',
            'initialise_exchanges.py',
            'get_trading_symbols.py',
            'setup.sh'
            ]
    for server in servers:
        serverNum = get_serverNum(server)
        commands = {'bash setup.sh':'y'}#,'mkdir orderbook'+serverNum:''}
        putFilesToServer(server,files)
        giveCommands(server,commands)
        print(server,"set up successfully.\n")
        

#------------------------------------------------------------------------------
        
        
def run_program_on_one_servers(server):
    commands = get_orderbook_collection_commands(server)
    giveCommands(server,commands)
        
        
def run_program_on_all_servers():
    for server in servers:
        commands = get_orderbook_collection_commands(server)
        giveCommands(server,commands)
        

#------------------------------------------------------------------------------

        
def kill_python3(server):
    commands = ['sudo pkill python3']
    giveCommands(server,commands)
    
    
def kill_all_python3():
    for server in servers:
        commands = ['sudo pkill python3']
        giveCommands(server,commands)
        

#------------------------------------------------------------------------------

        
def clear_orderbook_folder(server):
    serverNum = get_serverNum(server)
    commands = ['rm -f orderbook'+str(serverNum)+'/*']
    giveCommands(server,commands)


def remove_orderbook_folder(server):
    serverNum = get_serverNum(server)
    commands = ['rm -r orderbook'+str(serverNum)+'/*']
    giveCommands(server,commands)


def clear_all_orderbook_folders():
    for server in servers:
        clear_orderbook_folder(server)
        
        
def erase_on_all_servers():
    for server in servers:
        kill_python3(server)
        clear_orderbook_folder(server)
    
        
#------------------------------------------------------------------------------


def getFilesFromAllServers():
    for server in servers:
        serverNum = get_serverNum(server)
        filename = ['orderbook'+str(serverNum)]
        getFilesFromServer(server,filename)
        
        
#------------------------------------------------------------------------------
        
        
def thread_function(func):
    threads_list = []
    for i in range(len(servers)):
        thread =  threading.Thread(target=func)
        thread.start()
        threads_list.append(thread)
    for thread in threads_list:
        thread.join()
# DON'T THINK I'LL BOTHER WITH RUNNING THE PROGRAM WITH MULTITHREADING. IT WOULD
# ENTAIL ADDING A LOCK TO A LOT OF STATEMENTS AND I'M NOT BOTHERED.

#------------------------------------------------------------------------------
        

if __name__ == '__main__':
    
    '''
    to test servers can be reached:
    '''
    #for server in servers:
    #    commands = ['\n']
    #    giveCommands(server,commands)
    
    
    '''
    to erase data currently on one server to start fresh:
    '''
    #kill_python3('server1')
    #clear_orderbook_folder('server1')
    
    
    '''
    to erase data currently on servers to start fresh:
    '''
    #erase_on_all_servers()
    
    
    
    '''
    to kill all python processes across servers:
    '''
    #kill_all_python3()
    
    #commands = ['sudo pkill python3','rm -f orderbook'+str(1)+'/*']
    #giveCommands('server1',commands)
    

    '''
    to set up one server:
    '''
    #set_up_one_server('server1')
    
    
    '''
    to set up all servers:
    '''
    #set_up_all_servers()
    

    
    '''
    to run script on a single test server:
    '''
    
    #run_program_on_one_servers('server1')
   
    #commands = ['nohup python3 orderbook_hdf.py 1 > foo.out 2> foo.err < /dev/null &']
    #giveCommands('server1',commands)


    '''
    to run orderbook collection script on all servers:
    '''
    #run_program_on_all_servers()    
    
    
    '''
    to collect orderbook folders from all servers:
    '''
    getFilesFromAllServers()
    
    
    pass
    

#------------------------------------------------------------------------------