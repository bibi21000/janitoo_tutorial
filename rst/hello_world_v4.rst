============
HelloWord V4
============


Goal
====

Back to our Rapsberry pi server : .
For the impatient that did not use a raspberry, you can jump :doc:`here <more>`

State machine
=============

Look at the spyer. At startup, the server publish all its values but after a while it became silently :

.. code:: bash

    /values/user/0225/0003/voltage 0 {"help": "The voltage of the CPU", "voice_uuid": null, "max": null, "reply_hadd": null, "node_uuid": "tutorial2__cpu", "entry
    _name": "sensor_voltage", "genre": 2, "poll_delay": 300, "data": 1.35, "is_polled": true, "is_writeonly": false, "list_items": null, "index": 0, "uuid": "volt
    age", "is_readonly": true, "min": null, "default": null, "type": 3, "cmd_class": 49, "hadd": "0225/0003", "label": "CPUVolt", "units": "V"}
    /values/user/0225/0002/temperature 0 {"help": "The temperature", "voice_uuid": null, "max": null, "reply_hadd": null, "node_uuid": "tutorial2__temperature", "
    entry_name": "sensor_temperature", "genre": 2, "poll_delay": 300, "data": 85.0, "is_polled": true, "is_writeonly": false, "list_items": null, "index": 0, "uui
    d": "temperature", "is_readonly": true, "min": null, "default": null, "type": 3, "cmd_class": 49, "hadd": "0225/0002", "label": "Temp", "units": "\u00b0C"}
    /dhcp/heartbeat/0225/0002 0 ONLINE
    /dhcp/heartbeat/0225/0004 0 ONLINE
    /dhcp/heartbeat/0225/0003 0 ONLINE
    /dhcp/heartbeat/0225/0001 0 ONLINE
    /dhcp/heartbeat/0225/0000 0 ONLINE
    /dhcp/heartbeat/0225/0002 0 ONLINE
    /dhcp/heartbeat/0225/0004 0 ONLINE
    /dhcp/heartbeat/0225/0003 0 ONLINE
    /dhcp/heartbeat/0225/0001 0 ONLINE
    /dhcp/heartbeat/0225/0000 0 ONLINE
    /values/user/0225/0000/tutorial2_state 0 {"help": "The state of the fsm.", "voice_uuid": null, "max": null, "reply_hadd": null, "node_uuid": "tutorial2", "entry_name": "sensor_string", "genre": 2, "poll_delay": 900, "data": "sleeping", "is_polled": true, "is_writeonly": false, "list_items": null, "index": 0, "uuid": "tutorial2_state", "is_readonly": true, "min": null, "default": null, "type": 8, "cmd_class": 49, "hadd": "0225/0000", "label": "State", "units": null}
    /dhcp/heartbeat/0225/0002 0 ONLINE
    /dhcp/heartbeat/0225/0004 0 ONLINE
    /dhcp/heartbeat/0225/0003 0 ONLINE
    /dhcp/heartbeat/0225/0001 0 ONLINE
    /dhcp/heartbeat/0225/0000 0 ONLINE
    /dhcp/heartbeat/0225/0002 0 ONLINE
    /dhcp/heartbeat/0225/0004 0 ONLINE
    /dhcp/heartbeat/0225/0003 0 ONLINE
    /dhcp/heartbeat/0225/0001 0 ONLINE
    /dhcp/heartbeat/0225/0000 0 ONLINE

That's because we enter in mode sleep. As publish in the last value : "data": "sleeping". And we publish this value every 900seconds : "poll_delay": 900.

That's done in the check_heartbeat method :

.. code:: python

    def check_heartbeat(self):
        """Check that the component is 'available'

        """
        res = False
        #~ for bus in self.buses:
            #~ res = res and self.buses[bus].check_heartbeat()
        logger.debug("[%s] - sensors %s", self.__class__.__name__, self.polled_sensors)
        if self.state == 'booting' and all(v is not None for v in self.polled_sensors):
            #We try to enter in sleeping mode
            self.sleep()
        return self.state != 'booting'

That's not the fastest way to dot it but not the worst. We need to check that all nodes are up before changing of state.
If the state is not change, the node associated to the bus will send an 'OFFLINE' heartbeat.

.. code:: python

    def start_sleeping(self):
        """
        """
        logger.debug("[%s] - start_sleeping", self.__class__.__name__)
        self.stop_check()
        self.bus_acquire()
        res = True
        try:
            self.nodeman.remove_polls(self.polled_sensors)
            self.nodeman.find_value('led', 'blink').data = 'off'
            #In sleeping mode, send the state of the fsm every 900 seconds
            #We update poll_delay directly to nto update the value in config file
            self.nodeman.find_bus_value('state').poll_delay = 900
        except Exception:
            logger.exception("[%s] - Error in start_sleeping", self.__class__.__name__)
            res = False
        finally:
            self.bus_release()
        return res

We do the same for the other transition conditions.

Wake up baby
============

It's time to wake-up the state machine. At first, we need to find the right value :

.. code: bash

    $ jnt_query node --hadd 0225/0000 --vuuid request_info_basics

.. code: bash

    request_info_basics
    ----------
    hadd       uuid                           idx  data                      units      type  genre cmdclass help
    0225/0004  switch                         0    off                       None       5     1     37       A switch. Valid values are : ['on', 'off']
    0225/0004  blink                          0    off                       None       5     1     12803    Blink
    0225/0000  tutorial2_transition           0    None                      None       5     1     0        Send a transition to the fsm

Get more informations on this value :

.. code: bash

    $ jnt_query query --host=192.168.14.65 --hadd 0225/0000 --genre basic --uuid tutorial2_transition --cmdclass 4272 --type 1 --readonly True

.. code: bash

    tutorial2_transition
    ----------
    hadd       uuid                      idx  data                      units      type  genre cmdclass list_items help
    0225/0000  tutorial2_transition      0    None                      None       5     1     4272     [u'wakeup', u'report', u'sleep', u'ring'] Trigger a transition on the fsm or get the last triggered

And trigger a transition from [u'wakeup', u'report', u'sleep', u'ring'] :

.. code: bash

    $ jnt_query query --host=192.168.14.65 --hadd 0225/0000 --genre basic --uuid tutorial2_transition --cmdclass 4272 --type 1 --writeonly True --data wakeup

.. code: bash

    tutorial2_transition
    ----------
    hadd       uuid                      idx  data                      units      type  genre cmdclass list_items help
    0225/0000  tutorial2_transition      0    wakeup                    None       5     1     4272     [u'wakeup', u'report', u'sleep', u'ring'] Trigger a transition on the fsm or get the last triggered

Look at spyer :

.. code: bash

    /values/user/0225/0003/frequency 0 {"help": "The frequency of the CPU", "voice_uuid": null, "max": null, "reply_hadd": null, "node_uuid": "tutorial2__cpu", "entry_name": "sensor_frequency", "genre": 2, "poll_delay": 300, "data": 1000, "is_polled": true, "is_writeonly": false, "list_items": null, "index": 0, "uuid": "frequency", "is_readonly": true, "min": null, "default": null, "type": 3, "cmd_class": 49, "hadd": "0225/0003", "label": "CPUFreq", "units": "MHz"}
    /values/basic/0225/0004/blink 0 {"help": "Blink", "reply_hadd": null, "entry_name": "blink", "poll_delay": 300, "is_writeonly": false, "list_items": null, "index": 0, "uuid": "blink", "min": null, "delays": {"info": {"on": 0.6, "off": 60}, "off": {"on": 0, "off": 1}, "blink": {"on": 0.6, "off": 2.5}, "warning": {"on": 0.6, "off": 5}, "notify": {"on": 0.6, "off": 10}, "heartbeat": {"on": 0.5, "off": 300}, "alert": {"on": 0.6, "off": 1}}, "cmd_class": 12803, "hadd": "0225/0004", "label": "Blink", "units": null, "type": 5, "max": null, "genre": 1, "data": "heartbeat", "is_polled": true, "node_uuid": "tutorial2__led", "voice_uuid": null, "is_readonly": false, "default": "off"}
    /values/user/0225/0000/tutorial2_temperature 0 {"help": "The average temperature of tutorial.", "voice_uuid": null, "max": null, "reply_hadd": null, "node_uuid": "tutorial2", "entry_name": "sensor_temperature", "genre": 2, "poll_delay": 300, "data": null, "is_polled": true, "is_writeonly": false, "list_items": null, "index": 0, "uuid": "tutorial2_temperature", "is_readonly": true, "min": null, "default": null, "type": 3, "cmd_class": 49, "hadd": "0225/0000", "label": "Temp", "units": "\u00b0C"}
    /values/basic/0225/0000/tutorial2_transition 0 {"help": "Trigger a transition on the fsm or get the last triggered", "voice_uuid": null, "max": null, "reply_hadd": null, "node_uuid": "tutorial2", "entry_name": "transition_fsm", "genre": 1, "poll_delay": 60, "data": "wakeup", "is_polled": true, "is_writeonly": false, "list_items": ["wakeup", "report", "sleep", "ring"], "index": 0, "uuid": "tutorial2_transition", "is_readonly": false, "min": null, "default": null, "cmd_class": 4272, "hadd": "0225/0000", "label": "Transit", "units": null, "type": 5}
    /nodes/0225/0000/request 0 {"reply_hadd": "9999/9990", "uuid": "tutorial2_transition", "is_readonly": true, "genre": 1, "data": null, "cmd_class": 4272, "hadd": "0225/0000", "is_writeonly": false}
    /nodes/9999/9990/reply 0 {"help": "Trigger a transition on the fsm or get the last triggered", "voice_uuid": null, "max": null, "reply_hadd": "9999/9990", "node_uuid": "tutorial2", "entry_name": "transition_fsm", "genre": 1, "poll_delay": 60, "data": "wakeup", "is_polled": true, "is_writeonly": false, "list_items": ["wakeup", "report", "sleep", "ring"], "index": 0, "uuid": "tutorial2_transition", "is_readonly": true, "min": null, "default": null, "cmd_class": 4272, "hadd": "0225/0000", "label": "Transit", "units": null, "type": 5}
    /values/basic/0225/0000/tutorial2_transition 0 {"help": "Trigger a transition on the fsm or get the last triggered", "voice_uuid": null, "max": null, "reply_hadd": "9999/9990", "node_uuid": "tutorial2", "entry_name": "transition_fsm", "genre": 1, "poll_delay": 60, "data": "wakeup", "is_polled": true, "is_writeonly": false, "list_items": ["wakeup", "report", "sleep", "ring"], "index": 0, "uuid": "tutorial2_transition", "is_readonly": true, "min": null, "default": null, "cmd_class": 4272, "hadd": "0225/0000", "label": "Transit", "units": null, "type": 5}
    /dhcp/heartbeat/0225/0000 0 ONLINE
    /dhcp/heartbeat/0225/0002 0 ONLINE
    /dhcp/heartbeat/0225/0004 0 ONLINE
    /dhcp/heartbeat/0225/0003 0 ONLINE
    /dhcp/heartbeat/0225/0001 0 ONLINE
    /dhcp/heartbeat/0225/0000 0 ONLINE
    /dhcp/heartbeat/0225/0002 0 ONLINE
    /values/user/0225/0000/tutorial2_state 0 {"help": "The state of the fsm.", "voice_uuid": null, "max": null, "reply_hadd": null, "node_uuid": "tutorial2", "entry_name": "sensor_string", "genre": 2, "poll_delay": 60, "data": "reporting", "is_polled": true, "is_writeonly": false, "list_items": null, "index": 0, "uuid": "tutorial2_state", "is_readonly": true, "min": null, "default": null, "type": 8, "cmd_class": 49, "hadd": "0225/0000", "label": "State", "units": null}

The values are published regulary. You should also see your led blinking in heartbeat mode.

A note ont the state machine. Writing this tutorial, I added a new bus with an integrated state machine : https://github.com/bibi21000/janitoo_factory/blob/master/src/janitoo_factory/buses/fsm.py.
It's a better idea to inherit from it.


Critical temperature
====================

We want to notify when a temperature decome to much higher. To do that, we add a threadtimer that will check temperatures.
If a temperature is higher than the critical one, we transit in ringing mode.

The on_check timer is started when entering in "reporting" state :

.. code:: python

    def start_reporting(self):
        """
        """
        logger.debug("[%s] - start_reporting", self.__class__.__name__)
        self.bus_acquire()
        res = True
        try:
            self.nodeman.find_value('led', 'blink').data = 'heartbeat'
            self.nodeman.add_polls(self.polled_sensors, slow_start=True, overwrite=False)
            #In sleeping mode, send the state of the fsm every 900 seconds
            #We update poll_delay directly to not update the value in configfile
            state = self.nodeman.find_bus_value('state')
            state.poll_delay = self.nodeman.find_bus_value('state_poll').data
            overheat = self.nodeman.find_bus_value('overheat')
            overheat.poll_delay = self.nodeman.find_bus_value('overheat_poll').data
            self.nodeman.publish_value(overheat)
            self.nodeman.add_polls([state, overheat], slow_start=True, overwrite=True)
        except Exception:
            logger.exception("[%s] - Error in start_reporting", self.__class__.__name__)
            res = False
        finally:
            self.bus_release()
        self.on_check()
        return res

We also publish the overheat value :

.. code:: python

        overheat = self.nodeman.find_bus_value('overheat')
        overheat.poll_delay = self.nodeman.find_bus_value('overheat_poll').data
        self.nodeman.publish_value(overheat)

The overheat value is updated in the on_check timer :

.. code:: python

        if criticals > 1:
            if self.state != 'ringing':
                #We should notify a security problem : fire ?
                self.nodeman.find_bus_value('overheat').data = True
                self.ring()
        elif self.state == 'ringing':
            #We should notify a security problem : fire ?
            self.nodeman.find_bus_value('overheat').data = False
            self.report()

In ringing state, we are more verbose :

.. code:: python

    def start_ringing(self):
        """
        """
        logger.debug("[%s] - start_ringing", self.__class__.__name__)
        self.bus_acquire()
        res = True
        try:
            self.nodeman.find_value('led', 'blink').data = 'warning'
            #In sleeping mode, send the state of the fsm every 900 seconds
            #We update poll_delay directly to not update the value in configfile
            state = self.nodeman.find_bus_value('state')
            state.poll_delay = self.nodeman.find_bus_value('state_poll').data / 3
            overheat = self.nodeman.find_bus_value('overheat')
            overheat.poll_delay = self.nodeman.find_bus_value('overheat_poll').data / 3
            self.nodeman.publish_value(overheat)
            self.nodeman.add_polls([state, overheat], slow_start=True, overwrite=True)
        except Exception:
            logger.exception("[%s] - Error in start_ringing", self.__class__.__name__)
            res = False
        finally:
            self.bus_release()
        return res

We also check temperature more frequently :

.. code:: python

    if self.check_timer is None and self.is_started:
        timer_delay = self.get_bus_value('timer_delay').data
        if self.state == 'ringing':
            timer_delay = timer_delay / 2
        self.check_timer = threading.Timer(timer_delay, self.on_check)
        self.check_timer.start()

It's time to ring :

.. code:: bash

    $ jnt_query query --host=192.168.14.65 --hadd 0225/0000 --genre basic --uuid tutorial2_transition --cmdclass 4272 --type 1 --writeonly True --data wakeup

And check the result :

.. code:: bash


    $ jnt_query node --host=192.168.14.65 --hadd 0225/0000 --vuuid request_info_basics
    ----------
    hadd       uuid                           idx  data                      units      type  genre cmdclass help
    0225/0004  switch                         0    off                       None       5     1     37       A switch. Valid values are : ['on', 'off']
    0225/0004  blink                          0    warning                   None       5     1     12803    Blink
    0225/0000  tutorial2_transition           0    ring                      None       5     1     4272     Trigger a transition on the fsm or get the last triggered
    0225/0000  tutorial2_state                0    ringing                   None       8     1     49       The state of the fsm.
