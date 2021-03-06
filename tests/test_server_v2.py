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

from janitoo_nosetests.server import JNTTServer, JNTTServerCommon
from janitoo.utils import HADD_SEP, HADD
from janitoo_raspberry.server import PiServer

class TestTutorialServer(JNTTServer, JNTTServerCommon):
    """Test the tutorial server
    """
    server_class = PiServer
    server_conf = "tests/data/helloworldv2.conf"
    server_section = "tutorial2"

    hadds = [HADD%(225,0), HADD%(225,1), HADD%(225,2), HADD%(225,3)]

    def test_040_server_start_no_error_in_log(self):
        self.onlyRasperryTest()
        JNTTServerCommon.test_040_server_start_no_error_in_log(self)
