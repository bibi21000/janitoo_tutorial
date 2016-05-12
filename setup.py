#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Setup file of Janitoo
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

from os import name as os_name
from setuptools import setup, find_packages
from platform import system as platform_system
import glob
import os
import sys
from _version import janitoo_version

DEBIAN_PACKAGE = False
filtered_args = []

for arg in sys.argv:
    if arg == "--debian-package":
        DEBIAN_PACKAGE = True
    else:
        filtered_args.append(arg)
sys.argv = filtered_args

def data_files_config(res, rsrc, src, pattern):
    for root, dirs, fils in os.walk(src):
        if src == root:
            sub = []
            for fil in fils:
                sub.append(os.path.join(root,fil))
            res.append((rsrc, sub))
            for dire in dirs:
                    data_files_config(res, os.path.join(rsrc, dire), os.path.join(root, dire), pattern)

data_files = []
data_files_config(data_files, 'docs','src/docs/','*')

setup(
    name = 'janitoo_tutorial',
    description = "A server which handle many controller (hardware, onewire, i2c, ...) dedicated to the raspberry",
    long_description = "A server which handle many controller (hardware, onewire, i2c, ...) dedicated to the raspberry",
    author='Sébastien GALLET aka bibi2100 <bibi21000@gmail.com>',
    author_email='bibi21000@gmail.com',
    url='http://bibi21000.gallet.info/',
    license = """
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
    """,
    version = janitoo_version,
    zip_safe = False,
    scripts=['src/scripts/jnt_tutorial'],
    packages = find_packages('src', exclude=["scripts", "docs", "config"]),
    package_dir = { '': 'src' },
    keywords = "raspberry,tutorial",
    include_package_data=True,
    data_files = data_files,
    install_requires=[
                     'janitoo',
                     'janitoo_factory',
                     'janitoo_factory_exts',
                     'janitoo_raspberry',
                     'janitoo_raspberry_gpio',
                     'janitoo_raspberry_1wire',
                     'janitoo_raspberry_dht',
                     'janitoo_hostsensor',
                     'janitoo_hostsensor_raspberry',
                    ],
    dependency_links = [
      'https://github.com/bibi21000/janitoo/archive/master.zip#egg=janitoo',
      'https://github.com/bibi21000/janitoo_factory/archive/master.zip#egg=janitoo_factory',
      'https://github.com/bibi21000/janitoo_factory_exts/archive/master.zip#egg=janitoo_factory_exts',
      'https://github.com/bibi21000/janitoo_raspberry/archive/master.zip#egg=janitoo_raspberry',
      'https://github.com/bibi21000/janitoo_raspberry_1wire/archive/master.zip#egg=janitoo_raspberry_1wire',
      'https://github.com/bibi21000/janitoo_raspberry_dht/archive/master.zip#egg=janitoo_raspberry_dht',
      'https://github.com/bibi21000/janitoo_raspberry_gpio/archive/master.zip#egg=janitoo_raspberry_gpio',
      'https://github.com/bibi21000/janitoo_raspberry_i2c/archive/master.zip#egg=janitoo_raspberry_i2c',
      'https://github.com/bibi21000/janitoo_raspberry_i2c_ds1307/archive/master.zip#egg=janitoo_raspberry_i2c_ds1307',
      'https://github.com/bibi21000/janitoo_hostsensor/archive/master.zip#egg=janitoo_hostsensor',
      'https://github.com/bibi21000/janitoo_hostsensor_raspberry/archive/master.zip#egg=janitoo_hostsensor_raspberry',
    ],
    entry_points = {
        "janitoo.threads": [
            "tutorial1 = janitoo_tutorial.thread_tutorial1:make_thread",
            "tutorial2 = janitoo_tutorial.thread_tutorial2:make_thread",
        ],
        "janitoo.components": [
            "tutorial1.ambiance = janitoo_tutorial.tutorial1:make_ambiance",
            "tutorial1.cpu = janitoo_tutorial.tutorial1:make_cpu",
            "tutorial1.temperature = janitoo_tutorial.tutorial1:make_temperature",
            "tutorial1.led = janitoo_tutorial.tutorial1:make_led",
            "tutorial2.ambiance = janitoo_tutorial.tutorial12:make_ambiance",
            "tutorial2.cpu = janitoo_tutorial.tutorial2:make_cpu",
            "tutorial2.temperature = janitoo_tutorial.tutorial2:make_temperature",
            "tutorial2.led = janitoo_tutorial.tutorial2:make_led",
        ],
    },
)
