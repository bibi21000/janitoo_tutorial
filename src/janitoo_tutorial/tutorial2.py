# -*- coding: utf-8 -*-
"""The Raspberry tutorial

"""

__license__ = """
    This file is part of Janitoo.

    Janitoo is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Janitoo is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Janitoo. If not, see <http://www.gnu.org/licenses/>.

"""
__author__ = 'Sébastien GALLET aka bibi21000'
__email__ = 'bibi21000@gmail.com'
__copyright__ = "Copyright © 2013-2014-2015-2016 Sébastien GALLET aka bibi21000"

import logging
logger = logging.getLogger(__name__)
import os, sys
import threading
import datetime

from transitions.extensions import HierarchicalMachine as Machine

from janitoo.thread import JNTBusThread, BaseThread
from janitoo.options import get_option_autostart
from janitoo.utils import HADD
from janitoo.node import JNTNode
from janitoo.value import JNTValue
from janitoo.component import JNTComponent
from janitoo.bus import JNTBus

from janitoo_raspberry_dht.dht import DHTComponent
from janitoo_raspberry_gpio.gpio import GpioBus, OutputComponent, PirComponent as GPIOPir, LedComponent as GPIOLed, SonicComponent
from janitoo_raspberry_1wire.bus_1wire import OnewireBus
from janitoo_raspberry_1wire.components import DS18B20
from janitoo_hostsensor_raspberry.component import HardwareCpu

##############################################################
#Check that we are in sync with the official command classes
#Must be implemented for non-regression
from janitoo.classes import COMMAND_DESC

COMMAND_WEB_CONTROLLER = 0x1030
COMMAND_WEB_RESOURCE = 0x1031
COMMAND_DOC_RESOURCE = 0x1032

assert(COMMAND_DESC[COMMAND_WEB_CONTROLLER] == 'COMMAND_WEB_CONTROLLER')
assert(COMMAND_DESC[COMMAND_WEB_RESOURCE] == 'COMMAND_WEB_RESOURCE')
assert(COMMAND_DESC[COMMAND_DOC_RESOURCE] == 'COMMAND_DOC_RESOURCE')
##############################################################

OID = 'tutorial2'

def make_ambiance(**kwargs):
    return AmbianceComponent(**kwargs)

def make_led(**kwargs):
    return LedComponent(**kwargs)

def make_temperature(**kwargs):
    return TemperatureComponent(**kwargs)

def make_cpu(**kwargs):
    return CpuComponent(**kwargs)

