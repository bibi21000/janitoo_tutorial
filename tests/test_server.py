# -*- coding: utf-8 -*-

"""Unittests for Janitoo-Raspberry Pi Server.
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

import warnings
warnings.filterwarnings("ignore")

import sys, os
import time, datetime
import unittest
import threading
import logging
from pkg_resources import iter_entry_points

from janitoo_nosetests.server import JNTTServer, JNTTServerCommon
from janitoo_nosetests.thread import JNTTThread, JNTTThreadCommon

from janitoo.utils import json_dumps, json_loads
from janitoo.utils import HADD_SEP, HADD
from janitoo.utils import TOPIC_HEARTBEAT, NETWORK_REQUESTS
from janitoo.utils import TOPIC_NODES, TOPIC_NODES_REPLY, TOPIC_NODES_REQUEST
from janitoo.utils import TOPIC_BROADCAST_REPLY, TOPIC_BROADCAST_REQUEST
from janitoo.utils import TOPIC_VALUES_USER, TOPIC_VALUES_CONFIG, TOPIC_VALUES_SYSTEM, TOPIC_VALUES_BASIC
from janitoo.thread import JNTBusThread

from janitoo_rantanplan.server import RantanplanServer

##############################################################
#Check that we are in sync with the official command classes
#Must be implemented for non-regression
from janitoo.classes import COMMAND_DESC

COMMAND_DISCOVERY = 0x5000

assert(COMMAND_DESC[COMMAND_DISCOVERY] == 'COMMAND_DISCOVERY')
##############################################################

class TestRantanplanServer(JNTTServer, JNTTServerCommon):
    """Test the pi server
    """
    loglevel = logging.DEBUG
    path = '/tmp/janitoo_test'
    broker_user = 'toto'
    broker_password = 'toto'
    server_class = RantanplanServer
    server_conf = "tests/data/janitoo_rantanplan.conf"
    server_section = "rantanplan"

    hadds = [HADD%(222,0), HADD%(222,1), HADD%(222,2), HADD%(222,3), HADD%(222,4), HADD%(222,5), HADD%(222,6)]

    def test_011_start_reload_stop(self):
        self.skipRasperryTest()
        JNTTServerCommon.test_011_start_reload_stop(self)

    def test_012_start_reload_threads_stop(self):
        self.skipRasperryTest()
        JNTTServerCommon.test_012_start_reload_threads_stop(self)

    def test_030_wait_for_all_nodes(self):
        self.skipRasperryTest()
        JNTTServerCommon.test_030_wait_for_all_nodes(self)

    def test_100_server_start_machine_state(self):
        self.start()
        time.sleep(10)
        thread = self.server.find_thread(self.server_section)
        self.assertNotEqual(thread, None)
        self.assertIsInstance(thread, JNTBusThread)
        bus = thread.bus
        self.assertNotEqual(bus, None)
        self.waitHeartbeatNodes(hadds=self.hadds)
        bus.guard()
        time.sleep(5)
        bus.report()
        time.sleep(5)
        bus.guard()
        time.sleep(5)
        bus.bark()
        time.sleep(5)
        bus.guard()
        time.sleep(5)
        bus.bark()
        time.sleep(5)
        bus.bite()
        time.sleep(5)
        bus.sleep()
