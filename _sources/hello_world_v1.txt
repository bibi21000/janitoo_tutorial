============
HelloWord V1
============


Explanations
============

For this first example, we will create a server using a configuration file.


Configuration
=============

Change to the tutorial directory :

.. code:: bash

    cd /opt/janitoo/src/janitoo_tutorial

And open the test configuration file in your favorite editor :

.. code:: bash

    vim tests/data/helloworldv1.conf


The DHT component
-----------------

At first, we will add the DHT component.

You can see the following section :

.. code:: bash

    [rpibasic]
    auto_start = True
    name = Hello world
    location = DHT
    components.ambiance = rpibasic.dht
    hadd = 0220/0000

It defines a new bus with a name and a location.
We must define the HADD of the controller node associated to the bus (0220/0000).
This bus hold one component (ambiance) of type rpibasic.dht.

Look at the following section :

.. code:: bash

    [rpibasic__ambiance]
    name = Ambiance 1
    location = DHT
    hadd = 0220/0001
    pin_0 = 6
    sensor_0 = 11

We add the ambiance component of the rpibasic bus ([rpibasic__ambiance]) and define a location and a name.
Like for the bus, we should set an HADD for the associated node (0220/0001).

There is 2 other parameters which allows to define the pin used (pin_0) to connect the sensor and its type (sensor_0).

You can get more informations on config values using jnt_collect :

.. code:: bash

    jnt_collect -c rpibasic.dht

.. code:: bash

    -------------------------------------------------------------------------------
    Component : rpibasic.dht
     temperature_poll : Config : Int - The poll delay of the value (None)
     temperature : User : Decimal - The temperature (None)
     pin : Config : Int - The pin number on the board (1)
     humidity_poll : Config : Int - The poll delay of the value (None)
     humidity : User : Decimal - The humidity (None)
     sensor : Config : Int - The sensor type : 11,22,2302 (11)

You can see that sensor config value can be : 11, 22 or 2302.
That's why there is sensor_0 = 11 in the config values. Of course, update it to your needs.

Config values in configuration files always ended with a _0. In the future, we will support multi-instances using (_1,_2, ...)

You can also use jnt_collect to get values from a bus :

.. code:: bash

    jnt_collect -b rpibasic

.. code:: bash

    -------------------------------------------------------------------------------
    Bus (thread) : rpibasic

No values for this bus ;)


The DS18B20 component
---------------------

At first, we will add the DS18B20 Onewire component.

You can see the following section :

.. code:: bash

    [rpi1wire]
    auto_start = True
    name = Hello world
    location = Onewire
    components.temperature = rpi1wire.ds18b20
    hadd = 0221/0000

It defines a new bus with a name and a location.
We must define the HADD of the controller node associated to the bus (0221/0000).
This bus hold one component (temperature) of type rpi1wire.ds18b20.

.. code:: bash

    jnt_collect -b rpi1wire

.. code:: bash

    -------------------------------------------------------------------------------
    Bus (thread) : rpi1wire
     rpi1wire_sensors_dir : Config : String - The sensor directory (/sys/bus/w1/devices/)

Using jnt_collect you can see that there is a config value available for this bus.
The default value is whown between () : /sys/bus/w1/devices/

Values for bus always start with the bus oid (for avoiding conflict when aggragating bus).

If you need to set this config value, add a line like :

.. code:: bash

    rpi1wire_sensors_dir_0 = /sys/bus/w1/devices/

.. code:: bash

    [rpi1wire__temperature]
    name = Temperature
    location = Onewire
    hadd = 0221/0001
    hexadd_0 = 28-00000463b745

We add the temperature component of the rpi1wire bus ([rpi1wire__temperature]) and define a location and a name.
Like for the bus, we should set an HADD for the associated node (0221/0001).

You can get more informations on config values using jnt_collect :

.. code:: bash

    jnt_collect -c rpi1wire.ds18b20

.. code:: bash

    -------------------------------------------------------------------------------
    Component : rpi1wire.ds18b20
     hexadd : Config : String - The hexadecimal address of the DS18B20 (28-000005e2fdc3)
     temperature_poll : Config : Int - The poll delay of the value (None)
     temperature : User : Decimal - The temperature (None)

You can see that hexadd config value is the address of your DS18B20. You can find it using :

.. code:: bash

    ls /sys/bus/w1/devices/


The CPU component
-----------------

And finally the configuration for the CPU monitoring :

.. code:: bash

    [hostsensor]
    auto_start = True
    components.picpu = hostsensor.picpu
    name = Hello world
    location = Hostsensor
    hadd = 0222/0000

    [hostsensor__picpu]
    name = CPU
    location = Hostsensor
    hadd = 0222/0001


Test it
=======

