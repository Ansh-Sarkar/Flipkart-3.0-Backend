import os
import time
import local_storage
from paramiko import SSHClient, AutoAddPolicy
import one_pass_parser as opp
from signal import signal, SIGINT
from pythonping import ping
from datetime import datetime


BASE_DIR = os.getcwd()
EMPTY_CACHE = False
LOCAL_CACHE = {}
CHANGE_IN_LOCAL_VARIABLES = False
LOCAL_VARS = local_storage.get_local_variables()
REWRITE_LOCAL_CACHE = False


def print_dictionary(d):
    for key in d.keys():
        print("{key} : {value}".format(key=key, value=d[key]))


def handler(signal_received, frame):
    print('\n\nSIGINT or CTRL-C detected . . . ')
    print('Performing cleanup . . . ')
    update_local_cache(LOCAL_CACHE, REWRITE_LOCAL_CACHE)
    print(terminal_print(LOCAL_VARS['DESIGN'], ''))
    print(terminal_print(LOCAL_VARS['DESIGN'],
                         '< / Embrace Client Interface >'))
    print(terminal_print(LOCAL_VARS['DESIGN'], ''))
    exit(0)


def update_local_cache(LOCAL_CACHE, REWRITE_LOCAL_CACHE):
    if REWRITE_LOCAL_CACHE:
        file = open("auth_hosts.abx", "w")
        for host in LOCAL_CACHE:
            file.write("{ip} : {username} : {password} : {keyfile} : {verified}\n".format(
                ip=host, username=LOCAL_CACHE[host][0], password=LOCAL_CACHE[host][1], keyfile=LOCAL_CACHE[host][2], verified=LOCAL_CACHE[host][3]))
        REWRITE_LOCAL_CACHE = False
        file.close()
    return 'updated'


def auth_host_loader(LOCAL_CACHE, EMPTY_CACHE):
    file = open("auth_hosts.abx", "r")
    hosts = file.readlines()
    file.close()
    if(len(hosts) == 1 and hosts[0] == ""):
        EMPTY_CACHE = True
        return
    for host in hosts:
        host = host.split(":")
        if len(host) != 5:
            print("Error in auth_hosts file . . .")
            return "Manipulation of auth_hosts file detected"
        else:
            LOCAL_CACHE[host[0].strip()] = [host[1].strip()] + \
                [host[2].strip()] + [host[3].strip()] + [host[4].strip()]
    return LOCAL_CACHE


def register_new_host_for_monitoring(LOCAL_CACHE, EMPTY_CACHE):
    print("IP Address of System : ", end='')
    ip_address = input()
    if ip_address in LOCAL_CACHE.keys():
        print('Warning duplicate host found . . . aborting new registration')
        return

    print("\nBASE : {base_dir}\n".format(base_dir=BASE_DIR.replace('\\', '/')))
    os.system('ssh-keygen -P "" -t rsa -b 4096 -f {base_dir}/keys/{ip} -m pem'.format(
        ip=ip_address.replace('.', '_'), base_dir=BASE_DIR.replace('\\', '/')))
    # os.system('ssh-keygen -f {base_dir}/keys/{ip}.pub -m pem -e > {base_dir}/keys/{ip}.pem'.format(ip=ip_address.replace('.','_'),base_dir=BASE_DIR.replace('\\','/')))
    # os.system('ssh-keygen -f C:/Users/KIIT/Desktop/Team-DAB-Flipkart-3.0-Binit/Team-DAB-Flipkart-3.0-Binit/keys/{ip} -t rsa -b 4096 -m pem'.)
    file = open("{base_dir}/keys/{filename}".format(
        filename=ip_address.replace('.', '_'), base_dir=BASE_DIR.replace('\\', '/')))
    privateKey = ''.join(file.readlines())
    file.close()
    print("\nYour public key has been stored at : \n{localurl}".format(
        localurl="{base_dir}/keys/{ip}\n").format(ip=ip_address.replace('.', '_'), base_dir=BASE_DIR.replace('\\', '/')))
    print("!! Setup this key on your server for key based authentication !!\n")
    print(privateKey)
    print("----------------- Password and Username Setup -----------------\n")
    username = "root"
    password = "password"
    print("Username ( Default = root ) : ", end='')
    username = input()
    print("Password ( Default = None ) : ", end='')
    password = input()
    file = open("auth_hosts.abx", "a")
    file.write("{ip} : {user} : {pwd} : {keyfile} : False\n".format(
        ip=ip_address, user=username, pwd=password, keyfile=ip_address.replace('.', '_')))
    file.close()
    print("\nNew host and authentication added successfully .")
    print("Syncing local cache . . . ")
    LOCAL_CACHE = {}
    LOCAL_CACHE = auth_host_loader(LOCAL_CACHE, EMPTY_CACHE)
    EMPTY_CACHE = False
    print_dictionary(LOCAL_CACHE)
    return True


