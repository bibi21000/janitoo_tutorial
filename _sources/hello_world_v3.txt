============
HelloWord V3
============


Explanations
============

For this last example, we will create a more sophisticated server : it will

 - calculate the average temperature
 - report its state via a led
 - use a finish state machine (fsm)


The bus
=======

Components and thread are defined the same way we did in the previous tutorial

The bus is now based on a fsm (Look at https://github.com/tyarkoni/transitions for more documentation)

At first, we must define state and transitions :

.. code:: python

    states = [
       'sleeping',
       'reporting',
       'ringing',
    ]
    """The tutorial states :
    """

    transitions = [
        { 'trigger': 'wakeup',
            'source': '*',
            'dest': 'reporting',
        },
        { 'trigger': 'report',
            'source': '*',
            'dest': 'reporting',
        },
        { 'trigger': 'sleep',
            'source': '*',
            'dest': 'sleeping',
        },
        { 'trigger': 'ring',
            'source': 'reporting',
            'dest': 'ringing',
        },
    ]

And start / stop the fsm when starting/stopping the bus :

.. code:: python

    def start(self, mqttc, trigger_thread_reload_cb=None):
        """Start the bus
        """
        for bus in self.buses:
            self.buses[bus].start(mqttc, trigger_thread_reload_cb=None)
        JNTBus.start(self, mqttc, trigger_thread_reload_cb)
        self._tutorial_statemachine =  Machine(self,
            states=self.states,
            transitions=self.transitions,
            initial='sleeping')

    def stop(self):
        """Stop the bus
        """
        self.stop_check()
        self.sleep()
        for bus in self.buses:
            self.buses[bus].stop()
        JNTBus.stop(self)

We should now define actions when entering states :

.. code:: python

    def on_enter_reporting(self):
        """
        """
        logger.debug("[%s] - on_enter_reporting", self.__class__.__name__)
        self.bus_acquire()
        try:
            self.nodeman.find_value('led', 'blink').data = 'heartbeat'
            self.nodeman.add_polls(self.polled_sensors, slow_start=True, overwrite=False)
        except:
            logger.exception("[%s] - Error in on_enter_reporting", self.__class__.__name__)
        finally:
            self.bus_release()
        self.on_check()

    def on_enter_ringing(self):
        """
        """
        logger.debug("[%s] - on_enter_ringing", self.__class__.__name__)
        self.bus_acquire()
        try:
            self.nodeman.find_value('led', 'blink').data = 'warning'
        except:
            logger.exception("[%s] - Error in on_enter_ringing", self.__class__.__name__)
        finally:
            self.bus_release()

    ...

The finish state machine
========================

FSM

.. image:: images/fsm_bus.png


Spy it
======

Open a new shell and launch

.. code:: bash

    jnt_spy

This will launch a spyer for the mqtt protocol :

.. code:: bash

Go to the first terminal and launch ther server if needed :

.. code:: bash

    sudo jnt_raspberry -c /opt/janitoo/etc/helloworldv3.conf start

You can look at the protocol during startup on the spyer terminal.

You can also look at logs. In a new terminal :

.. code:: bash

    tail -n 100 -f /opt/janitoo/log/helloworldv3.log

Its time to query ther server. Go to the first terminal and query the network :

.. code:: bash

    jnt_query network

You should receive the list of nodes availables on your server :

.. code:: bash

    hadd       uuid                 name                      location                  product_type
    hadd       uuid                 name                      location                  product_type
    0225/0000  tutorial2            Hello world               Rapsberry                 Default product type
    0225/0002  tutorial2__temperature Temperature               Onewire                   Temperature sensor
    0225/0004  tutorial2__led       Led                       GPIO                      Software
    0225/0003  tutorial2__cpu       CPU                       Hostsensor                Software component
    0225/0001  tutorial2__ambiance  Ambiance 1                DHT                       Temperature/humidity sensor

You can also query a node :

.. code:: bash

    jnt_query node --hadd 0225/0000

.. code:: bash

Check the config values :

.. code:: bash

    jnt_query node --hadd 0225/0000 --vuuid request_info_configs

.. code:: bash

    hadd       node_uuid                 uuid                           idx  data                      units      type  genre cmdclass help
    0225/0004  tutorial2__led            switch_poll                    0    300                       seconds    4     3     112      The poll delay of the value
    0225/0004  tutorial2__led            blink_poll                     0    300                       seconds    4     3     112      The poll delay of the value
    0225/0004  tutorial2__led            location                       0    GPIO                      None       8     3     112      The location of the node
    0225/0004  tutorial2__led            pin                            0    1                         None       4     3     112      The pin number on the board
    0225/0004  tutorial2__led            name                           0    Led                       None       8     3     112      The name of the node
    0225/0001  tutorial2__ambiance       temperature_poll               0    300                       seconds    4     3     112      The poll delay of the value
    0225/0001  tutorial2__ambiance       name                           0    Ambiance 1                None       8     3     112      The name of the node
    0225/0001  tutorial2__ambiance       pin                            0    6                         None       4     3     112      The pin number on the board
    0225/0001  tutorial2__ambiance       humidity_poll                  0    300                       seconds    4     3     112      The poll delay of the value
    0225/0001  tutorial2__ambiance       location                       0    DHT                       None       8     3     112      The location of the node
    0225/0001  tutorial2__ambiance       sensor                         0    11                        None       4     3     112      The sensor type : 11,22,2302
    0225/0000  tutorial2                 tutorial2_temperature_poll     0    300                       seconds    4     3     112      The poll delay of the value
    0225/0000  tutorial2                 tutorial2_temperature_critical 0    50                        None       4     3     112      The critical temperature. If 2 of the 3 temperature sensors are up to this value, a security notification is sent.
    0225/0000  tutorial2                 location                       0    Rapsberry                 None       8     3     112      The location of the node
    0225/0000  tutorial2                 name                           0    Hello world               None       8     3     112      The name of the node
    0225/0000  tutorial2                 tutorial2_timer_delay          0    45                        None       4     3     112      The delay between 2 checks
    0225/0003  tutorial2__cpu            frequency_poll                 0    30                        seconds    4     3     112      The poll delay of the value
    0225/0003  tutorial2__cpu            temperature_poll               0    30                        seconds    4     3     112      The poll delay of the value
    0225/0003  tutorial2__cpu            voltage_poll                   0    30                        seconds    4     3     112      The poll delay of the value
    0225/0003  tutorial2__cpu            location                       0    Hostsensor                None       8     3     112      The location of the node
    0225/0003  tutorial2__cpu            name                           0    CPU                       None       8     3     112      The name of the node
    0225/0002  tutorial2__temperature    temperature_poll               0    300                       seconds    4     3     112      The poll delay of the value
    0225/0002  tutorial2__temperature    location                       0    Onewire                   None       8     3     112      The location of the node
    0225/0002  tutorial2__temperature    hexadd                         0    28-00000463b745           None       8     3     112      The hexadecimal address of the DS18B20
    0225/0002  tutorial2__temperature    name                           0    Temperature               None       8     3     112      The name of the node

Get the user values :

.. code:: bash

    jnt_query node --hadd 0225/0000 --vuuid request_info_users

.. code:: bash

    hadd       node_uuid                 uuid                           idx  data                      units      type  genre cmdclass help
    0225/0001  tutorial2__ambiance       temperature                    0    19.0                      °C         3     2     49       The temperature
    0225/0001  tutorial2__ambiance       humidity                       0    24.0                      %          3     2     49       The humidity
    0225/0000  tutorial2                 tutorial2_temperature          0    None                      °C         3     2     49       The average temperature of tutorial.
    0225/0000  tutorial2                 tutorial2_state                0    sleeping                  None       8     2     49       The state of the machine.
    0225/0000  tutorial2                 tutorial2_change               0    None                      None       8     2     0        Change the state of the machine.
    0225/0003  tutorial2__cpu            frequency                      0    1000                      MHz        3     2     49       The frequency of the CPU
    0225/0003  tutorial2__cpu            voltage                        0    1.35                      V          3     2     49       The voltage of the CPU
    0225/0003  tutorial2__cpu            temperature                    0    37.9                      °C         3     2     49       The temperature of the CPU
    0225/0002  tutorial2__temperature    temperature                    0    19.5                      °C         3     2     49       The temperature

Performances
============

.. code:: bash

    nice top

.. code:: bash

    PID   USER      PR  NI  VIRT  RES  SHR S  %CPU %MEM    TIME+  COMMAND
    24126 root      20   0 59352  13m 4292 S   5,9  2,7   0:38.28 /usr/bin/python /usr/local/bin/jnt_tutorial -c /opt/janitoo/src/janitoo_tutorial/tests/data/helloworldv