You're ready to test your server. Janitoo has a lot of built in tests.

.. code:: bash

    vim tests/test_server_v1.py

.. code:: python

    class TestTutorialServer(JNTTServer, JNTTServerCommon):
        """Test the tutorial server
        """
        server_class = PiServer
        server_conf = "tests/data/helloworldv1.conf"

        hadds = [HADD%(220,0), HADD%(220,1), HADD%(221,0), HADD%(221,1), HADD%(222,0), HADD%(222,1)]

For the impatient :

.. code:: bash

    sudo nosetests tests/test_server_v1.py -v -m test_040_server_start_no_error_in_log

If everything is ok, the screen output should be something like this :

.. code:: bash

    test_040_server_start_no_error_in_log (tests.test_server_v1.TestTutorialServer) ... ok
    ----------------------------------------------------------------------
    Ran 1 test in 128.712s

    OK

Otherwise you should have a log capture with surely some errors inside.


Launch it
=========

You can now copy the config file to the config directory:

.. code:: bash

    cd /opt/janitoo/etc
    cp /opt/janitoo/src/janitoo_tutorial/tests/data/helloworldv1.conf .

And launch the server :

.. code:: bash

    sudo jnt_raspberry -c /opt/janitoo/etc/helloworldv1.conf front

This will launch the server in foreground.

You can type ctrl + c to stop it.

If everything is ok, you can launch the server in background :

.. code:: bash

    sudo jnt_raspberry -c /opt/janitoo/etc/helloworldv1.conf start

You can stop it using :

.. code:: bash

    sudo jnt_raspberry -c /opt/janitoo/etc/helloworldv1.conf stop

Checking its status :

.. code:: bash

    sudo jnt_raspberry -c /opt/janitoo/etc/helloworldv1.conf status

Or killing it if needed :

.. code:: bash

    sudo jnt_raspberry -c /opt/janitoo/etc/helloworldv1.conf kill


Query it
========

Launch the server :

.. code:: bash

    sudo jnt_raspberry -c /opt/janitoo/etc/helloworldv1.conf start

Open a new shell (or screen) and launch the spyer. It will report all activity on mqtt :

.. code:: bash

    jnt_spy

You can look at the protocol during startup. You'll see something like this :

.. code:: bash

    >>>>>> Subscribe to /#
    !!!!!! Connect rc : 0
    !!!!!! Subscribed to None : 1 (0,)
    !!!!!! Type Ctrl+C 2 times to exit !!!!!!
    ...
    /values/user/0222/0001/voltage 0 {"help": "The voltage of the CPU", "voice_uuid": null, "max": null, "reply_hadd": null, "node_uuid": "hostsensor__picpu", "entry_name": "sensor_voltage", "genre": 2, "poll_delay": 300, "data": 1.35, "is_polled": true, "is_writeonly": false, "list_items": null, "index": 0, "uuid": "voltage", "is_readonly": true, "min": null, "default": null, "type": 3, "cmd_class": 49, "hadd": "0222/0001", "label": "CPUVolt", "units": "V"}
    /dhcp/heartbeat/0222/0001 0 OFFLINE
    /dhcp/heartbeat/0221/0001 0 ONLINE
    /values/user/0220/0001/humidity 0 {"help": "The humidity", "voice_uuid": null, "max": null, "reply_hadd": null, "node_uuid": "rpibasic__ambiance", "entry_name": "sensor_humidity", "genre": 2, "poll_delay": 300, "data": 34.0, "is_polled": true, "is_writeonly": false, "list_items": null, "index": 0, "uuid": "humidity", "is_readonly": true, "min": null, "default": null, "type": 3, "cmd_class": 49, "hadd": "0220/0001", "label": "Hum", "units": "%"}
    /dhcp/heartbeat/0220/0001 0 ONLINE
    /values/user/0222/0001/frequency 0 {"help": "The frequency of the CPU", "voice_uuid": null, "max": null, "reply_hadd": null, "node_uuid": "hostsensor__picpu", "entry_name": "sensor_frequency", "genre": 2, "poll_delay": 300, "data": 1000, "is_polled": true, "is_writeonly": false, "list_items": null, "index": 0, "uuid": "frequency", "is_readonly": true, "min": null, "default": null, "type": 3, "cmd_class": 49, "hadd": "0222/0001", "label": "CPUFreq", "units": "MHz"}
    /values/user/0222/0001/temperature 0 {"help": "The temperature of the CPU", "voice_uuid": null, "max": null, "reply_hadd": null, "node_uuid": "hostsensor__picpu", "entry_name": "sensor_temperature", "genre": 2, "poll_delay": 300, "data": 40.1, "is_polled": true, "is_writeonly": false, "list_items": null, "index": 0, "uuid": "temperature", "is_readonly": true, "min": null, "default": null, "type": 3, "cmd_class": 49, "hadd": "0222/0001", "label": "CPUTemp", "units": "\u00b0C"}
    /values/user/0220/0001/temperature 0 {"help": "The temperature", "voice_uuid": null, "max": null, "reply_hadd": null, "node_uuid": "rpibasic__ambiance", "entry_name": "sensor_temperature", "genre": 2, "poll_delay": 300, "data": 21.0, "is_polled": true, "is_writeonly": false, "list_items": null, "index": 0, "uuid": "temperature", "is_readonly": true, "min": null, "default": null, "type": 3, "cmd_class": 49, "hadd": "0220/0001", "label": "Temp", "units": "\u00b0C"}
    /values/user/0221/0001/temperature 0 {"help": "The temperature", "voice_uuid": null, "max": null, "reply_hadd": null, "node_uuid": "rpi1wire__temperature", "entry_name": "sensor_temperature", "genre": 2, "poll_delay": 300, "data": 85.0, "is_polled": true, "is_writeonly": false, "list_items": null, "index": 0, "uuid": "temperature", "is_readonly": true, "min": null, "default": null, "type": 3, "cmd_class": 49, "hadd": "0221/0001", "label": "Temp", "units": "\u00b0C"}
    /dhcp/heartbeat/0222/0000 0 ONLINE
    /dhcp/heartbeat/0222/0001 0 OFFLINE
    /dhcp/heartbeat/0221/0000 0 ONLINE
    /dhcp/heartbeat/0220/0000 0 ONLINE
    /dhcp/heartbeat/0221/0001 0 ONLINE
    /dhcp/heartbeat/0220/0001 0 ONLINE
    /dhcp/heartbeat/0221/0001 0 OFFLINE
    /dhcp/heartbeat/0222/0001 0 OFFLINE
    /dhcp/heartbeat/0220/0000 0 OFFLINE
    ...