def terminal_print(design, message):
    terminal = os.get_terminal_size()
    columns = terminal.columns
    rows = terminal.lines
    padding = int((columns-2)/2)-int(len(message)/2)
    if len(message) % 2 == 0:
        return design*padding + ' ' + message + ' ' + design*padding
    else:
        return design*padding + ' ' + message + ' ' + design*(padding-1)


def get_total_info(LOCAL_CACHE, host):
    file = open('total_info.abx', 'w')
    count = 0
    print("Hard Syncing Local Cache . . .")
    LOCAL_CACHE = auth_host_loader(LOCAL_CACHE, EMPTY_CACHE)
    print("LOCAL_CACHE == NULL ? ", EMPTY_CACHE)
    print("\n")

    username = LOCAL_CACHE[host][0]
    if LOCAL_CACHE[host][1] == '':
        password = None
    else:
        password = LOCAL_CACHE[host][1]
    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy())
    try:
        # establishing connection with remote machine
        client.connect(host, username=username, password=password, key_filename="{base_dir}/keys/{ip}".format(
            ip=host.replace('.', '_'), base_dir=BASE_DIR.replace('\\', '/')))

        stdin, stdout, stderr = client.exec_command('ifconfig')

        #ip and mac info
        if stdout.channel.recv_exit_status() == 0:
            # note: can only use stdout.read once
            val = stdout.read().decode("utf-8")
            print(f'ip and mac info: {val}')
            file.write(f'ip and mac info: \n {val}')
        else:
            print(f'STDERR: {stderr.read().decode("utf-8")}')

        #hostname
        stdin, stdout, stderr = client.exec_command('hostname')

        if stdout.channel.recv_exit_status() == 0:
            # note: can only use stdout.read once
            val = stdout.read().decode("utf-8")
            print(f'hostinfo: {val}')
            file.write(f'hostname: {val}')
        else:
            print(f'STDERR: {stderr.read().decode("utf-8")}')

        #os information
        stdin, stdout, stderr = client.exec_command('uname -o')

        if stdout.channel.recv_exit_status() == 0:
            # note: can only use stdout.read once
            val = stdout.read().decode("utf-8")
            print(f'OS info: {val}')
            file.write(f'OS info: {val}')
        else:
            print(f'STDERR: {stderr.read().decode("utf-8")}')

        #last seen
        stdin, stdout, stderr = client.exec_command(f'lastlog -u {username}')

        if stdout.channel.recv_exit_status() == 0:
            # note: can only use stdout.read once
            val = stdout.read().decode("utf-8")
            print(f'last seen: {val}')
            file.write(f'last seen: \n {val}')
        else:
            print(f'STDERR: {stderr.read().decode("utf-8")}')

        #memory information
        stdin, stdout, stderr = client.exec_command('free -m')

        if stdout.channel.recv_exit_status() == 0:
            # note: can only use stdout.read once
            val = stdout.read().decode("utf-8")
            print(f'memory: {val}')
            file.write(f'memory: \n {val}')
        else:
            print(f'STDERR: {stderr.read().decode("utf-8")}')

        #hardware information
        #note - requires sudo thus added password may need to be provided
        stdin, stdout, stderr = client.exec_command('sudo lshw')

        if stdout.channel.recv_exit_status() == 0:
            # note: can only use stdout.read once
            val = stdout.read().decode("utf-8")
            print(f'hardware info {val}')
            file.write(f'hardware info \n {val}')
        else:
            print(f'STDERR: {stderr.read().decode("utf-8")}')

        stdin, stdout, stderr = client.exec_command('groups')

        if stdout.channel.recv_exit_status() == 0:
            # note: can only use stdout.read once
            val = stdout.read().decode("utf-8")
            print(f'groups:\n{val}')
            file.write(f'groups:\n{val}')
        else:
            print(f'STDERR: {stderr.read().decode("utf-8")}')

        stdin, stdout, stderr = client.exec_command(
            "LANG=C ip link show | awk '/link\/ether/ {print $2}'")

        if stdout.channel.recv_exit_status() == 0:
            # note: can only use stdout.read once
            val = stdout.read().decode("utf-8")
            print(f'mac addresses:\n{val}')
            file.write(f'mac addresses:\n{val}')
        else:
            print(f'STDERR: {stderr.read().decode("utf-8")}')

        # more commands here for retrieving data
        stdin.close()
        stdout.close()
        stderr.close()
        client.close()
        file.close()
        return True
    except :
        return False


