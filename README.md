# MiniPod-for-Legacy-Devices
My final year dissertation project. Graded 78%

Abstract

The aim of this project is to develop a MiniPod, an automation tool that can automate the
configuration process for devices in networks. The MiniPod will be able to configure various network
parameters, such as setting up interfaces, configuring IPv4 addresses to interfaces, configuring DHCP,
OSPF, VLANs, and ACLs, as well as implementing security measures.
In the background section, this project will provide a detailed explanation of how networks work, the
different network protocols, and ways to make networks secure. Furthermore, this project will
discuss the existing automation technologies on the market, including ACI, NSX, Ansible, and Puppet.
The project requirements will include the types of configurations the MiniPod can automate, along
with a couple of use cases. The MiniPod's functionality will be self-evaluated, and a comparison
between the time taken for manual configuration and the time taken for the MiniPod to do the
same tasks will be examined. The evaluation will be performed using a spine and leaf 2-tier network
topology.

Summary of work

An automation MiniPod was created in Python using the NetMiko library. Configurations that were automated
include:
Assigning interfaces an IPv4 address
DHCP
OSPF routing protocol
VLANs Router-on-a-stick method
Access Lists

Project was self-evaluated. Using a 2 tier spine and leaf topology a newly added spine node would be configured.
The time for manual and the MiniPod configuration was compared.
MiniPod was significantly faster than manual configuration.
