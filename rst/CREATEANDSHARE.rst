================
Create and share
================

With Janitoo you can easely share your components, threads and values.

Why
===

 - Re-use of code
 - Tests

How
===

 - Create your components
 - Write tests (at least 80% coverage)
 - Submit pull requests to janitoo_factory or janitoo_factory_exts repositories.

For more complex developments, you can also ask to add your github directory to : https://github.com/bibi21000/janitoo_docker.

Bus aggregation vs bus extension
================================

In the previous tutorials, we aggregate many buses in a single one. But sometimes, this way of doing is not sufficient.

For example, for ic2_pca9865 component, I need to share the pca9865 module between many components (ie to manage 2 DC motors and 1 stepper).
This can be done by extending the i2c bus to hold the shared mode.
Look at : https://github.com/bibi21000/janitoo_raspberry_i2c_pca9685/blob/master/src/janitoo_raspberry_i2c_pca9685/bus_pca9685.py

For the spi bus, extensions allows to use the same bus for hardware and software SPI.
Look at : https://github.com/bibi21000/janitoo_raspberry_spi/blob/master/src/janitoo_raspberry_spi/bus_spi.py

You need to define an entry-point for your bus extension in your setup.py :

.. code:: python

    "rpii2c.extensions": [
        "pca9865 = janitoo_raspberry_i2c_pca9685.bus_pca9685:extend",
    ],

And load extension in your configuration file :

.. code:: bash

    [rpispi]
    auto_start = True
    hadd = 0159/0000
    heartbeat = 30
    extensions = hardware

Remote development
==================

If you try to develop on raspberry, you surely seen how it is ... slow.

With Janitoo and and its tests, you can simply create your server and tests on your personal computer.
On travis, this tutorial has a coverage greater than 80%, this also means that more than 80% of the code is tested out of the box (out of the Raspberry).

Tests
=====

Janitoo is a test driven development.

Janitoo has 2 tests modules (janitoo_nosetests and janitoo_nosetests_flask).
They define framework for testing servers, threads, buses, compenents, values, ...

They also define tests that will check that your component is valid with the janitoo protocol.
When the protocol will be updated, these tess will too.

Ideally, when a new bug is reported, the workflow should be : bug -> test to reproduce the bug -> fix for the bug.

Testing tools
-------------

TravisCI : https://travis-ci.org/search/janitoo


CircleCI : https://circleci.com/gh/bibi21000

Docker : there is a docker image to launch but it should not be launched on Docker Hub (timeout after 2 hours).
You can launch it locally, look at https://github.com/bibi21000/janitoo_docker

Raspberry : you can launch tests on your raspberry using : sudo make tests-all (from the /opt/janitoo/src direcotry)

Examples
========

Values
------

Ip ping
^^^^^^^
A value to ping an IP.

Code : https://github.com/bibi21000/janitoo_factory_exts/blob/master/src/janitoo_factory_exts/values/ping.py

Example : https://github.com/bibi21000/janitoo_nut/blob/master/src/janitoo_nut/nut.py#L89

Test : https://github.com/bibi21000/janitoo_factory_exts/blob/master/tests/test_values.py

Blink
^^^^^
A value to blink ... everything. Use callback to perform the action

Code : https://github.com/bibi21000/janitoo_factory_exts/blob/master/src/janitoo_factory_exts/values/blink.py

Example : https://github.com/bibi21000/janitoo_raspberry_gpio/blob/master/src/janitoo_raspberry_gpio/gpio.py#L764

Test : https://github.com/bibi21000/janitoo_factory_exts/blob/master/tests/test_values.py

Components and bus
------------------

Look at rasperry i2c :

 - https://github.com/bibi21000/janitoo_raspberry_i2c_bmp
 - https://github.com/bibi21000/janitoo_raspberry_i2c_pca9685
