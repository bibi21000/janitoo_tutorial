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
