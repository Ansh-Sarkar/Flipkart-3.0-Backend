import os
from paramiko import SSHClient, AutoAddPolicy

client = SSHClient()
BASE_DIR = os.getcwd()
# client.load_host_keys("flipkart_gcloud.txt")
client.set_missing_host_key_policy(AutoAddPolicy())
client.connect('128.199.19.142', username="root", password=None, key_filename="flipkart_gcloud.txt")
stdin, stdout, stderr = client.exec_command('landscape-sysinfo')
#ip and mac info
if stdout.channel.recv_exit_status() == 0:
# note: can only use stdout.read once
    val = stdout.read().decode("utf-8")
    print(f'{val}')
    # file.write(f'{val}')
else:
    print(f'STDERR: {stderr.read().decode("utf-8")}')

stdin.close()
stdout.close()
stderr.close()
client.close()
# file.close()
