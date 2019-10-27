#!/usr/bin/python

# Testbed Lab 4
# 
# @author Andrea Mayer
#

from mininet.net import Mininet
from mininet.node import Host, Node
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink
from subprocess import call

def myNetwork():

    net = Mininet(topo=None,
                   build=False)

    info( '*** Add bridge\n')
    br = net.addHost('br', cls=Node, ip=None) #Use ip=None to turn off automatic ip assignment

    info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip=None, mac='00:00:10:00:30:01')
    h2 = net.addHost('h2', cls=Host, ip=None, mac='00:00:10:00:20:02')
    h3 = net.addHost('h3', cls=Host, ip=None, mac='00:00:10:00:10:03')

    info( '*** Add links\n')
    h1br = {'bw':1000}
    net.addLink(h1, br, cls=TCLink , **h1br)
    h2br = {'bw':1000}
    net.addLink(h2, br, cls=TCLink , **h2br)
    h3br = {'bw':1000}
    net.addLink(h3, br, cls=TCLink , **h3br)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Disable IPv6 network stack\n')

    br.cmd('sysctl -w net.ipv6.conf.all.disable_ipv6=1')
    br.cmd('sysctl -w net.ipv6.conf.default.disable_ipv6=1')
    h1.cmd('sysctl -w net.ipv6.conf.all.disable_ipv6=1')
    h1.cmd('sysctl -w net.ipv6.conf.default.disable_ipv6=1')
    h2.cmd('sysctl -w net.ipv6.conf.all.disable_ipv6=1')
    h2.cmd('sysctl -w net.ipv6.conf.default.disable_ipv6=1')
    h3.cmd('sysctl -w net.ipv6.conf.all.disable_ipv6=1')
    h3.cmd('sysctl -w net.ipv6.conf.default.disable_ipv6=1')

    # --------------------------------------------------------------
    #  Network topology
    #
    #                     h3 
    #                     10.0.10.3 VLAN 10
    #
    #                          +-----+
    #                          |     |
    #                          |     |
    #                       +-----------+
    #                       +-----------+
    #                             |
    #                             |
    #                             |
    #                             |
    #                             | br-eth2
    #                          +------+
    #         +----------------+  br  +-------------+
    #         |        br-eth0 +------+ br-eth1     |
    #         |                                     |
    #         |                                     |
    #      +--+--+                               +--+--+
    #      |     |                               |     |
    #      |     |                               |     |
    #   +-----------+                         +-----------+
    #   +-----------+                         +-----------+
    #
    #  h1                                    h2
    #  10.0.10.1 VLAN 10                     10.0.20.2 VLAN 20
    #  10.0.20.1 VLAN 20

    info( '*** Post configure bridge and hosts\n')
    
    # h1

    # h2

    # h3

    #br
    br.cmd('ip link add br0 type bridge')
    # NOTE: The software bridge has recently gained a "default_pvid" feature which 
    # makes it work like cheap hardware switches: it is vlan aware, but will per 
    # default do a pvid->vid mapping to vid 1, and will allow vid 1 on all ports, so 
    # that you can plug the switch in and start using ports for untagged traffic 
    # without a single configuration directive.
    br.cmd('echo 0 > /sys/class/net/br0/bridge/default_pvid')
    br.cmd('echo 1 > /sys/class/net/br0/bridge/vlan_filtering')
    br.cmd('ip link set br-eth0 master br0')
    br.cmd('ip link set br-eth1 master br0')
    br.cmd('ip link set br-eth2 master br0')
    br.cmd('bridge vlan add dev br-eth0 vid 10')
    br.cmd('bridge vlan add dev br-eth0 vid 20')
    br.cmd('bridge vlan add dev br-eth1 vid 20')
    br.cmd('bridge vlan add dev br-eth2 vid 10')
    br.cmd('ip link set br0 up')

    # USEFULL COMMANDS
    # 
    # (*) To set ageing time we need to issue the command: 'brctl setageing br0 10' (10 secs)
    #
    # (*) To show the mac forwarding table we need to issue the command: 
    #     watch -n 1 "bridge -statistics fdb show | grep -v 'permanent'"


    # Statistics shown by  'bridge -s fdb show', source code at: iproute2/bridge/fdb.c.
    #
    #    static void fdb_print_stats(FILE *fp, const struct nda_cacheinfo *ci)
    #  108 {
    # 			...
    #
    #  120         fprintf(fp, "used %d/%d ", ci->ndm_used / hz,
    #  121                     ci->ndm_updated / hz);
    #
    #  124 }

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

