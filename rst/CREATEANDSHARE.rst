================
Create and share
================

With Janitoo you can easely share your components, threads and values.

Why
===

 - re-use of code
 - tests

How
===

 - Create your components
 - write tests (at least 90% coverage)

And submit pull requests to janitoo_factory or janitoo_factory_exts repositories.

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

Look at rasperry i2c
