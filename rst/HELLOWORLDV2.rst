============
HelloWord V2
============


Explanations
============

For this second example, we will create a more sophisticated server : it will calculate the average temperature and send it.

The components
==============

Change to the tutorial directory :

.. code:: bash

    cd /opt/janitoo/src/janitoo_tutorial

Open the tutorial1 implementation :

.. code:: bash

    vim src/janitoo_tutorial/tutorial1.py

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


Configuration
=============

Open the test configuration file in your favorite editor :

.. code:: bash

    vim tests/data/helloworldv2.conf

Like seen in the first tutorial, there is a section for the new bus (thread) :

.. code:: bash

    [tutorial1]
    auto_start = True
    name = Hello world
    location = Rapsberry
    components.ambiance = tutorial1.dht
    components.temperature = tutorial1.ds18b20
    components.cpu = tutorial1.picpu
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

You're ready to test your components. Create a test :

.. code:: bash

    vim tests/test_component_v2.py

.. code:: bash

    class TestAmbianceComponent(JNTTComponent, JNTTComponentCommon):
        """Test the component
        """
        component_name = "tutorial1.ambiance"

And launch it :

.. code:: bash

    sudo nosetests tests/test_component_v2.py -v

Same for the tread (bus) :

.. code:: bash

    vim tests/test_thread_v2.py

.. code:: bash

    class TestTutorialThread(JNTTThreadRun, JNTTThreadRunCommon):
        """Test the thread
        """
        thread_name = "tutorial1"
        conf_file = "tests/data/janitoo_tutorial2.conf"

And launch it :

.. code:: bash

    sudo nosetests tests/test_thread_v2.py -v

And for the server :

.. code:: bash

    vim tests/test_server_v2.py

.. code:: bash

    class TestTutorialServer(JNTTServer, JNTTServerCommon):
        """Test the tutorial server
        """
        server_class = PiServer
        server_conf = "tests/data/helloworldv3.conf"

        hadds = [HADD%(225,0), HADD%(225,1), HADD%(225,2), HADD%(225,3)]

And launch it :

.. code:: bash

    sudo nosetests tests/test_server_v1.py -v -m test_040_server_start_no_error_in_log

If everything is ok, the screen output should be something like this :

.. code:: bash

    test_040_server_start_no_error_in_log (tests.test_server_v1.TestTutorialServer) ... ok
    ----------------------------------------------------------------------
    Ran 1 test in 128.712s

    OK

Otherwise you should have a log capture with surely some errors inside.

You can also the whole tests, which whould help you to fix problems :

.. code:: bash

    sudo make tests

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


Spy it
======

Open a new shell and launch

.. code:: bash

    jnt_spy

This will launch a spyer for the mqtt protocol :

.. code:: bash

Go to the first terminal and launch ther server if needed :

.. code:: bash

    sudo jnt_raspberry -c /opt/janitoo/etc/helloworldv1.conf start

You can look at the protocol during startup on the spyer terminal.

You can also look at logs. In a new terminal :

.. code:: bash

    tail -n 100 -f /opt/janitoo/log/helloworldv1.log

Its time to query ther server. Go to the first terminal and query the network :

.. code:: bash

    jnt_query network

You should receive the list of nodes availables on your server :

.. code:: bash

    hadd       uuid                 name                      location                  product_type
    1111/0000  939477c767b8         testname                  testlocation              RGB LED and Temperature (v 0.06)

You can also query a node :

.. code:: bash

    jnt_query node --hadd 0222/0000

.. code:: bash


Performances
============

.. code:: bash

    nice top

.. code:: bash

    PID   USER      PR  NI  VIRT  RES  SHR S  %CPU %MEM    TIME+  COMMAND
    275   root      20   0     0    0    0 S  24,9  0,0 137:12.31 [w1_bus_master1]
    10016 root      20   0 94388  20m 7240 S   1,6  4,2  10:23.43 /usr/bin/python /usr/local/bin/jnt_fishtank -c /opt/janitoo/etc/jnt_fishtank.conf restart
