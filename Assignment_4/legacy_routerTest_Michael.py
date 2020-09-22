#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

def myNetwork():    
    net = Mininet( topo=None,
                   build=False, ipBase = '192.168.1.1/24')
    
    info( '*** Adding controller\n' )
    info( '*** Add switches\n')

    r1 = net.addHost('r1',cls=Node)
    r1.cmd('sysctl -w net.ipv4.ip_forward=1')

	
    info( '*** Add hosts\n')
    h1 = net.addHost('h1', ip='192.168.1.100/24',
                           defaultRoute='via 192.168.1.1' )
    h2 = net.addHost('h2', ip='172.16.0.100/12',
                           defaultRoute='via 172.16.0.1' )

    info( '*** Add links\n')
    net.addLink(h1, r1, intfName2='eth1-r1',
                      params2={ 'ip' : '192.168.1.1/24' } )
    net.addLink(h2, r1, intfName2='eth2-r1',
                      params2={ 'ip' : '172.16.0.1/12' })

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')

    info( '*** Post configure switches and hosts\n')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()
    info( '*** Routing Table on Router:\n' )
    print net[ 'r1' ].cmd( 'route' )
