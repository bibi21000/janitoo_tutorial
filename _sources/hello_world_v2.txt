============
HelloWord V2
============


Goal
====

For this second example, we will create a more sophisticated server : it will calculate the average temperature and send it.

In the previous, we define many bus in the configuration. This have some limits, in particular if we want to do some operations (like calculating the average temperature) on the values.

So in this example, we will create a new bus which will hold all the sensors and define a new value.


The components
==============

Change to the tutorial directory :

.. code:: bash

    $ cd /opt/janitoo/src/janitoo_tutorial

Open the tutorial1 implementation :

.. code:: bash

    $ vim src/janitoo_tutorial/tutorial1.py

We will import all the needed components, and update their oid to match the new bus oid (tutorial1).
For the DHT component, it's looks like :

.. code:: python

    from janitoo_raspberry_dht.dht import DHTComponent

    ...

    class AmbianceComponent(DHTComponent):
        """ A component for ambiance """

        def __init__(self, bus=None, addr=None, **kwargs):
            """
            """
            oid = kwargs.pop('oid', 'tutorial1.ambiance')
            name = kwargs.pop('name', "Ambiance sensor")
            DHTComponent.__init__(self, oid=oid, bus=bus, addr=addr, name=name,
                    **kwargs)


The bus
=======

At first, we will aggregate the needed bus.
We don't need to aggregate the rpibasic bus (which hold the dht component) as it holds no special features.
Of course, we would add it without problem.

.. code:: python

    def __init__(self, **kwargs):
        """
        """
        JNTBus.__init__(self, **kwargs)
        self.buses = {}
        self.buses['gpiobus'] = GpioBus(masters=[self], **kwargs)
        self.buses['1wire'] = OnewireBus(masters=[self], **kwargs)

After, we will a new value to propagate the average tempetature :

.. code:: python

        uuid="{:s}_temperature".format(OID)
        self.values[uuid] = self.value_factory['sensor_temperature'](options=self.options, uuid=uuid,
            node_uuid=self.uuid,
            get_data_cb=self.get_temperature_cb,
            help='The average temperature of tutorial. Can be use as a good quality source for a thermostat.',
            label='Temp',
        )

        poll_value = self.values[uuid].create_poll_value(default=300)
        self.values[poll_value.uuid] = poll_value

We also define a poll value to this value.


The thread
==========

The thread hold the bus :

.. code:: bash

    $ vim src/janitoo_tutorial/thread_tutorial1.py

We will import all the needed components, and update their oid to match the new bus oid (tutorial1).
For the DHT component, it's looks like :

.. code:: python

    class TutorialThread(JNTBusThread):
        """The basic thread

        """
        def init_bus(self):
            """Build the bus
            """
            from janitoo_tutorial.tutorial1 import TutorialBus
            self.section = OID
            self.bus = TutorialBus(options=self.options, oid=self.section, product_name="Raspberry tutorial controller")


Entry-points
============

Janitoo uses entry-points for defining threads (bus) and components :

.. code:: python

    entry_points = {
        "janitoo.threads": [
            "tutorial1 = janitoo_tutorial.thread_tutorial1:make_thread",
        ],
        "janitoo.components": [
            "tutorial1.ambiance = janitoo_tutorial.tutorial1:make_ambiance",
            "tutorial1.cpu = janitoo_tutorial.tutorial1:make_cpu",
            "tutorial1.temperature = janitoo_tutorial.tutorial1:make_temperature",
        ],
    },

The entry-point reference a function in the thread :

.. code:: python

    def make_thread(options, force=False):
        if get_option_autostart(options, OID) == True or force:
            return TutorialThread(options)
        else:
            return None

Or for the component :

.. code:: python

    def make_ambiance(**kwargs):
        return AmbianceComponent(**kwargs)


Configuration
=============

Open the test configuration file in your favorite editor :

.. code:: bash

    $ vim tests/data/helloworldv2.conf

Like seen in the first tutorial, there is a section for the new bus (thread) :

.. code:: bash

    [tutorial1]
    auto_start = True
    name = Hello world
    location = Rapsberry
    components.ambiance = tutorial1.ambiance
    components.temperature = tutorial1.temperature
    components.cpu = tutorial1.cpu
    hadd = 0225/0000

It defines a new bus with a name and a location.
We must define the HADD of the controller node associated to the bus (0225/0000).
But this bus now holds the 3 components.

Look at the DHT section, it's similar to the one seen in first tutorial :

.. code:: bash

    [tutorial1__ambiance]
    name = Ambiance 1
    location = DHT
    hadd = 0225/0001
    pin_0 = 6
    sensor_0 = 11


Test it
=======

You're ready to test your components. Create a test for each component. For example, for the DTH:

.. code:: bash

    $ vim tests/test_components_v2.py

.. code:: python

    class TestAmbianceComponent(JNTTComponent, JNTTComponentCommon):
        """Test the component
        """
        component_name = "tutorial1.ambiance"

