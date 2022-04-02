# ip and mac info
'ifconfig'
# hostname
'hostname'
# os info
'uname -o'
# last seen logs
'lastlog -u {username}'
# memory information
'free -m'
# hardware information
'sudo lshw'
# security groups and active directories
'groups'
# list of all mac addresses
"'LANG=C ip link show | awk '/link\/ether/ {print $2}'"