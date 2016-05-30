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

That's not the fastest way to do it but not the worst. We need to check that all nodes are up before changing of state.
If the state is not change, the node associated to the bus will send an 'OFFLINE' heartbeat.

We add a condition for the state machine : values needs to be up to change the state. Of course, no need to check conditions to get into sleeping state.

.. code:: python

    def condition_values(self):
        """
        """
        logger.debug("[%s] - condition_values", self.__class__.__name__)
        return all(v is not None for v in self.polled_sensors)

And we add on_enter_{state} functions. For example, when entering in reporting mode, we activate the polls  :

.. code:: python

    def on_enter_reporting(self):
        """
        """
        logger.debug("[%s] - on_enter_reporting", self.__class__.__name__)
        self.bus_acquire()
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
            logger.exception("[%s] - Error in on_enter_reporting", self.__class__.__name__)
        finally:
            self.bus_release()

We also publish the overheat value immediatly :

.. code:: python

    self.nodeman.publish_value(overheat)

It's time to add some code to interact with the state machine ... and speak about the value_factory.
Values are used to interact with nodes : update config, poll, location, get temperature, ...
To allow developpers to share these interactions, there is the value factory.
You can collect values in your local values factory using :

.. code:: bash

    jnt_collect -t janitoo.values

.. code:: bash
    -------------------------------------------------------------------------------
    Group : janitoo.values
     action_boolean = janitoo_factory.values.action:make_action_boolean
     action_byte = janitoo_factory.values.action:make_action_byte
     action_integer = janitoo_factory.values.action:make_action_integer
     action_list = janitoo_factory.values.action:make_action_list
     action_string = janitoo_factory.values.action:make_action_string
     action_switch_binary = janitoo_factory.values.action:make_action_switch_binary
     action_switch_multilevel = janitoo_factory.values.action:make_action_switch_multilevel
     blink = janitoo_factory_exts.values.blink:make_blink
     config_array = janitoo_factory.values.config:make_config_array
     config_boolean = janitoo_factory.values.config:make_config_boolean
     ...
     sensor_rotation_speed = janitoo_factory.values.sensor:make_sensor_rotation_speed
     sensor_string = janitoo_factory.values.sensor:make_sensor_string
     sensor_temperature = janitoo_factory.values.sensor:make_sensor_temperature
     sensor_voltage = janitoo_factory.values.sensor:make_sensor_voltage
     transition_fsm = janitoo_factory.values.action:make_transition_fsm
     updown = janitoo_factory_exts.values.updown:make_updown

For example, the value sensor_temperature is used to send a temperature :D
It defines the right units, command class, label, ...

We want to interact with the finish state machine, so transition_fsm is a good choice :

.. code:: python

    uuid="{:s}_transition".format(OID)
    self.values[uuid] = self.value_factory['transition_fsm'](options=self.options, uuid=uuid,
        node_uuid=self.uuid,
        list_items=[ v['trigger'] for v in self.transitions ],
        fsm_bus=self,
    )
    poll_value = self.values[uuid].create_poll_value()
    self.values[poll_value.uuid] = poll_value

We defined a new value using 'transition_fsm' with a list of valid items populated from the transition state machine and a refrence to the bus itself.
And that's all. All the job is done automatically : `here <https://github.com/bibi21000/janitoo_factory/blob/master/src/janitoo_factory/values/action.py#L230>`_

As we want to poll this value, we also add a linked poll value.


Wake up baby
============

It's time to wake-up the state machine. At first, we need to find the right value :

.. code:: bash

    $ jnt_query node --hadd 0225/0000 --vuuid request_info_basics

.. code:: bash

    request_info_basics
    ----------
    hadd       uuid                           idx  data                      units      type  genre cmdclass help
    0225/0004  switch                         0    off                       None       5     1     37       A switch. Valid values are : ['on', 'off']
    0225/0004  blink                          0    off                       None       5     1     12803    Blink
    0225/0000  tutorial2_transition           0    None                      None       5     1     0        Send a transition to the fsm

Get more informations on this value :

.. code:: bash

    $ jnt_query query --host=192.168.14.65 --hadd 0225/0000 --genre basic --uuid tutorial2_transition --cmdclass 4272 --type 1 --readonly True

.. code:: bash

    tutorial2_transition
    ----------
    hadd       uuid                      idx  data                      units      type  genre cmdclass list_items help
    0225/0000  tutorial2_transition      0    None                      None       5     1     4272     [u'wakeup', u'report', u'sleep', u'ring'] Trigger a transition on the fsm or get the last triggered

And trigger a transition from [u'wakeup', u'report', u'sleep', u'ring'] :

.. code:: bash

    $ jnt_query query --host=192.168.14.65 --hadd 0225/0000 --genre basic --uuid tutorial2_transition --cmdclass 4272 --type 1 --writeonly True --data wakeup

