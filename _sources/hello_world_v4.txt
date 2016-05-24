============
HelloWord V4
============


Explanations
============

In this part, we will connect many machines using Janitoo.
Ideally you need another raspberry :D. But you can also use :

- a computer with Ubuntu or Debian
- install another server on the same raspberry
- or using a docker image


Mosquitto
=========

We need to check that mosquitto is accessible from the network. You can do it manually or install the janitoo package.
It will also install a more recent version of mosquitto (from the developpers site).

At first, remove the old package :

.. code:: bash

    sudo apt-get purge -y mosquitto

And install the new one :

.. code:: bash

    cd /opt/janitoo/src
    sudo make clone module=janitoo_mosquitto

After a while you should see something like :

.. code:: bash

    netcat -zv 127.0.0.1 1-9999 2>&1|grep succeeded
    Connection to 127.0.0.1 21 port [tcp/ftp] succeeded!
    Connection to 127.0.0.1 22 port [tcp/ssh] succeeded!
    Connection to 127.0.0.1 139 port [tcp/netbios-ssn] succeeded!
    Connection to 127.0.0.1 445 port [tcp/microsoft-ds] succeeded!

    Dependencies for janitoo_mosquitto finished.
    make[1]: Leaving directory '/opt/janitoo/src/janitoo_mosquitto'

Launch the tests :

.. code:: bash

    cd janitoo_mosquitto
    sudo make tests

They should be like :