class TutorialBus(JNTBus):
    """A bus to manage Tutorial
    """

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

    def __init__(self, **kwargs):
        """
        """
        JNTBus.__init__(self, **kwargs)
        self.buses = {}
        self.buses['gpiobus'] = GpioBus(masters=[self], **kwargs)
        self.buses['1wire'] = OnewireBus(masters=[self], **kwargs)
        self._tutorial_statemachine =  None
        self.check_timer = None
        uuid="{:s}_timer_delay".format(OID)
        self.values[uuid] = self.value_factory['config_integer'](options=self.options, uuid=uuid,
            node_uuid=self.uuid,
            help='The delay between 2 checks',
            label='Timer.',
            default=45,
        )
        uuid="{:s}_temperature_critical".format(OID)
        self.values[uuid] = self.value_factory['config_integer'](options=self.options, uuid=uuid,
            node_uuid=self.uuid,
            help='The critical temperature. If 2 of the 3 temperature sensors are up to this value, a security notification is sent.',
            label='Critical',
            default=50,
        )
        self._bus_lock = threading.Lock()
        self.presence_events = {}

        uuid="{:s}_temperature".format(OID)
        self.values[uuid] = self.value_factory['sensor_temperature'](options=self.options, uuid=uuid,
            node_uuid=self.uuid,
            help='The average temperature of tutorial. Can be use as a good quality source for a thermostat.',
            label='Temp',
        )
        poll_value = self.values[uuid].create_poll_value(default=300)
        self.values[poll_value.uuid] = poll_value

    @property
    def polled_sensors(self):
        """
        """
        return [
            self.nodeman.find_value('temperature', 'temperature'),
            self.nodeman.find_value('ambiance', 'temperature'),
            self.nodeman.find_value('cpu', 'temperature'),
            self.nodeman.find_value('ambiance', 'humidity'),
        ]

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

    def on_enter_sleeping(self):
        """
        """
        logger.debug("[%s] - on_enter_sleeping", self.__class__.__name__)
        self.stop_check()
        self.bus_acquire()
        try:
            self.nodeman.remove_polls(self.polled_sensors)
            self.nodeman.find_value('led', 'blink').data = 'off'
        except:
            logger.exception("[%s] - Error in on_enter_sleeping", self.__class__.__name__)
        finally:
            self.bus_release()

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

    def bus_acquire(self, blocking=True):
        """Get a lock on the bus"""
        if self._bus_lock.acquire(blocking):
            return True
        return False

    def bus_release(self):
        """Release a lock on the bus"""
        self._bus_lock.release()

    def bus_locked(self):
        """Get status of the lock"""
        return self._bus_lock.locked()

    def stop_check(self):
        """Check that the component is 'available'

        """
        if self.check_timer is not None:
            self.check_timer.cancel()
            self.check_timer = None

    def on_check(self):
        """Make a check using a timer.

        """
        self.bus_acquire()
        try:
            self.stop_check()
            if self.check_timer is None and self.is_started:
                self.check_timer = threading.Timer(self.get_bus_value('timer_delay').data)
                self.check_timer.start()
            state = True
            #Check the temperatures
            critical_temp = self.get_bus_value('temperature_critical').data
            criticals = 0
            nums = 0
            total = 0
            mini = maxi = None
            for value in [('temperature', 'temperature'), ('ambiance', 'temperature'), ('cpu', 'temperature')]:
                data = self.nodeman.find_value(*value).data
                if data is None:
                    #We should notify a sensor problem here.
                    pass
                else:
                    nums += 1
                    total += data
                    if data > critical_temp:
                        criticals += 1
                    if maxi is None or data > maxi:
                        maxi = data
                    if mini is None or data < mini:
                        mini = data
            if criticals > 1:
                #We should notify a security problem : fire ?
                self.ring()
            if nums != 0:
                self.get_bus_value('temperature').data = total / nums
        except:
            logger.exception("[%s] - Error in on_check", self.__class__.__name__)
        finally:
            self.bus_release()

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

    def check_heartbeat(self):
        """Check that the component is 'available'

        """
        res = True
        #~ for bus in self.buses:
            #~ res = res and self.buses[bus].check_heartbeat()
        return res

    def loop(self, stopevent):
        """Retrieve data
        Don't do long task in loop. Use a separated thread to not perturbate the nodeman

        """
        for bus in self.buses:
            self.buses[bus].loop(stopevent)

class AmbianceComponent(DHTComponent):
    """ A component for ambiance """

    def __init__(self, bus=None, addr=None, **kwargs):
        """
        """
        oid = kwargs.pop('oid', 'tutorial2.ambiance')
        name = kwargs.pop('name', "Ambiance sensor")
        DHTComponent.__init__(self, oid=oid, bus=bus, addr=addr, name=name,
                **kwargs)
        logger.debug("[%s] - __init__ node uuid:%s", self.__class__.__name__, self.uuid)

class LedComponent(GPIOLed):
    """ A component for a Led (on/off) """

    def __init__(self, bus=None, addr=None, **kwargs):
        """
        """
        oid = kwargs.pop('oid', 'tutorial2.led')
        name = kwargs.pop('name', "Led")
        GPIOLed.__init__(self, oid=oid, bus=bus, addr=addr, name=name,
                **kwargs)
        logger.debug("[%s] - __init__ node uuid:%s", self.__class__.__name__, self.uuid)

class TemperatureComponent(DS18B20):
    """ A water temperature component """

    def __init__(self, bus=None, addr=None, **kwargs):
        """
        """
        oid = kwargs.pop('oid', 'tutorial2.temperature')
        name = kwargs.pop('name', "Temperature")
        DS18B20.__init__(self, oid=oid, bus=bus, addr=addr, name=name,
                **kwargs)
        logger.debug("[%s] - __init__ node uuid:%s", self.__class__.__name__, self.uuid)

class CpuComponent(HardwareCpu):
    """ A water temperature component """

    def __init__(self, bus=None, addr=None, **kwargs):
        """
        """
        oid = kwargs.pop('oid', 'tutorial2.cpu')
        name = kwargs.pop('name', "CPU")
        HardwareCpu.__init__(self, oid=oid, bus=bus, addr=addr, name=name,
                **kwargs)
        logger.debug("[%s] - __init__ node uuid:%s", self.__class__.__name__, self.uuid)
