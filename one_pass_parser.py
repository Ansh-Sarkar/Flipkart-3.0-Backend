from contextlib import suppress

def get_purified_log(metrics):
    for i in range(len(metrics)):
        metrics[i] = metrics[i].strip()
        if metrics[i] == "":
            continue
    return metrics

def get_group_data():
    file = open("total_info.abx", "r")
    metrics = file.readlines()
    file.close()
    metrics = get_purified_log(metrics)
    group_data = {'available': False, 'groups': []}
    for i in range(len(metrics)):
        if metrics[i] == "groups:" and group_data['available'] == False:
            group_data['available'] = True
            i += 1
            while(i < len(metrics) and metrics[i].find(":") == -1):
                group_data['groups'].append(metrics[i])
                i += 1
    return ' '.join(group_data['groups'])

def get_mac_addresses():
    file = open("total_info.abx", "r")
    metrics = file.readlines()
    file.close()
    metrics = get_purified_log(metrics)
    mac_address_data = {'available': False, 'mac_addresses': []}
    for i in range(len(metrics)):
        if metrics[i] == "mac addresses:" and mac_address_data['available'] == False:
            mac_address_data['available'] = True
            i += 1
            while(i < len(metrics) and len(metrics[i].split(":")) == 6):
                mac_address_data['mac_addresses'].append(metrics[i])
                i += 1
    return ' '.join(mac_address_data['mac_addresses'])

def get_host_os_data():
    file = open("total_info.abx", "r")
    metrics = file.readlines()
    file.close()
    metrics = get_purified_log(metrics)
    host_os_data = {'available': False, 'host_os': ''}
    for i in range(len(metrics)):
        if metrics[i].find("OS info") != -1:
            host_os_data['available'] = True
            temp_split = metrics[i].split(":")
            temp_pure = []
            for i in temp_split:
                temp_pure.append(i.strip())
                with suppress(BaseException):
                    host_os_data['host_os'] = temp_pure[1]
    return host_os_data

def get_hostname_data():
    file = open("total_info.abx", "r")
    metrics = file.readlines()
    file.close()
    metrics = get_purified_log(metrics)
    hostname_data = {'available': False, 'hostname': ''}
    for i in range(len(metrics)):
        if metrics[i].find("hostname") != -1:
            hostname_data['available'] = True
            temp_split = metrics[i].split(":")
            temp_pure = []
            for i in temp_split:
                temp_pure.append(i.strip())
            with suppress(BaseException):
                hostname_data['hostname'] = temp_pure[1]
    return hostname_data

def get_last_seen():
    file = open("total_info.abx", "r")
    metrics = file.readlines()
    file.close()
    metrics = get_purified_log(metrics)
    last_seen_data = {'available': False, 'username': '',
                      'accessed_via_port': '', 'accessed_from_ip': '', 'access_timestamp': ''}
    for i in range(len(metrics)):
        if metrics[i] == "last seen:" and last_seen_data['available'] == False:
            last_seen_data['available'] = True
            i += 2
            temp_split = metrics[i].split(" ")
            temp_pure = []
            for token in temp_split:
                if token == '':
                    continue
                temp_pure.append(token)
            with suppress(BaseException):
                last_seen_data['username'] = temp_pure[0]
            with suppress(BaseException):
                last_seen_data['accessed_via_port'] = temp_pure[1]
            with suppress(BaseException):
                last_seen_data['accessed_from_ip'] = temp_pure[2]
            with suppress(BaseException):
                last_seen_data['access_timestamp'] = ' '.join(temp_pure[3:])
    return last_seen_data

def get_memory_data():
    file = open("total_info.abx", "r")
    metrics = file.readlines()
    file.close()
    metrics = get_purified_log(metrics)
    memory_data = {'available': False, 'total_memory': '', 'used_memory': '', 'free_memory': '',
                   'shared_memory': '', 'cache_or_buffer_memory': '', 'available_memory': ''}
    for i in range(len(metrics)):
        if metrics[i] == "memory:" and memory_data['available'] == False:
            memory_data['available'] = True
            i += 2
            with suppress(BaseException):
                temp_split = ''.join(metrics[i].split(":")[1:])
            temp_split = temp_split.split(" ")
            temp_pure = []
            for token in temp_split:
                if token == '':
                    continue
                temp_pure.append(token)
            with suppress(BaseException):
                memory_data['total_memory'] = temp_pure[0]
            with suppress(BaseException):
                memory_data['used_memory'] = temp_pure[1]
            with suppress(BaseException):
                memory_data['free_memory'] = temp_pure[2]
            with suppress(BaseException):
                memory_data['shared_memory'] = temp_pure[3]
            with suppress(BaseException):
                memory_data['cache_or_buffer_memory'] = temp_pure[4]
            with suppress(BaseException):
                memory_data['available_memory'] = temp_pure[5]
    return memory_data