.. code:: bash

    netcat -zv 127.0.0.1 1-9999 2>&1|grep succeeded
    Connection to 127.0.0.1 21 port [tcp/ftp] succeeded!
    Connection to 127.0.0.1 22 port [tcp/ssh] succeeded!
    Connection to 127.0.0.1 139 port [tcp/netbios-ssn] succeeded!
    Connection to 127.0.0.1 445 port [tcp/microsoft-ds] succeeded!
    Connection to 127.0.0.1 1883 port [tcp/*] succeeded!
    #~ #No websocket for precise
    #~ netcat -zv 127.0.0.1 1-9999 2>&1|grep succeeded|grep 9001
    /usr/local/bin/nosetests --verbosity=2 tests
    test_001_connect_to_server (tests.test_docker.TestMosquittoSerser) ... SKIP: Only on docker
    test_001_connect_to_server (tests.test_server.TestMosquittoSerser) ... ok

    ----------------------------------------------------------------------
    Ran 2 tests in 0.042s

    OK (SKIP=1)

    Tests for janitoo_mosquitto finished.

At last, we need to find the ip address on the network :

.. code:: bash

    ip addr

.. code:: bash

    1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN qlen 1
        link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
        inet 127.0.0.1/8 scope host lo
           valid_lft forever preferred_lft forever
    2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP qlen 1000
        link/ether b8:27:eb:a8:55:6d brd ff:ff:ff:ff:ff:ff
        inet 192.168.14.65/24 brd 192.168.14.255 scope global eth0
           valid_lft forever preferred_lft forever

The interafec should be called eth0 or wlan0 or womething like that.
Here, that is : 192.168.14.65.

You can now restart your server :

.. code:: bash

    sudo service jnt_tutorial restart


The docker appliance
====================

On Janitoo, you can use a docker appliance. Pull the janitoo_hostsensor image :

.. code:: bash

    docker pull bibi21000/janitoo_hostsensor

And create a container :

.. code:: bash

    docker create -p 8882:22 --name mycontainer bibi21000/janitoo_hostsensor

Start it :

.. code:: bash

    docker start mycontainer

Check that is it running :

.. code:: bash

    docker ps

Connect to the docker image and update the hostsensor configuration file :

.. code:: bash

    ssh root@$127.0.0.1 -p 8882

Default password is janitoo.

Open the configuration file. The docker image contains a nano or vim for editing files :

.. code:: bash

    root@8eafc45f6d09:~# vim /opt/janitoo/etc/janitoo_hostsensor.conf

You must update the broker ip. It should match the ip address of your shared "mosquitto" :

.. code:: bash

    broker_ip = 192.168.14.65

Save your updates and restart jnt_hostsensor :

.. code:: bash

    root@8eafc45f6d09:~# killall jnt_hostsensor

Exit from ssh :

.. code:: bash

    root@8eafc45f6d09:~# exit

For a complete tutorial about the janitoo_hostsensor docker appliance, loook at https://bibi21000.github.io/janitoo_hostsensor/.


The network
===========

Its time to query the network :

.. code:: bash

    jnt_query network --host 192.168.14.65

You should receive the list of nodes availables on your server :

.. code:: bash

    hadd       uuid                 name                      location                  product_type
    hadd       uuid                 name                      location                  product_type
    0121/0003  hostsensor__uptime   Uptime                    Docker                    Software component
    0121/0001  hostsensor__load     Load                      Docker                    Software component
    0121/0002  hostsensor__disks    Disks                     Dokcer                    Software component
    0121/0000  hostsensor           Docker sensors            Docker                    Default product type
    0225/0000  tutorial2            Hello world               Rapsberry                 Default product type
    0225/0002  tutorial2__temperature Temperature               Onewire                   Temperature sensor
    0225/0004  tutorial2__led       Led                       GPIO                      Software
    0225/0003  tutorial2__cpu       CPU                       Hostsensor                Software component
    0225/0001  tutorial2__ambiance  Ambiance 1                DHT                       Temperature/humidity sensor

We need to specify a host to query as we use a remote one. Query basics values using :

.. code:: bash

    jnt_query node --hadd 0121/0000 --vuuid request_info_basics --host 192.168.14.65

.. code:: bash

    hadd       node_uuid                 uuid                           idx  data                      units      type  genre cmdclass help
    0121/0001  hostsensor__load          load                           1    0.55                      None       3     1     49       The load average
    0121/0001  hostsensor__load          load                           0    0.19                      None       3     1     49       The load average
    0121/0001  hostsensor__load          load                           2    0.82                      None       3     1     49       The load average
    0121/0002  hostsensor__disks         total                          1    98294312960               Bytes      4     1     49       The total size of partitions
    0121/0002  hostsensor__disks         total                          0    98294312960               Bytes      4     1     49       The total size of partitions
    0121/0002  hostsensor__disks         total                          3    98294312960               Bytes      4     1     49       The total size of partitions
    0121/0002  hostsensor__disks         total                          2    98294312960               Bytes      4     1     49       The total size of partitions
    0121/0002  hostsensor__disks         total                          5    98294312960               Bytes      4     1     49       The total size of partitions
    0121/0002  hostsensor__disks         total                          4    98294312960               Bytes      4     1     49       The total size of partitions
    0121/0002  hostsensor__disks         used                           1    28937203712               Bytes      4     1     49       The used size of partitions
    0121/0002  hostsensor__disks         used                           0    28937203712               Bytes      4     1     49       The used size of partitions
    0121/0002  hostsensor__disks         used                           3    28937203712               Bytes      4     1     49       The used size of partitions
    0121/0002  hostsensor__disks         used                           2    28937203712               Bytes      4     1     49       The used size of partitions
    0121/0002  hostsensor__disks         used                           5    28937203712               Bytes      4     1     49       The used size of partitions
    0121/0002  hostsensor__disks         used                           4    28937203712               Bytes      4     1     49       The used size of partitions
    0121/0002  hostsensor__disks         percent_use                    1    29.4                      %          3     1     49       The percent_use of partitions
    0121/0002  hostsensor__disks         percent_use                    0    29.4                      %          3     1     49       The percent_use of partitions
    0121/0002  hostsensor__disks         percent_use                    3    29.4                      %          3     1     49       The percent_use of partitions
    0121/0002  hostsensor__disks         percent_use                    2    29.4                      %          3     1     49       The percent_use of partitions
    0121/0002  hostsensor__disks         percent_use                    5    29.4                      %          3     1     49       The percent_use of partitions
    0121/0002  hostsensor__disks         percent_use                    4    29.4                      %          3     1     49       The percent_use of partitions
    0121/0002  hostsensor__disks         free                           1    64340357120               Bytes      4     1     49       The free size of partitions
    0121/0002  hostsensor__disks         free                           0    64340357120               Bytes      4     1     49       The free size of partitions
    0121/0002  hostsensor__disks         free                           3    64340357120               Bytes      4     1     49       The free size of partitions
    0121/0002  hostsensor__disks         free                           2    64340357120               Bytes      4     1     49       The free size of partitions
    0121/0002  hostsensor__disks         free                           5    64340357120               Bytes      4     1     49       The free size of partitions
    0121/0002  hostsensor__disks         free                           4    64340357120               Bytes      4     1     49       The free size of partitions
    0121/0002  hostsensor__disks         partition                      1    /root/.ssh                None       8     1     49       The partition list
    0121/0002  hostsensor__disks         partition                      0    /etc/ssh                  None       8     1     49       The partition list
    0121/0002  hostsensor__disks         partition                      3    /etc/resolv.conf          None       8     1     49       The partition list
    0121/0002  hostsensor__disks         partition                      2    /opt/janitoo/etc          None       8     1     49       The partition list
    0121/0002  hostsensor__disks         partition                      5    /etc/hosts                None       8     1     49       The partition list
    0121/0002  hostsensor__disks         partition                      4    /etc/hostname             None       8     1     49       The partition list
    0121/0003  hostsensor__uptime        uptime                         0    21003.93                  None       3     1     49       Uptime in seconds


More servers
============

You could find something usefull here :

- https://github.com/bibi21000/janitoo_nut
- https://github.com/bibi21000/janitoo_roomba

All this examples have configurations and tests which should help you to configure your server.