def average_ping(host):
    response_list = ping(host, size=100, count=5)
    return response_list.rtt_min_ms, response_list.rtt_avg_ms, response_list.rtt_max_ms


def time_series_info(LOCAL_CACHE):
    print("Hard Syncing Local Cache . . .")
    LOCAL_CACHE = auth_host_loader(LOCAL_CACHE, EMPTY_CACHE)
    print("LOCAL_CACHE == NULL ? ", EMPTY_CACHE)
    print("\n")
    frozen_time = time.time()
    frozen_timestamp = 'T'.join(str(datetime.fromtimestamp(
        int(frozen_time))).split()).replace(':', '_')
    while(EMPTY_CACHE == False):
        for host in LOCAL_CACHE.keys():
            file = open('{host}.abx'.format(host=host.replace('.', '_')), 'w')

            time.sleep(int(LOCAL_VARS['pingInterval']))
            username = LOCAL_CACHE[host][0]
            password = LOCAL_CACHE[host][1]
            client = SSHClient()
            client.set_missing_host_key_policy(AutoAddPolicy())
            
            # connect to remote machine
            client.connect(host, username=username, password=password, key_filename="{base_dir}/keys/{ip}".format(
                ip=host.replace('.', '_'), base_dir=BASE_DIR.replace('\\', '/')))

            stdin, stdout, stderr = client.exec_command('landscape-sysinfo')
            if stdout.channel.recv_exit_status() == 0:
                # note: can only use stdout.read once
                val = stdout.read().decode("utf-8")
                file.write(f'{val}')
            else:
                print(f'STDERR: {stderr.read().decode("utf-8")}')

            stdin.close()
            stdout.close()
            stderr.close()
            client.close()
            file.close()

            file = open("{host}.abx".format(host=host.replace('.', '_')), "r")
            data = file.readlines()
            file.close()
            for i in range(len(data)):
                data[i] = data[i][:-1]
            data = ' '.join((''.join(data)).split())
            data = data.split()
            d = {}
            ipv4 = []
            for i in range(len(data)):
                if data[i] == "System":
                    d['load'] = data[i+2]
                elif data[i] == "Usage":
                    d['mem_usage'] = data[i+3:i+6]
                elif data[i] == "Users":
                    d['users_logged_in'] = data[i+3]
                elif data[i] == "Processes:":
                    d['processes'] = data[i+1]
                elif data[i] == "Memory":
                    d['ram_usage'] = data[i+2]
                elif data[i] == "Swap":
                    d['swap_usage'] = data[i+2]
                elif data[i] == "IPv4" and ' '.join(data[i:i+3]) == "IPv4 address for":
                    ipv4.append((data[i+3][:-1], data[i+4]))
            d['ipv4'] = ipv4
            min_ping, avg_ping, max_ping = average_ping(host)
            try:
                os.mkdir('time')
            except:
                pass
            try:
                os.mkdir('time/{host}'.format(host=host.replace('.', '_')))
                logstash_config_injector = open('time/{host}/logstash.conf'.format(host=host.replace('.', '_')),"w")
                template = open("logstash.abx","r")
                template_data = template.readlines()
                print(template_data)
                for line in template_data:
                    path_pos = line.find('@path@')
                    index_pos = line.find('@index@')
                    if path_pos != -1:
                        line = line.replace('@path@',os.getcwd().replace('\\','/')+"/time/{host}/active.csv".format(host = host.replace('.','_')))
                    if index_pos != -1:
                        line = line.replace('@index@',host.replace('.', '_'))
                    logstash_config_injector.write(line)
                logstash_config_injector.close()
                template.close()
                print("\nYou can now , setup a logstash pipeline by typing : ")
                print("logstash -f {config_path}\n".format(config_path = (os.getcwd()+"\\time\\{host}\\logstash.conf".format(host = host.replace('.','_')))))
            except Exception as error:
                print(error)
            time_series = open('time/{host}/{epoch}.csv'.format(
                host=host.replace('.', '_'), epoch=str(frozen_timestamp)), 'a+')
            active = open('time/{host}/active.csv'.format(
                host=host.replace('.', '_'), epoch=str(frozen_timestamp)), 'a+')
            if os.stat('time/{host}/{epoch}.csv'.format(host=host.replace('.', '_'), epoch=str(frozen_timestamp))).st_size == 0:
                active.close()
                active = open('time/{host}/active.csv'.format(
                    host=host.replace('.', '_'), epoch=str(frozen_timestamp)), 'w')
                time_series.write(
                    "epoch,load,active_users,mem_usage,total_memory,swap_usage,ram_usage,processes,min_ping,average_ping,max_ping\n")
                active.write(
                    "epoch,load,active_users,mem_usage,total_memory,swap_usage,ram_usage,processes,min_ping,average_ping,max_ping\n")
            time_series.write("{epoch},{load},{active_users},{mem_usage_percent},{total_memory},{swap_usage},{ram_usage},{processes},{min_ping},{average_ping},{max_ping}\n".format(
                epoch=str(int(time.time())), load=d['load'], active_users=d['users_logged_in'], mem_usage_percent=d['mem_usage'][0][:-1], total_memory=d['mem_usage'][-1], swap_usage=d['swap_usage'][:-1], ram_usage=d['ram_usage'][:-1], processes=d['processes'], min_ping=min_ping, average_ping=avg_ping, max_ping=max_ping))
            active.write("{epoch},{load},{active_users},{mem_usage_percent},{total_memory},{swap_usage},{ram_usage},{processes},{min_ping},{average_ping},{max_ping}\n".format(
                epoch=str(int(time.time())), load=d['load'], active_users=d['users_logged_in'], mem_usage_percent=d['mem_usage'][0][:-1], total_memory=d['mem_usage'][-1], swap_usage=d['swap_usage'][:-1], ram_usage=d['ram_usage'][:-1], processes=d['processes'], min_ping=min_ping, average_ping=avg_ping, max_ping=max_ping))
            time_series.close()
            active.close()
            print_dictionary(d)
            print("\n")


