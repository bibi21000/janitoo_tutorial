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

from janitoo.thread import JNTBusThread, BaseThread
from janitoo.options import get_option_autostart
from janitoo.utils import HADD
from janitoo.node import JNTNode
from janitoo.value import JNTValue
from janitoo.component import JNTComponent
from janitoo.bus import JNTBus

from janitoo_raspberry_dht.dht import DHTComponent
from janitoo_raspberry_gpio.gpio import GpioBus, LedComponent as GPIOLed
from janitoo_raspberry_1wire.bus_1wire import OnewireBus
from janitoo_raspberry_1wire.components import DS18B20
from janitoo_hostsensor_raspberry.component import HardwareCpu

OID = 'tutorial2'

def make_ambiance(**kwargs):
    return AmbianceComponent(**kwargs)

def make_temperature(**kwargs):
    return TemperatureComponent(**kwargs)

def make_cpu(**kwargs):
    return CpuComponent(**kwargs)

class TutorialBus(JNTBus):
    """A bus to manage Tutorial
    """

    def __init__(self, **kwargs):
        """
        """
        JNTBus.__init__(self, **kwargs)
        self.buses = {}
        self.buses['gpiobus'] = GpioBus(masters=[self], **kwargs)
        self.buses['1wire'] = OnewireBus(masters=[self], **kwargs)
        uuid="{:s}_temperature".format(OID)
        self.values[uuid] = self.value_factory['sensor_temperature'](options=self.options, uuid=uuid,
            node_uuid=self.uuid,
            get_data_cb=self.get_temperature_cb,
            help='The average temperature of tutorial. Can be use as a good quality source for a thermostat.',
            label='Temp',
        )
        poll_value = self.values[uuid].create_poll_value(default=300)
        self.values[poll_value.uuid] = poll_value

    def start(self, mqttc, trigger_thread_reload_cb=None):
        """Start the bus
        """
        for bus in self.buses:
            self.buses[bus].start(mqttc, trigger_thread_reload_cb=None)
        JNTBus.start(self, mqttc, trigger_thread_reload_cb)

    def stop(self):
        """Stop the bus
        """
        for bus in self.buses:
            self.buses[bus].stop()
        JNTBus.stop(self)

    def loop(self, stopevent):
        """Retrieve data
        Don't do long task in loop. Use a separated thread to not perturbate the nodeman

        """
        for bus in self.buses:
            self.buses[bus].loop(stopevent)

    def get_temperature_cb(self, node_uuid=None, index=None):
        """Callback for average temperature"""
        nums = 0
        total = 0
        for value in [('temperature', 'temperature'), ('ambiance', 'temperature'), ('cpu', 'temperature')]:
            data = self.nodeman.find_value(*value).data
            if data is not None:
                nums += 1
                total += data
        if nums > 0:
            return 1.0 * total / nums
        return None

class AmbianceComponent(DHTComponent):
    """ A component for ambiance """

    def __init__(self, bus=None, addr=None, **kwargs):
        """
        """
        oid = kwargs.pop('oid', '%s.ambiance'%OID)
        name = kwargs.pop('name', "Ambiance sensor")
        DHTComponent.__init__(self, oid=oid, bus=bus, addr=addr, name=name,
                **kwargs)
        logger.debug("[%s] - __init__ node uuid:%s", self.__class__.__name__, self.uuid)

class TemperatureComponent(DS18B20):
    """ A water temperature component """

    def __init__(self, bus=None, addr=None, **kwargs):
        """
        """
        oid = kwargs.pop('oid', '%s.temperature'%OID)
        name = kwargs.pop('name', "Temperature")
        DS18B20.__init__(self, oid=oid, bus=bus, addr=addr, name=name,
                **kwargs)
        logger.debug("[%s] - __init__ node uuid:%s", self.__class__.__name__, self.uuid)

class CpuComponent(HardwareCpu):
    """ A water temperature component """

    def __init__(self, bus=None, addr=None, **kwargs):
        """
        """
        oid = kwargs.pop('oid', '%s.cpu'%OID)
        name = kwargs.pop('name', "CPU")
        HardwareCpu.__init__(self, oid=oid, bus=bus, addr=addr, name=name,
                **kwargs)
        logger.debug("[%s] - __init__ node uuid:%s", self.__class__.__name__, self.uuid)
