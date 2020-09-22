# CST 311
# Programming Assignment 4
# Amir-Andy Alameddine
# Michael Lee
# Ramon Lucindo
# Sergio Quiroz

#!/usr/bin/python

# import statements
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

# setup network
def myNetwork():
    #Create the Mininet
    net = Mininet(topo=None,
                  build=False, ipBase='192.168.1.1/24')

    info('*** Adding controller\n')
    info('*** Add switches\n')
    #Add the Router
    r1 = net.addHost('r1', cls=Node)
    #Enable Forwarding in the Router
    r1.cmd('sysctl -w net.ipv4.ip_forward=1')

    info('*** Add hosts\n')
    
    #Add Host 1 with IP Address 192.168.1.100/24.  
    h1 = net.addHost('h1', ip='192.168.1.100/24',
                     defaultRoute='via 192.168.1.1') #Default route is the R1 Default Interface
    #Add Host 2 with IP Address 172.16.0.100/12
    h2 = net.addHost('h2', ip='172.16.0.100/12',
                     defaultRoute='via 172.16.0.1') #Default Route is the R1 2nd interface

    info('*** Add links\n')

    #Add a link from host 1 to router 1 to the interface 
    net.addLink(h1, r1, intfName2='eth1-r1',
                params2={'ip': '192.168.1.1/24'})
    #Add a link from host 2 to router 2 to the interface
    net.addLink(h2, r1, intfName2='eth2-r1',
                params2={'ip': '172.16.0.1/12'})

    #Start the network
    info('*** Starting network\n')
    net.build()

    #Starting the Controller
    # added the following 5 lines of code:
    info('*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info('*** Starting switches\n')

    info('*** Post configure switches and hosts\n')
    #Stop the network
    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    #Runs the metho myNetwork
    myNetwork()
    # added 2 lines of code below:
    info('*** Routing Table on Router:\n')
    #Prints the routing table
    print net['r1'].cmd('route')