.. code:: bash

    tutorial2_transition
    ----------
    hadd       uuid                      idx  data                      units      type  genre cmdclass list_items help
    0225/0000  tutorial2_transition      0    wakeup                    None       5     1     4272     [u'wakeup', u'report', u'sleep', u'ring'] Trigger a transition on the fsm or get the last triggered

Look at spyer :

.. code:: bash

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

A note ont the state machine.
Writing this tutorial, I added a new bus with an integrated state machine : `here <https://github.com/bibi21000/janitoo_factory/blob/master/src/janitoo_factory/buses/fsm.py>`_.
It's a better idea to inherit from it. It use a timer to speed up the boot process.


Critical temperature
====================

We want to notify when a temperature become critical. To do that, we add 2 values and a thread timer that will check temperatures.
If a temperature is higher than the critical one, we transit in ringing mode.

The on_check timer start/stop is managed entering / exiting the sleeping state :

.. code:: python

    def on_enter_sleeping(self):
        """
        """
        logger.debug("[%s] - on_enter_sleeping", self.__class__.__name__)
        self.bus_acquire()
        try:
            self.stop_check()
            self.nodeman.remove_polls(self.polled_sensors)
            self.nodeman.find_value('led', 'blink').data = 'off'
            #In sleeping mode, send the state of the fsm every 900 seconds
            #We update poll_delay directly to nto update the value in config file
            self.nodeman.find_bus_value('state').poll_delay = 900
        except Exception:
            logger.exception("[%s] - Error in on_enter_sleeping", self.__class__.__name__)
        finally:
            self.bus_release()

    def on_exit_sleeping(self):
        """
        """
        logger.debug("[%s] - on_exit_sleeping", self.__class__.__name__)
        self.on_check()

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

    def on_enter_ringing(self):
        """
        """
        logger.debug("[%s] - on_enter_ringing", self.__class__.__name__)
        self.bus_acquire()
        try:
            self.nodeman.find_value('led', 'blink').data = 'warning'
            #In sleeping mode, send the state of the fsm every 900 seconds
            #We update poll_delay directly to not update the value in configfile
            state = self.nodeman.find_bus_value('state')
            state.poll_delay = 1.0 * self.nodeman.find_bus_value('state_poll').data / 3
            overheat = self.nodeman.find_bus_value('overheat')
            overheat.poll_delay = 1.0 * self.nodeman.find_bus_value('overheat_poll').data / 3
            self.nodeman.publish_value(overheat)
            self.nodeman.add_polls([state, overheat], slow_start=True, overwrite=True)
        except Exception:
            logger.exception("[%s] - Error in on_enter_ringing", self.__class__.__name__)
        finally:
            self.bus_release()

We also launch the on_check temperature more frequently :

.. code:: python

    if self.check_timer is None and self.is_started:
        timer_delay = self.get_bus_value('timer_delay').data
        if self.state == 'ringing':
            timer_delay = timer_delay / 2
        self.check_timer = threading.Timer(timer_delay, self.on_check)
        self.check_timer.start()

It's time to ring :

.. code:: bash

    $ jnt_query query --host=192.168.14.65 --hadd 0225/0000 --genre basic --uuid tutorial2_transition --cmdclass 4272 --type 1 --writeonly True --data ring

And check that the state is ringing. You can also look at your led, should blink faster :

.. code:: bash

    $ jnt_query node --host=192.168.14.65 --hadd 0225/0000 --vuuid request_info_basics

.. code:: bash

    ----------
    hadd       uuid                           idx  data                      units      type  genre cmdclass help
    0225/0004  switch                         0    off                       None       5     1     37       A switch. Valid values are : ['on', 'off']
    0225/0004  blink                          0    warning                   None       5     1     12803    Blink
    0225/0000  tutorial2_transition           0    ring                      None       5     1     4272     Trigger a transition on the fsm or get the last triggered
    0225/0000  tutorial2_state                0    ringing                   None       8     1     49       The state of the fsm.

After a while, the state returns in reporting state :

.. code:: bash

    $ jnt_query node --host=192.168.14.65 --hadd 0225/0000 --vuuid request_info_basicsrequest_info_basics

.. code:: bash

    ----------
    hadd       uuid                           idx  data                      units      type  genre cmdclass help
    0225/0004  switch                         0    off                       None       5     1     37       A switch. Valid values are : ['on', 'off']
    0225/0004  blink                          0    heartbeat                 None       5     1     12803    Blink
    0225/0000  tutorial2_transition           0    wakeup                    None       5     1     4272     Trigger a transition on the fsm or get the last triggered
    0225/0000  tutorial2_state                0    reporting                 None       8     1     49       The state of the fsm.