And launch it :

.. code:: bash

    $ sudo nosetests -v tests/test_components_v2.py

The result should be :

.. code:: bash

    test_001_component_entry_point (tests.test_components_v2.TestAmbianceComponent) ... ok
    test_002_component_oid (tests.test_components_v2.TestAmbianceComponent) ... ok
    test_002_component_properties (tests.test_components_v2.TestAmbianceComponent) ... ok
    test_001_component_entry_point (tests.test_components_v2.TestCpuComponent) ... ok
    test_002_component_oid (tests.test_components_v2.TestCpuComponent) ... ok
    test_002_component_properties (tests.test_components_v2.TestCpuComponent) ... ok
    test_001_component_entry_point (tests.test_components_v2.TestLedComponent) ... ok
    test_002_component_oid (tests.test_components_v2.TestLedComponent) ... ok
    test_002_component_properties (tests.test_components_v2.TestLedComponent) ... ok
    test_001_component_entry_point (tests.test_components_v2.TestTemperatureComponent) ... ok
    test_002_component_oid (tests.test_components_v2.TestTemperatureComponent) ... ok
    test_002_component_properties (tests.test_components_v2.TestTemperatureComponent) ... ok

    ----------------------------------------------------------------------
    Ran 12 tests in 6.772s

    OK

Test for the tread :

.. code:: bash

    $ vim tests/tests/test_thread_v2.py

.. code:: python

    class TestTutorialThread(JNTTThreadRun, JNTTThreadRunCommon):
        """Test the thread
        """
        thread_name = "tutorial1"
        conf_file = "tests/data/janitoo_tutorial2.conf"

And launch it :

.. code:: bash

    $ sudo nosetests -v tests/test_thread_v2.py

The result should be :

.. code:: bash

    test_001_thread_entry_point (tests.test_thread_v2.TestTutorialThread) ... ok
    test_011_thread_start_wait_stop (tests.test_thread_v2.TestTutorialThread) ... ok
    test_031_cron_hourly (tests.test_thread_v2.TestTutorialThread) ... SKIP: Hourly timer not used for this thread

    ----------------------------------------------------------------------
    Ran 3 tests in 27.107s

    OK (SKIP=1)

And the test for the bus :

.. code:: bash

    $ vim tests/tests/test_bus_v2.py

.. code:: python

    from janitoo_tutorial.tutorial1 import TutorialBus

    class TestTutorialBus(JNTTBus, JNTTBusCommon):
        """Test the Bus
        """
        oid = 'tutorial1'
        bus = TutorialBus

And launch it :

.. code:: bash

    $ sudo nosetests -v tests/test_bus_v2.py

The result should be :

.. code:: bash

    test_001_bus_oid (tests.test_bus_v2.TestTutorialBus) ... ok
    test_002_bus_values (tests.test_bus_v2.TestTutorialBus) ... ok

    ----------------------------------------------------------------------
    Ran 2 tests in 0.784s

    OK

And for the server :

.. code:: python

    $ vim tests/test_server_v2.py

.. code:: bash

    class TestTutorialServer(JNTTServer, JNTTServerCommon):
        """Test the tutorial server
        """
        server_class = PiServer
        server_conf = "tests/data/helloworldv2.conf"

        hadds = [HADD%(225,0), HADD%(225,1), HADD%(225,2), HADD%(225,3)]

And launch it :

.. code:: bash

    $ sudo nosetests -v tests/test_server_v2.py

The result should be :

.. code:: bash

    test_010_start_heartbeat_stop (tests.test_server_v2.TestTutorialServer) ... ok
    test_011_start_reload_stop (tests.test_server_v2.TestTutorialServer) ... ok
    test_012_start_reload_threads_stop (tests.test_server_v2.TestTutorialServer) ... ok
    test_020_request_broadcast (tests.test_server_v2.TestTutorialServer) ... ok
    test_030_wait_for_all_nodes (tests.test_server_v2.TestTutorialServer) ... ok
    test_040_server_start_no_error_in_log (tests.test_server_v2.TestTutorialServer) ... ok
    ----------------------------------------------------------------------
    Ran 6 tests in 828.932s

    OK

Otherwise you should have a log capture with surely some errors inside.

You can also the whole tests, which whould help you to fix problems :

.. code:: bash

    $ sudo make tests


Launch it
=========

You can now copy the config file to the config directory:

.. code:: bash

    $ cd /opt/janitoo/etc
    $ cp /opt/janitoo/src/janitoo_tutorial/tests/data/helloworldv2.conf .

Launch the server :

.. code:: bash

    $ sudo jnt_raspberry -c /opt/janitoo/etc/helloworldv2.conf start

You can look at the protocol during startup on the spyer terminal.

You can also look at logs. In a new terminal :

.. code:: bash

    $ tail -n 100 -f /opt/janitoo/log/helloworldv2.log

Its time to query ther server. Go to the first terminal and query the network :