You can also look at logs. In a new terminal :

.. code:: bash

    tail -n 100 -f /opt/janitoo/log/helloworldv1.log

Its time to query ther server. Go to the first terminal and query the network :

.. code:: bash

    jnt_query network

You should receive the list of nodes availables on your server :

.. code:: bash

    hadd       uuid                 name                      location                  product_type
    0222/0001  hostsensor__picpu    CPU                       Hostsensor                Software component
    0222/0000  hostsensor           Hello world               Hostsensor                Default product type
    0220/0000  rpibasic             Hello world               DHT                       Default product type
    0220/0001  rpibasic__ambiance   Ambiance 1                DHT                       Temperature/humidity sensor
    0221/0001  rpi1wire__temperature Temperature               Onewire                   Temperature sensor
    0221/0000  rpi1wire             Hello world               Onewire                   Default product type

You can also query a node :

.. code:: bash

    jnt_query node --hadd 0222/0000

.. code:: bash

    hadd       uuid                           name                      location             product_type
    0222/0001  hostsensor__picpu              CPU                       Hostsensor           Software component
    0222/0000  hostsensor                     Hello world               Hostsensor           Default product type

.. code:: bash

    jnt_query node --hadd 0220/0000

.. code:: bash

    hadd       uuid                           name                      location             product_type
    0220/0000  rpibasic                       Hello world               DHT                  Default product type
    0220/0001  rpibasic__ambiance             Ambiance 1                DHT                  Temperature/humidity sensor

.. code:: bash

    jnt_query node --hadd 0221/0000

.. code:: bash

    hadd       uuid                           name                      location             product_type
    0221/0001  rpi1wire__temperature          Temperature               Onewire              Temperature sensor
    0221/0000  rpi1wire                       Hello world               Onewire              Default product type

You can also query a node to request its users values :

.. code:: bash

    jnt_query node --hadd 0222/0000 --vuuid request_info_users

.. code:: bash

    hadd       node_uuid                 uuid                           idx  data                      units      type  genre cmdclass help
    0222/0001  hostsensor__picpu         frequency                      0    999                       MHz        3     2     49       The frequency of the CPU
    0222/0001  hostsensor__picpu         voltage                        0    1.35                      V          3     2     49       The voltage of the CPU
    0222/0001  hostsensor__picpu         temperature                    0    39.5                      °C         3     2     49       The temperature of the CPU


Performances
============

.. code:: bash

    nice top

.. code:: bash

    PID   USER      PR  NI  VIRT  RES  SHR S  %CPU %MEM    TIME+  COMMAND
    10793 root      20   0  131m  14m 4268 S   5,6  2,9   0:46.98 /usr/bin/python /usr/local/bin/jnt_tutorial -c /opt/janitoo/src/jani
