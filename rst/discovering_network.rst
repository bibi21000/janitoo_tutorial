===================
Discovering network
===================


Goal
====

More servers for this parts and more about network too.


One more server
===============

We need another server it's not mandatory but it's also a way to speak about Janitoo deploying.
For example, we want to monitor our UPS.

You've got may way to do that.

In the first tutorial (:doc:`here <hello_world_v1>`), we defined 3 bus in the configuration file.
We can do the same by adding a bus section in the configuration file of a running server (of course after installing the needed modules) :

.. code:: bash

    [nut]
    auto_start = True
    heartbeat = 30
    config_timeout = 5
    hadd = 1045/0000
    components.ups1 = nut.ups
    components.ups2 = nut.ups

Doing this way, both buses will be launched in the same processus.
Remember that the GIL will surely block your code on a core, so a single core will hold your 2 appliances.
If a bus is not fair with resources (cpu, io, ...) the other one will be impacted.
Same if a bus fails.

In the :doc:`second <hello_world_v2>` and :doc:`third <hello_world_v3>` tutorials,
we aggregate 2 buses with python code. Your code will also stay on the same core.

We don't see it before but you can install many servers on the same rasberry but :

- don't share i2c, spi, ... between servers. You can safely launch one with spi and the other one with i2c
- you can share gpio as long as you use it on differents pins
- you must use different configuration file, server name, log file, ...

Each server run in its own processus, so it's much interessant on a multi-core machine.
If a server crash, the other should not be impacted.

At last, you can create your own docker appliance to deploy your servers at home.
Docker appliances are a simple way to deploy Janitoo too.
You need to install docker (Linux, Windows, MacOS, ...)
and deploy appliance in 3 commands.

A typical docker file for hostsensor and NUT should be like :

