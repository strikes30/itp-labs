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
                   build=False )

    info( '*** Adding controller\n' )
    info( '*** Add switches\n')
    r1 = net.addHost('r1', cls=Node, ip=None)

    info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip=None, mac='00:00:10:00:00:64')
    h2 = net.addHost('h2', cls=Host, ip=None, mac='00:00:10:00:01:64')
    h3 = net.addHost('h3', cls=Host, ip=None, mac='00:00:10:00:02:64')

   
    info( '*** Add links\n')
    net.addLink(h1, r1)
    net.addLink(h2, r1)
    net.addLink(h3, r1)


    info( '*** Starting network\n')
    net.build()

    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    r1.intf( 'r1-eth0' ).config(mac='00:00:10:00:00:01')
    r1.intf( 'r1-eth1' ).config(mac='00:00:10:00:01:01')
    r1.intf( 'r1-eth2' ).config(mac='00:00:10:00:02:01')

    info( '*** Turn off IPv6\n')
    r1.cmd('sysctl -w net.ipv6.conf.all.disable_ipv6=1')
    r1.cmd('sysctl -w net.ipv6.conf.default.disable_ipv6=1')
    h1.cmd('sysctl -w net.ipv6.conf.all.disable_ipv6=1')
    h1.cmd('sysctl -w net.ipv6.conf.default.disable_ipv6=1')
    h2.cmd('sysctl -w net.ipv6.conf.all.disable_ipv6=1')
    h2.cmd('sysctl -w net.ipv6.conf.default.disable_ipv6=1')
    h3.cmd('sysctl -w net.ipv6.conf.all.disable_ipv6=1')
    h3.cmd('sysctl -w net.ipv6.conf.default.disable_ipv6=1')


    info( '*** Post configure switches and hosts\n')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