def get_super_parsed_data():
    file = open("total_info.abx", "r")
    metrics = file.readlines()
    file.close()
    metrics = get_purified_log(metrics)
    super_parsed_data = {'available': False}
    temp = {}
    for i in range(len(metrics)):
        if metrics[i][:2] == "*-":
            super_parsed_data['available'] = True
            with suppress(BaseException):
                property_name = metrics[i][2:]
            i += 1
            while(i < len(metrics) and metrics[i].find(":") != -1):
                temp_data = metrics[i].split(":")
                with suppress(BaseException):
                    sub_prop, sub_prop_data = temp_data[0], ''.join(
                        temp_data[1:]).strip()
                temp[sub_prop] = sub_prop_data
                i += 1
            super_parsed_data[property_name] = temp
            temp = {}
    return super_parsed_data

def get_short_hardware_info():
    file = open("total_info.abx", "r")
    metrics = file.readlines()
    file.close()
    metrics = get_purified_log(metrics)
    
    short_hardware_data = {'available': False, 'description': '', 'product':'' , 'vendor':'' , 'version':'' , 'serial':'' , 'width' : '' , 'capabilities':'' , 'configuration':''}
    
    for i in range(len(metrics)):
        if metrics[i] == "hardware info" and short_hardware_data['available'] == False:
            short_hardware_data['available'] = True
            i += 1
            short_hardware_data['host_computer_name'] = metrics[i]
            i += 1
            while(i < len(metrics) and metrics[i].find(":") != -1):
                temp_data = metrics[i].split(":")
                with suppress(BaseException):
                    sub_prop, sub_prop_data = temp_data[0], ''.join(
                        temp_data[1:]).strip()
                print(sub_prop)
                if sub_prop not in short_hardware_data.keys() or sub_prop == "available":
                    i += 1
                    continue
                print("yesh")
                short_hardware_data[sub_prop] = sub_prop_data
                i += 1
    return short_hardware_data

def get_ip_and_mac_data():
    file = open("total_info.abx", "r")
    metrics = file.readlines()
    file.close()
    metrics = get_purified_log(metrics)
    ip_and_mac_data = {'available': False}
    for i in range(len(metrics)):
        if metrics[i] == "ip and mac info:" and ip_and_mac_data['available'] == False:
            ip_and_mac_data['available'] = True
            with suppress(BaseException):
                mtu_loc = metrics[i+1].find('mtu')
            if mtu_loc != -1:
                with suppress(BaseException):
                    mtu = metrics[i+1][mtu_loc:].split(" ")[1]
            with suppress(BaseException):
                inet = metrics[i+2].split(" ")
            with suppress(BaseException):
                inet6 = metrics[i+3].split(" ")
            temp_inet = []
            temp_inet6 = []
            for token in inet:
                if token == '':
                    continue
                temp_inet.append(token)
            for token in inet6:
                if token == '':
                    continue
                temp_inet6.append(token)
            inet = temp_inet
            inet6 = temp_inet6
            with suppress(BaseException):
                ip_and_mac_data['inet'] = inet[1]
            with suppress(BaseException):
                ip_and_mac_data['netmask'] = inet[3]
            with suppress(BaseException):
                ip_and_mac_data['broadcast'] = inet[5]
            with suppress(BaseException):
                ip_and_mac_data['inet6'] = inet6[1]
            with suppress(BaseException):
                ip_and_mac_data['prefixlen'] = inet6[3]
            with suppress(BaseException):
                ip_and_mac_data['scopeid'] = inet6[5]
    return ip_and_mac_data

def experimental_init(last_seen_data):
    with suppress(BaseException):
        metrics = get_purified_log(metrics)
    with suppress(BaseException):
        last_seen_data = get_last_seen(metrics, last_seen_data)
    with suppress(BaseException):
        host_os_data = get_host_os_data(metrics, host_os_data)
    with suppress(BaseException):
        hostname_data = get_hostname_data(metrics, hostname_data)
    with suppress(BaseException):
        memory_data = get_memory_data(metrics, memory_data)
    with suppress(BaseException):
        super_parsed_data = get_super_parsed_data(metrics, super_parsed_data)
    with suppress(BaseException):
        short_hardware_data = get_short_hardware_info(
            metrics, short_hardware_data)
    with suppress(BaseException):
        ip_and_mac_data = get_ip_and_mac_data(metrics, ip_and_mac_data)
    with suppress(BaseException):
        group_data = get_group_data(metrics, group_data)
    with suppress(BaseException):
        mac_address_data = get_mac_addresses(metrics, mac_address_data)

print(get_short_hardware_info())