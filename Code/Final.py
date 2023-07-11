import re
from netmiko import ConnectHandler
from ipaddress import IPv4Interface, IPv4Address


def configure_interfaces(net_connect, neighbours):
    for neighbour in neighbours:
        ip_address = IPv4Address(neighbour[0])
        interface = neighbour[1]
        interface = interface.strip(',')

        new_IP = ip_address + 1
        subnet_mask = '255.255.255.0'

        config_commands = [
            f'interface {interface}',
            f'ip address {new_IP} {subnet_mask}',
            'no shutdown',
        ]
        output = net_connect.send_config_set(config_commands)
        print(output)

        print(f"interface {interface}", f"ip address {new_IP} 255.255.255.0")


def configure_dhcp(net_connect, DHCP_ip, deviceIP):
    dhcp_config_commands = [
        'ip dhcp pool LAN',
        f'network {DHCP_ip} 255.255.255.0',
        f'default-router {deviceIP}',  # Default gateway
        'exit',
        f'ip dhcp excluded-address {deviceIP}',  # Exclude the router IP from the DHCP pool
    ]
    output = net_connect.send_config_set(dhcp_config_commands)
    print(output)


def configure_ospf(net_connect):
    ospf_config_commands = [
        'router ospf 1',
        'network 0.0.0.0 255.255.255.255 area 0',  # Advertise all connected networks to area 0
        'exit',
    ]
    output = net_connect.send_config_set(ospf_config_commands)
    print(output)

def configure_vlan(net_connect):
    VLAN_config_commands = [
        'interface FastEthernet0/1.10',
        'encapsulation dot1Q 10',
        'description admin VLAN',
        'ip address 192.168.10.1 255.255.255.0',
        'exit',
        'interface FastEthernet0/1.20',
        'description CS VLAN',
        'encapsulation dot1Q 20',
        'ip address 192.168.20.1 255.255.255.0',
        'exit',
    ]
    output = net_connect.send_config_set(VLAN_config_commands)
    print(output)


def configure_access_lists(net_connect):
    acl_config_commands = [
        "access-list 101 permit icmp any any",  # allow ICMP    
        "access-list 101 permit tcp any any eq 22", # allow SSH (port 22)
        "access-list 101 deny ip any any",  # block everything else
    ]
    output = net_connect.send_config_set(acl_config_commands)
    print(output)



# Get the device information
device_ip = input("Enter device IP address: ")
username = input("Enter username: ")
password = input("Enter password: ")
configure_dhcp_option = input("Do you want to configure DHCP? (y/n): ")

device = {
    'device_type': 'cisco_ios',
    'ip': device_ip,
    'username': username,
    'password': password,
}

# Connect to the device
net_connect = ConnectHandler(**device)

# Run the "show cdp neighbors" command
output = net_connect.send_command('show cdp neighbors detail')

# Extract the IP addresses and interfaces from the output
neighbours = re.findall(r"IP address: (\d+\.\d+\.\d+\.\d+).*?Interface: (\S+)", output, re.DOTALL)
print(neighbours)

octets = device_ip.split('.')
octets[-1] = '0'
DHCP_ip = '.'.join(octets)

# Configure the interfaces, DHCP, VLAN, and OSPF
configure_interfaces(net_connect, neighbours)
if configure_dhcp_option.lower() == 'y':
    configure_dhcp(net_connect, DHCP_ip, device_ip)
configure_ospf(net_connect)
configure_vlan(net_connect)
configure_access_lists(net_connect)


# Disconnect from the device
net_connect.disconnect()