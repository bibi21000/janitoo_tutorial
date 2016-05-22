============
HelloWord V4
============


Explanations
============

In this part, we will connect many raspberries using Janitoo.
So ideally you need another one :D. But you can also use :

 - a computer with Ubuntu or Debian
 - install another server on the same raspberry

You could find something usefull here :

    - https://github.com/bibi21000/janitoo_nut
    - https://github.com/bibi21000/janitoo_roomba
    - https://github.com/bibi21000/janitoo_hostsensor_lmsensor
    - https://github.com/bibi21000/janitoo_hostsensor_psutil

All this examples have configurations and tests which should help you to configure your server.

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

The pure client
===============

On the other raspberry (or on your local pc), install Janitoo the same we do it in the past.
Except that you don't need to install mosquitto anymore, as we will use the one installed on the fisrt raspberry.

The only differnce is in the configuration file. Open it :

.. code:: bash

    vim /opt/janitoo/etc/jnt_tutorial.conf

.. code:: bash

    [system]
    service = jnt_tutorial
    log_dir = /opt/janitoo/log
    home_dir = /opt/janitoo/home
    pid_dir = /opt/janitoo/run
    conf_dir = /opt/janitoo/etc
    broker_ip = 192.168.14.65
    broker_port = 1883
    broker_keepalive = 60
    heartbeat_timeout = 10
    heartbeat_count = 3
    slow_start = 0.5

You need to change broker_ip = 127.0.0.1 to broker_ip = 192.168.14.65

On the Janitoo protocol, all machines must have its own hadd, so you need to change :

.. code:: bash

    hadd = 0225/0000

to

.. code:: bash

    hadd = 0226/0000

Do the same for all components on the bus : 0225/0001 -> 0226/0001, ...

You can now starts the service :

.. code:: bash

    sudo service jnt_tutorial start

You can look at the protocol during startup on the spyer terminal.

You can also look at logs. In a new terminal :

.. code:: bash

    tail -n 100 -f /opt/janitoo/log/jnt_tutorial.log

Its time to query ther server. Go to the first terminal and query the network :

.. code:: bash

    jnt_query network --host 192.168.14.65

You should receive the list of nodes availables on your server :

.. code:: bash

    hadd       uuid                 name                      location                  product_type
    hadd       uuid                 name                      location                  product_type
    0225/0000  tutorial2            Hello world               Rapsberry                 Default product type
    0225/0002  tutorial2__temperature Temperature               Onewire                   Temperature sensor
    0225/0004  tutorial2__led       Led                       GPIO                      Software
    0225/0003  tutorial2__cpu       CPU                       Hostsensor                Software component
    0225/0001  tutorial2__ambiance  Ambiance 1                DHT                       Temperature/humidity sensor
    0226/0000  tutorial2            Hello world               Rapsberry                 Default product type
    0226/0002  tutorial2__temperature Temperature               Onewire                   Temperature sensor
    0226/0004  tutorial2__led       Led                       GPIO                      Software
    0226/0003  tutorial2__cpu       CPU                       Hostsensor                Software component
    0226/0001  tutorial2__ambiance  Ambiance 1                DHT                       Temperature/humidity sensor

We need to specify a host to query as we use a remote one.