.. code:: bash

    FROM bibi21000/janitoo_docker_appliance

    MAINTAINER bibi21000 <bibi21000@gmail.com>

    WORKDIR /opt/janitoo/src

    RUN make clone module=janitoo_nut && \
        make appliance-deps module=janitoo_nut && \
        apt-get clean && rm -Rf /tmp/*||true && \
        [ -d /root/.cache ] && rm -Rf /root/.cache/*

    RUN make clone module=janitoo_hostsensor && \
        make clone module=janitoo_hostsensor_psutil && \
        make clone module=janitoo_hostsensor_lmsensor && \
        make appliance-deps module=janitoo_hostsensor && \
        apt-get clean && rm -Rf /tmp/*|| true && \
        [ -d /root/.cache ] && rm -Rf /root/.cache/*

    VOLUME ["/root/.ssh/", "/etc/ssh/", "/opt/janitoo/etc/"]

    EXPOSE 22

    CMD ["/root/auto.sh"]

After this explanations, install the NUT appliance docker from here : https://bibi21000.github.io/janitoo_nut/docker.html.
If you don't have an UPS, enter erronous informations and you will get a failed UPS.
Okay, okay, it's not mandatory but ...


Broadcast network
=================

Janitoo's protocol support broadcast. That mean that you can ask all nodes on ther server to send their configuration, ... and so on.

That's the way we discover the nodes in the last tutorial :

.. code:: bash

    $ jnt_query network --host=192.168.14.65

.. code:: bash

    request_info_nodes
    ----------
    hadd       uuid                 name                      location                  product_type
    0121/0003  hostsensor__uptime   Uptime                    Docker                    Software component
    0121/0001  hostsensor__load     Load                      Docker                    Software component
    0121/0002  hostsensor__disks    Disks                     Docker                    Software component
    0121/0000  hostsensor           Docker sensors            Docker                    Default product type
    0121/0004  hostsensor__lmsensor lm-sensors                Docker                    Software
    0120/0000  nut                  Default bus name controller Default location          Default product type
    0120/0001  nut__ups1            UPS                       Default location          3B1006X72726
    0225/0000  tutorial3            Hello world               Rapsberry                 Default product type
    0225/0002  tutorial3__temperature Temperature               Onewire                   Temperature sensor
    0225/0004  tutorial3__led       Led                       GPIO                      Software
    0225/0003  tutorial3__cpu       CPU                       Hostsensor                Software component
    0225/0001  tutorial3__ambiance  Ambiance 1                DHT                       Temperature/humidity sensor

But you can also ask for systems values.
System values are used by the protocol, you should not update or remove them in your code.

.. code:: bash

    $ jnt_query network --host=192.168.14.65 --vuuid=request_info_systems

.. code:: bash

    request_info_systems
    ----------
    hadd       node_uuid                 uuid                      idx  data                      units      type  genre cmdclass help
    0120/0001  nut__ups1                 heartbeat                 0    60                        seconds    4     4     112      The heartbeat delay in seconds
    0120/0001  nut__ups1                 config_timeout            0    3                         seconds    4     4     112      The config timeout before applying configuration and rebooting
    0120/0001  nut__ups1                 hadd                      0    0120/0001                            32    4     112      The Janitoo Home address
    0120/0000  nut                       heartbeat                 0    60                        seconds    4     4     112      The heartbeat delay in seconds
    0120/0000  nut                       config_timeout            0    5.0                       seconds    4     4     112      The config timeout before applying configuration and rebooting
    0120/0000  nut                       hadd                      0    0120/0000                            32    4     112      The Janitoo Home address
    0121/0000  hostsensor                heartbeat                 0    60                        seconds    4     4     112      The heartbeat delay in seconds
    0121/0000  hostsensor                config_timeout            0    3                         seconds    4     4     112      The config timeout before applying configuration and rebooting
    0121/0000  hostsensor                hadd                      0    0121/0000                            32    4     112      The Janitoo Home address
    0121/0001  hostsensor__load          heartbeat                 0    60                        seconds    4     4     112      The heartbeat delay in seconds
    0121/0001  hostsensor__load          config_timeout            0    3                         seconds    4     4     112      The config timeout before applying configuration and rebooting
    0121/0001  hostsensor__load          hadd                      0    0121/0001                            32    4     112      The Janitoo Home address
    0121/0002  hostsensor__disks         heartbeat                 0    60                        seconds    4     4     112      The heartbeat delay in seconds
    0121/0002  hostsensor__disks         config_timeout            0    3                         seconds    4     4     112      The config timeout before applying configuration and rebooting
    0121/0002  hostsensor__disks         hadd                      0    0121/0002                            32    4     112      The Janitoo Home address
    0121/0003  hostsensor__uptime        heartbeat                 0    60                        seconds    4     4     112      The heartbeat delay in seconds
    0121/0003  hostsensor__uptime        config_timeout            0    3                         seconds    4     4     112      The config timeout before applying configuration and rebooting
    0121/0003  hostsensor__uptime        hadd                      0    0121/0003                            32    4     112      The Janitoo Home address
    0121/0004  hostsensor__lmsensor      heartbeat                 0    60                        seconds    4     4     112      The heartbeat delay in seconds
    0121/0004  hostsensor__lmsensor      config_timeout            0    3                         seconds    4     4     112      The config timeout before applying configuration and rebooting
    0121/0004  hostsensor__lmsensor      hadd                      0    0121/0004                            32    4     112      The Janitoo Home address
    0225/0004  tutorial3__led            heartbeat                 0    30                        seconds    4     4     112      The heartbeat delay in seconds
    0225/0004  tutorial3__led            config_timeout            0    3                         seconds    4     4     112      The config timeout before applying configuration and rebooting
    0225/0004  tutorial3__led            hadd                      0    0225/0004                            32    4     112      The Janitoo Home address
    0225/0001  tutorial3__ambiance       heartbeat                 0    30                        seconds    4     4     112      The heartbeat delay in seconds
    0225/0001  tutorial3__ambiance       config_timeout            0    3                         seconds    4     4     112      The config timeout before applying configuration and rebooting
    0225/0001  tutorial3__ambiance       hadd                      0    0225/0001                            32    4     112      The Janitoo Home address
    0225/0000  tutorial3                 heartbeat                 0    30                        seconds    4     4     112      The heartbeat delay in seconds
    0225/0000  tutorial3                 config_timeout            0    3                         seconds    4     4     112      The config timeout before applying configuration and rebooting
    0225/0000  tutorial3                 hadd                      0    0225/0000                            32    4     112      The Janitoo Home address
    0225/0003  tutorial3__cpu            heartbeat                 0    30                        seconds    4     4     112      The heartbeat delay in seconds
    0225/0003  tutorial3__cpu            config_timeout            0    3                         seconds    4     4     112      The config timeout before applying configuration and rebooting
    0225/0003  tutorial3__cpu            hadd                      0    0225/0003                            32    4     112      The Janitoo Home address
    0225/0002  tutorial3__temperature    heartbeat                 0    30                        seconds    4     4     112      The heartbeat delay in seconds
    0225/0002  tutorial3__temperature    config_timeout            0    3                         seconds    4     4     112      The config timeout before applying configuration and rebooting
    0225/0002  tutorial3__temperature    hadd                      0    0225/0002                            32    4     112      The Janitoo Home address

When a primary node start and no other is started, it request all nodes and values of the nerwork by broadcast to create a map.
When a secondary can't contact a primary, it fall in fail mode and use broadcast to update its map.
On all other case, the map must be build using resolv (asking to the primary node)

Request nodes
=============

You can also retrieve information by asking directly to a controller one (the one is associated to the bus).
his is the requesting network.

.. code:: bash

    $ jnt_query node --hadd 0121/0000 --host=192.168.14.65 --vuuid=all

.. code:: bash

    request_info_nodes
    ----------
    hadd       uuid                           name                      location             product_type
    0121/0003  hostsensor__uptime             Uptime                    Docker               Software component
    0121/0001  hostsensor__load               Load                      Docker               Software component
    0121/0002  hostsensor__disks              Disks                     Docker               Software component
    0121/0000  hostsensor                     Docker sensors            Docker               Default product type
    0121/0004  hostsensor__lmsensor           lm-sensors                Docker               Software

    request_info_users
    ----------
    0121/0004  hostsensor__lmsensor      voltage                        0    None                      V          3     2     49       The voltage from lm-sensors
    0121/0004  hostsensor__lmsensor      temperature                    0    47.0                      °C         3     2     49       The temperatures from lm-sensors

    request_info_configs
    ----------
    0121/0000  hostsensor                location                       0    Docker                    None       8     3     112      The location of the node
    0121/0000  hostsensor                name                           0    Docker sensors            None       8     3     112      The name of the node
    0121/0001  hostsensor__load          load_config                    1    5 minutes                 None       2     3     112      The load average index (1, 5, and 15m)
    0121/0001  hostsensor__load          load_config                    0    1 minutes                 None       2     3     112      The load average index (1, 5, and 15m)
    0121/0001  hostsensor__load          load_config                    2    15 minutes                None       2     3     112      The load average index (1, 5, and 15m)
    0121/0001  hostsensor__load          location                       0    Docker                    None       8     3     112      The location of the node
    0121/0001  hostsensor__load          load_poll                      0    60                        seconds    4     3     112      The poll delay of the value
    0121/0001  hostsensor__load          name                           0    Load                      None       8     3     112      The name of the node
    0121/0002  hostsensor__disks         partition_poll                 0    1800                      seconds    4     3     112      The poll delay of the value
    0121/0002  hostsensor__disks         free_config                    0    /opt/janitoo/etc          None       8     3     112      The partition path
    0121/0002  hostsensor__disks         partition_config               0    /opt/janitoo/etc          None       8     3     112      The partition path
    0121/0002  hostsensor__disks         name                           0    Disks                     None       8     3     112      The name of the node
    0121/0002  hostsensor__disks         total_poll                     0    900                       seconds    4     3     112      The poll delay of the value
    0121/0002  hostsensor__disks         total_config                   0    /opt/janitoo/etc          None       8     3     112      The partition path
    0121/0002  hostsensor__disks         used_poll                      0    900                       seconds    4     3     112      The poll delay of the value
    0121/0002  hostsensor__disks         free_poll                      0    900                       seconds    4     3     112      The poll delay of the value
    0121/0002  hostsensor__disks         percent_use_config             0    /opt/janitoo/etc          None       8     3     112      The partition path
    0121/0002  hostsensor__disks         used_config                    0    /opt/janitoo/etc          None       8     3     112      The partition path
    0121/0002  hostsensor__disks         location                       0    Docker                    None       8     3     112      The location of the node
    0121/0002  hostsensor__disks         percent_use_poll               0    900                       seconds    4     3     112      The poll delay of the value
    0121/0003  hostsensor__uptime        location                       0    Docker                    None       8     3     112      The location of the node
    0121/0003  hostsensor__uptime        name                           0    Uptime                    None       8     3     112      The name of the node
    0121/0003  hostsensor__uptime        uptime_poll                    0    300                       seconds    4     3     112      The poll delay of the value
    0121/0004  hostsensor__lmsensor      temperature_poll               0    60                        seconds    4     3     112      The poll delay of the value
    0121/0004  hostsensor__lmsensor      name                           0    lm-sensors                None       8     3     112      The name of the node
    0121/0004  hostsensor__lmsensor      voltage_config                 0    None                      None       8     3     112      The name of the lmsensor
    0121/0004  hostsensor__lmsensor      voltage_poll                   0    90                        seconds    4     3     112      The poll delay of the value
    0121/0004  hostsensor__lmsensor      location                       0    Docker                    None       8     3     112      The location of the node
    0121/0004  hostsensor__lmsensor      temperature_config             0    temp1                     None       8     3     112      The name of the lmsensor
    0121/0004  hostsensor__lmsensor      config_filename                0    /etc/sensors3.conf        None       8     3     112      The full path/name of config file to use

    request_info_systems
    ----------
    0121/0000  hostsensor                heartbeat                      0    60                        seconds    4     4     112      The heartbeat delay in seconds
    0121/0000  hostsensor                config_timeout                 0    3                         seconds    4     4     112      The config timeout before applying configuration and rebooting
    0121/0000  hostsensor                hadd                           0    0121/0000                            32    4     112      The Janitoo Home address
    0121/0001  hostsensor__load          heartbeat                      0    60                        seconds    4     4     112      The heartbeat delay in seconds
    0121/0001  hostsensor__load          config_timeout                 0    3                         seconds    4     4     112      The config timeout before applying configuration and rebooting
    0121/0001  hostsensor__load          hadd                           0    0121/0001                            32    4     112      The Janitoo Home address
    0121/0002  hostsensor__disks         heartbeat                      0    60                        seconds    4     4     112      The heartbeat delay in seconds
    0121/0002  hostsensor__disks         config_timeout                 0    3                         seconds    4     4     112      The config timeout before applying configuration and rebooting
    0121/0002  hostsensor__disks         hadd                           0    0121/0002                            32    4     112      The Janitoo Home address
    0121/0003  hostsensor__uptime        heartbeat                      0    60                        seconds    4     4     112      The heartbeat delay in seconds
    0121/0003  hostsensor__uptime        config_timeout                 0    3                         seconds    4     4     112      The config timeout before applying configuration and rebooting
    0121/0003  hostsensor__uptime        hadd                           0    0121/0003                            32    4     112      The Janitoo Home address
    0121/0004  hostsensor__lmsensor      heartbeat                      0    60                        seconds    4     4     112      The heartbeat delay in seconds
    0121/0004  hostsensor__lmsensor      config_timeout                 0    3                         seconds    4     4     112      The config timeout before applying configuration and rebooting
    0121/0004  hostsensor__lmsensor      hadd                           0    0121/0004                            32    4     112      The Janitoo Home address

    request_info_basics
    ----------
    0121/0001  hostsensor__load          load                           1    0.32                      None       3     1     49       The load average
    0121/0001  hostsensor__load          load                           0    0.4                       None       3     1     49       The load average
    0121/0001  hostsensor__load          load                           2    0.43                      None       3     1     49       The load average
    0121/0002  hostsensor__disks         total                          0    98294312960               Bytes      4     1     49       The total size of partitions
    0121/0002  hostsensor__disks         used                           0    27372388352               Bytes      4     1     49       The used size of partitions
    0121/0002  hostsensor__disks         percent_use                    0    27.8                      %          3     1     49       The percent_use of partitions
    0121/0002  hostsensor__disks         free                           0    65905172480               Bytes      4     1     49       The free size of partitions
    0121/0002  hostsensor__disks         partition                      0    /opt/janitoo/etc          None       8     1     49       The partition list
    0121/0003  hostsensor__uptime        uptime                         0    172282.96                 None       3     1     49       Uptime in seconds

    request_info_commands
    ----------

This this the way primary and secondary nodes discover new nodes. When the receive an heartbeat from an unknown node, they "request" informations.


Values querying
===============

You can query a config value (setting or getting it) or a user one (ie setting a dimmer), ...

For example, we will get the list of configs values :

.. code:: bash

    $ jnt_query node --hadd 0121/0000 --vuuid request_info_configs

.. code:: bash

    hadd       node_uuid                 uuid                           idx  data                      units      type  genre cmdclass help
    0121/0000  hostsensor                location                       0    Docker                    None       8     3     112      The location of the node
    0121/0000  hostsensor                name                           0    Docker sensors            None       8     3     112      The name of the node
    0121/0001  hostsensor__load          load_config                    1    5 minutes                 None       2     3     112      The load average index (1, 5, and 15m)
    0121/0001  hostsensor__load          load_config                    0    1 minutes                 None       2     3     112      The load average index (1, 5, and 15m)
    0121/0001  hostsensor__load          load_config                    2    15 minutes                None       2     3     112      The load average index (1, 5, and 15m)
    0121/0001  hostsensor__load          location                       0    Docker                    None       8     3     112      The location of the node
    0121/0001  hostsensor__load          load_poll                      0    60                        seconds    4     3     112      The poll delay of the value
    0121/0001  hostsensor__load          name                           0    Load                      None       8     3     112      The name of the node
    0121/0002  hostsensor__disks         partition_poll                 0    1800                      seconds    4     3     112      The poll delay of the value
    0121/0002  hostsensor__disks         free_config                    0    /opt/janitoo/etc          None       8     3     112      The partition path
    0121/0002  hostsensor__disks         partition_config               0    /opt/janitoo/etc          None       8     3     112      The partition path
    0121/0002  hostsensor__disks         name                           0    Disks                     None       8     3     112      The name of the node
    0121/0002  hostsensor__disks         total_poll                     0    900                       seconds    4     3     112      The poll delay of the value
    0121/0002  hostsensor__disks         total_config                   0    /opt/janitoo/etc          None       8     3     112      The partition path
    0121/0002  hostsensor__disks         used_poll                      0    900                       seconds    4     3     112      The poll delay of the value
    0121/0002  hostsensor__disks         free_poll                      0    900                       seconds    4     3     112      The poll delay of the value
    0121/0002  hostsensor__disks         percent_use_config             0    /opt/janitoo/etc          None       8     3     112      The partition path
    0121/0002  hostsensor__disks         used_config                    0    /opt/janitoo/etc          None       8     3     112      The partition path
    0121/0002  hostsensor__disks         location                       0    Docker                    None       8     3     112      The location of the node
    0121/0002  hostsensor__disks         percent_use_poll               0    900                       seconds    4     3     112      The poll delay of the value
    0121/0003  hostsensor__uptime        location                       0    Docker                    None       8     3     112      The location of the node
    0121/0003  hostsensor__uptime        name                           0    Uptime                    None       8     3     112      The name of the node
    0121/0003  hostsensor__uptime        uptime_poll                    0    300                       seconds    4     3     112      The poll delay of the value
    0121/0004  hostsensor__lmsensor      temperature_poll               0    60                        seconds    4     3     112      The poll delay of the value
    0121/0004  hostsensor__lmsensor      name                           0    lm-sensors                None       8     3     112      The name of the node
    0121/0004  hostsensor__lmsensor      voltage_config                 0    None                      None       8     3     112      The name of the lmsensor
    0121/0004  hostsensor__lmsensor      voltage_poll                   0    90                        seconds    4     3     112      The poll delay of the value
    0121/0004  hostsensor__lmsensor      location                       0    Docker                    None       8     3     112      The location of the node
    0121/0004  hostsensor__lmsensor      temperature_config             0    temp1                     None       8     3     112      The name of the lmsensor
    0121/0004  hostsensor__lmsensor      config_filename                0    /etc/sensors3.conf        None       8     3     112      The full path/name of config file to use

We'll update the location of the controller node :

.. code:: bash

    hadd       node_uuid                 uuid                           idx  data                      units      type  genre cmdclass help
    0121/0000  hostsensor                location                       0    Docker                    None       8     3     112      The location of the node

Use the previous type, uuid, genre and cmdclass to create the query.
Set data to what you want. Add --writeonly True to set the value :

.. code:: bash

    $ jnt_query query --host=192.168.14.65 --hadd 0121/0000 --genre config --uuid location --data "My computer" --cmdclass 112 --type 8 --writeonly True

    location
    ----------
    hadd       uuid                      idx  data                      units      type  genre cmdclass help
    0121/0000  location                  0    My computer               None       None  3     112      The location of the node

You can get a value using --writeonly True :

.. code:: bash

    $ jnt_query query --host=192.168.14.65 --hadd 0121/0000 --genre config --uuid location --cmdclass 112 --readonly True

    location
    ----------
    hadd       uuid                      idx  data                      units      type  genre cmdclass help
    0121/0000  location                  0    My computer               None       None  3     112      The location of the node


Update the poll delay of the load value :

.. code:: bash

    hadd       node_uuid                 uuid                           idx  data                      units      type  genre cmdclass help
    0121/0001  hostsensor__load          load_poll                      0    60                        seconds    4     3     112      The poll delay of the value

.. code:: bash

    $ jnt_query query --host=192.168.14.65 --hadd 0121/0001 --genre config --uuid load_poll --data 10 --cmdclass 112 --type 4 --writeonly True

    load_poll
    ----------
    hadd       uuid                      idx  data                      units      type  genre cmdclass help
    0121/0001  load_poll                 0    10                        None       None  3     112      The poll delay of the value

Requery the config values :

.. code:: bash

    $ jnt_query node --hadd 0121/0000 --vuuid request_info_configs --host 192.168.14.65

.. code:: bash

    request_info_configs
    ----------
    hadd       uuid                           idx  data                      units      type  genre cmdclass help
    ...
    0121/0000  location                       0    My computer               None       8     3     112      The location of the node
    ...
    0121/0001  load_poll                      0    10                        seconds    4     3     112      The poll delay of the value
    ...

You can connect to docker appliance to check the configuration file :

.. code:: bash

    root@7de7e4993b13:~# cat /opt/janitoo/etc/janitoo_hostsensor.conf

.. code:: bash

    [hostsensor]
    auto_start = True
    components.load = hostsensor.load
    components.uptime = hostsensor.uptime
    components.disks = hostsensor.disks
    components.lmsensor = hostsensor.lmsensor
    heartbeat = 60
    name = Docker sensors
    location = My cumputer
    hadd = 0121/0000
    uuid = d6b66de0-21ed-11e6-ae4d-0242ac110002
    ...
    [hostsensor__load]
    heartbeat = 60
    name = Load
    location = Docker
    hadd = 0121/0001
    load_poll_0 = 10

You can also spy the values update and check that the load value is published every 10 seconds.

.. code:: bash

    $ jnt_spy --host 192.168.14.65 --topic /values/#

    >>>>>> Subscribe to /values/#
    !!!!!! Connect rc : 0
    !!!!!! Subscribed to None : 1 (0,)
    !!!!!! Type Ctrl+C 2 times to exit !!!!!!
    /values/basic/0121/0001/load 0 {"0": {"help": "The load average", "max": null, "reply_hadd": null, "entry_name": "sensor_float", "genre": 1, "poll_delay": 10,
     "data": 0.31, "is_writeonly": false, "list_items": null, "index": 0, "node_uuid": "hostsensor__load", "uuid": "load", "voice_uuid": null, "min": null, "defau
    lt": null, "cmd_class": 49, "hadd": "0121/0001", "label": "Load (1 minutes)", "units": null, "is_readonly": true, "is_polled": true, "type": 3}, "1": {"help":
     "The load average", "max": null, "reply_hadd": null, "entry_name": "sensor_float", "genre": 1, "poll_delay": 10, "data": 0.49, "is_writeonly": false, "list_i
    tems": null, "index": 1, "node_uuid": "hostsensor__load", "uuid": "load", "voice_uuid": null, "min": null, "default": null, "cmd_class": 49, "hadd": "0121/000
    1", "label": "Load (5 minutes)", "units": null, "is_readonly": true, "is_polled": true, "type": 3}, "2": {"help": "The load average", "max": null, "reply_hadd
    ": null, "entry_name": "sensor_float", "genre": 1, "poll_delay": 10, "data": 0.59, "is_writeonly": false, "list_items": null, "index": 2, "node_uuid": "hostse
    nsor__load", "uuid": "load", "voice_uuid": null, "min": null, "default": null, "cmd_class": 49, "hadd": "0121/0001", "label": "Load (15 minutes)", "units": nu
    ll, "is_readonly": true, "is_polled": true, "type": 3}}

You can get the documentation about `jnt_query <https://bibi21000.github.io/janitoo/cli.html#jnt-query>`_.


Command class discovering
=========================

Requesting and broadcasting informations create a lot of traffic on the network. So It's better to not use it on commons nodes.
It should be reserved to primary or sencondaries nodes.

But sometimes it's necessary. So if you really need it, use the resolv method.

We spoke many times about primary and secondaries ... but never about their implementation / deployement.

Typically, a primary is a Dynamic Home Configuration Protocol (DHCP), it will store the configuration of all nodes (using a db or not).
Actually, it about 20% finish ... so not usuable. And maybe we should do some updates on protocol.
That's why we set the HADD manually in the configuration file ...

And secondaries ?

Technically, every thread or server (in Janitoo API) can be a secondary. But a secondary hold a full map of the network (maybe more than 1000 values)
and it will consume RAM and cpu (to take the map up to date).

Typically, a user interface (`janitoo_manager <https://github.com/bibi21000/janitoo_manager>`_) which needs to list nodes, values, should be a secondary.

A notifier, which needs to call many nodes (an email notifier, a sms notifier, a tv message, a ring on an raspberry)  may
be a secondary too.

Typically, if you want your server become a secondary, you should extend the default network :

.. code:: python

    class MyNetwork(JNTNetwork):
        """The network manager for the flask application
        """

        def __init__(self, stop_event, options, **kwargs):
            """
            """
            JNTNetwork.__init__(self, stop_event, options, **kwargs)
            self.extend_from_entry_points('janitoo_tutorial')

        def emit_network(self):
            """Emit a network state event
            """
            ret = {}
            ret['state'] = self.state,
            ret['state_str'] = self.state_str,
            ret['nodes_count'] = self.nodes_count,
            ret['home_id'] = self.home_id,
            ret['is_failed'] = self.is_failed,
            ret['is_secondary'] = self.is_secondary,
            ret['is_primary'] = self.is_primary,

        def extend_from_entry_points(self, group):
            """"Extend the network with methods found in entrypoints
            """
            for entrypoint in iter_entry_points(group = '%s.network'%group):
                logger.info('Extend network with %s', entrypoint.module_name )
                extend = entrypoint.load()
                extend( self )

And you need to start/stop it the right place in your server (janitoo_dhcp `https://github.com/bibi21000/janitoo_dhcp/blob/master/src/janitoo_dhcp/server.py`_)

The network object will do all the requests / broadcast to populate the map : with a working primary (and some code fixes :)),
it should be up in less than 10 seconds.
With no primary, it take at least 30 seconds and surely more on large installations.
Look at the video on youtube or install the janitoo_manager package.

This example is copy/paste from the dhcp server, which is written with an old release of Janitoo.
Contact the core team if you need to develop a secondary node.

Back to the command classes : they are a way to organize nodes/values, it represents a capacity of a node :
ie a switch implement the cmdclass COMMAND_SWITCH_BINARY.
For a dimmer, it is COMMAND_SWITCH_MULTILEVEL.

Primary or secondaries
----------------------

On a primary or secondary, you can extend the network object to collect command classes :

.. code:: python

   def find_webcontrollers():
        """Return a dict with the web controller
        """
        res = {}
        web_servers = [node for node in self.nodes if COMMAND_WEB_CONTROLLER in self.nodes[node]['cmd_classes']]
        for node in web_servers:
            if node in self.basics:
                res[node] = {}
                for value in self.basics[node]:
                    res[node][value] = {}
                    for index in self.basics[node][value]:
                        if self.basics[node][value][index]['cmd_class'] == COMMAND_WEB_CONTROLLER:
                            res[node][value][index] = {
                                'value_uuid':self.basics[node][value][index]['uuid'],
                                'value_index':self.basics[node][value][index]['index'],
                                'data':self.basics[node][value][index]['data'],
                                'label':self.basics[node][value][index]['label'],
                                'help':self.basics[node][value][index]['data'],
                            }

This is the way the proxy extension for manager works : it collects all nodes which implements cmdclass COMMAND_WEB_CONTROLLER to show them on the web page
(̀ here <https://github.com/bibi21000/janitoo_manager_proxy/blob/master/src/janitoo_manager_proxy/network.py>`_).

Resolv
------

Not implemented.

Make a call via uuid to the primary to get a list of nodes implementing the needed command class.


More servers
============

You can find docker appliance here :

- https://bibi21000.github.io/janitoo_docker_appliance/directory.html

You could find other servers here :

- https://github.com/bibi21000/janitoo_nut
- https://github.com/bibi21000/janitoo_roomba

All this examples have configurations and tests which should help you to configure your server.