.. code:: bash

    $ jnt_query network

You should receive the list of nodes availables on your server :

.. code:: bash

    hadd       uuid                 name                      location                  product_type
    0225/0000  tutorial1            Hello world               Rapsberry                 Default product type
    0225/0002  tutorial1__temperature Temperature               Onewire                   Temperature sensor
    0225/0001  tutorial1__ambiance  Ambiance 1                DHT                       Temperature/humidity sensor
    0225/0003  tutorial1__cpu       CPU                       Hostsensor                Software component

You can also query a node :

.. code:: bash

    $ jnt_query node --hadd 0225/0000

.. code:: bash

    hadd       uuid                           name                      location             product_type
    0225/0000  tutorial1                      Hello world               Rapsberry            Default product type
    0225/0002  tutorial1__temperature         Temperature               Onewire              Temperature sensor
    0225/0001  tutorial1__ambiance            Ambiance 1                DHT                  Temperature/humidity sensor
    0225/0003  tutorial1__cpu                 CPU                       Hostsensor           Software component

.. code:: bash

Check the config values :

.. code:: bash

    $ jnt_query node --hadd 0225/0000 --vuuid request_info_configs

.. code:: bash

    hadd       node_uuid                 uuid                           idx  data                      units      type  genre cmdclass help
    0225/0001  tutorial1__ambiance       temperature_poll               0    300                       seconds    4     3     112      The poll delay of the value
    0225/0001  tutorial1__ambiance       name                           0    Ambiance 1                None       8     3     112      The name of the node
    0225/0001  tutorial1__ambiance       pin                            0    6                         None       4     3     112      The pin number on the board
    0225/0001  tutorial1__ambiance       humidity_poll                  0    300                       seconds    4     3     112      The poll delay of the value
    0225/0001  tutorial1__ambiance       location                       0    DHT                       None       8     3     112      The location of the node
    0225/0001  tutorial1__ambiance       sensor                         0    11                        None       4     3     112      The sensor type : 11,22,2302
    0225/0000  tutorial1                 tutorial1_temperature_poll     0    300                       seconds    4     3     112      The poll delay of the value
    0225/0000  tutorial1                 name                           0    Hello world               None       8     3     112      The name of the node
    0225/0000  tutorial1                 location                       0    Rapsberry                 None       8     3     112      The location of the node
    0225/0003  tutorial1__cpu            frequency_poll                 0    300                       seconds    4     3     112      The poll delay of the value
    0225/0003  tutorial1__cpu            temperature_poll               0    300                       seconds    4     3     112      The poll delay of the value
    0225/0003  tutorial1__cpu            voltage_poll                   0    300                       seconds    4     3     112      The poll delay of the value
    0225/0003  tutorial1__cpu            location                       0    Hostsensor                None       8     3     112      The location of the node
    0225/0003  tutorial1__cpu            name                           0    CPU                       None       8     3     112      The name of the node
    0225/0002  tutorial1__temperature    temperature_poll               0    300                       seconds    4     3     112      The poll delay of the value
    0225/0002  tutorial1__temperature    location                       0    Onewire                   None       8     3     112      The location of the node
    0225/0002  tutorial1__temperature    hexadd                         0    28-00000463b745           None       8     3     112      The hexadecimal address of the DS18B20
    0225/0002  tutorial1__temperature    name                           0    Temperature               None       8     3     112      The name of the node

Get the user values :

.. code:: bash

    $ jnt_query node --hadd 0225/0000 --vuuid request_info_users

.. code:: bash

    hadd       node_uuid                 uuid                           idx  data                      units      type  genre cmdclass help
    0225/0001  tutorial1__ambiance       temperature                    0    19.0                      °C         3     2     49       The temperature
    0225/0001  tutorial1__ambiance       humidity                       0    30.0                      %          3     2     49       The humidity
    0225/0000  tutorial1                 tutorial1_temperature          0    25.6                      °C         3     2     49       The average temperature of tutorial. Can be use as a good quality source for a thermostat.
    0225/0003  tutorial1__cpu            frequency                      0    1000                      MHz        3     2     49       The frequency of the CPU
    0225/0003  tutorial1__cpu            voltage                        0    1.35                      V          3     2     49       The voltage of the CPU
    0225/0003  tutorial1__cpu            temperature                    0    38.5                      °C         3     2     49       The temperature of the CPU
    0225/0002  tutorial1__temperature    temperature                    0    19.2                      °C         3     2     49       The temperature


Performances
============

.. code:: bash

    $ nice top

.. code:: bash

    PID   USER      PR  NI  VIRT  RES  SHR S  %CPU %MEM    TIME+  COMMAND
    3050 root      20   0 59340  13m 4288 S   2,3  2,7   1:30.00 /usr/bin/python /usr/local/bin/jnt_tutorial -c /opt/janitoo/src/janitoo_tutorial/tests/data/helloworldv

We divide the virtual memory by 2. Reserved memory is also less.