if __name__ == "__main__":
    print("Loading Local Cache . . . ")
    auth_host_loader(LOCAL_CACHE, EMPTY_CACHE)
    print(LOCAL_CACHE)
    time.sleep(3)
    os.system('cls||clear')
    signal(SIGINT, handler)
    print(terminal_print(LOCAL_VARS['DESIGN'], 'Nominally Started CLI'))
    username = "DEBUG CLIENT"
    print(terminal_print(LOCAL_VARS['DESIGN'], ''))
    print(terminal_print(LOCAL_VARS['DESIGN'], '< Embrace Client Interface >'))
    print(terminal_print(LOCAL_VARS['DESIGN'], ''))
    choice = ''
    # main loop
    while(choice != "exit"):
        print("\nCLI Commands : ")
        print("1. Doctor")
        print("2. Add Resource for Monitoring")
        print("3. Start Monitoring")
        print("4. Exit")
        print("")
        print("Client : > ", end='')
        choice = input()
        print("")
        print(terminal_print('=', ' < Result >'))
        print("")

        if choice == "1":
            pass
        elif choice == "2":
            register_new_host_for_monitoring(LOCAL_CACHE, EMPTY_CACHE)
        elif choice == "3":
            # start_monitoring_systems(LOCAL_CACHE)
            LOCAL_CACHE = auth_host_loader(LOCAL_CACHE, EMPTY_CACHE)
            for host in LOCAL_CACHE.keys():
                if LOCAL_CACHE[host][-1] == 'False':
                    verified = get_total_info(LOCAL_CACHE, host)
                    if not verified:
                        print("Invalid credentials for : {host}".format(host=host))
                        print("Skipped host with ip : {host}".format(host=host))
                        continue
                    LOCAL_CACHE[host][-1] = 'True'
                    REWRITE_LOCAL_CACHE = True
                    registry = open("registry.csv", "a+")

                    host_name = opp.get_hostname_data()['hostname']
                    host_os = opp.get_host_os_data()['host_os']

                    last_seen = opp.get_last_seen()
                    parsed_last_seen = ' '.join(
                        [last_seen['username'], last_seen['accessed_from_ip'], last_seen['access_timestamp']])
                    alert_last_seen_username = last_seen['username']
                    alert_last_seen_ip = last_seen['accessed_from_ip']

                    mac_address = opp.get_mac_addresses()
                    groups = opp.get_group_data()

                    raw_memory_data = opp.get_memory_data()
                    raw_system_configuration = opp.get_short_hardware_info()
                    if os.stat("registry.csv").st_size == 0:
                        registry.write("host,host_name,host_os,parsed_last_seen,alert_last_seen_username,alert_last_seen_ip,mac_address,groups,total_memory,used_memory,free_memory,shared_memory,cache_or_buffer_memory,available_memory,description,product,vendor,version,serial,width,capabilities,configuration\n")
                        
                    registry.write("{host},{host_name},{host_os},{parsed_last_seen},{alert_last_seen_username},{alert_last_seen_ip},{mac_address},{groups},{total_memory},{used_memory},{free_memory},{shared_memory},{cache_or_buffer_memory},{available_memory},{description},{product},{vendor},{version},{serial},{width},{capabilities},{configuration}\n"
                                   .format(host=host, host_name=host_name, host_os=host_os, parsed_last_seen=parsed_last_seen, alert_last_seen_username=alert_last_seen_username, alert_last_seen_ip=alert_last_seen_ip, mac_address=mac_address, groups=groups, total_memory=raw_memory_data['total_memory'], used_memory=raw_memory_data['used_memory'], free_memory=raw_memory_data['free_memory'], shared_memory=raw_memory_data['shared_memory'], cache_or_buffer_memory=raw_memory_data['cache_or_buffer_memory'], available_memory=raw_memory_data['available_memory'], description=raw_system_configuration['description'], product=raw_system_configuration['product'], vendor=raw_system_configuration['vendor'], version=raw_system_configuration['version'], serial=raw_system_configuration['serial'], width=raw_system_configuration['width'], capabilities=raw_system_configuration['capabilities'], configuration=raw_system_configuration['configuration']))
                    registry.close()
            update_local_cache(LOCAL_CACHE, REWRITE_LOCAL_CACHE)
            time_series_info(LOCAL_CACHE)
            # print(LOCAL_CACHE)

        elif choice == "exit":
            exit(0)
        else:
            print("{choice} is not a recognised embrace client command".format(
                choice=choice))

        print("")
        print(terminal_print('=', ' < / Result >'))
        print("")

    print(terminal_print(LOCAL_VARS['DESIGN'], ''))
    print(terminal_print(LOCAL_VARS['DESIGN'],
                         '< / Embrace Client Interface >'))
    print(terminal_print(LOCAL_VARS['DESIGN'], ''))
