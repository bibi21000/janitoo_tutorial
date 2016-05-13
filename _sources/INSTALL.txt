=========================
Installation for tutorial
=========================

Needed tools
============

Janitoo uses mosquitto as a MQTT server. On Debian or Ubuntu, install it using :

.. code:: bash

    sudo apt-get install mosquitto netcat-openbsd

We install netcat too. So that we can verify that mosquitto is listen on port 1883 on your local interface :

.. code:: bash

    netcat -zv 127.0.0.1 1-9999 2>&1|grep succeeded

.. code:: bash

    Connection to 127.0.0.1 1883 port [tcp/*] succeeded!

Initial clone
=============

Create a directory for Janitoo.
It is recommended to use the default one (/opt/janitoo), unless you're ready to update a lot a configuration files :

.. code:: bash

    sudo mkdir -p /opt/janitoo/src

Janitoo is hosted on github, so you need to clone it into the created directory.
/opt/janitoo/src is called the janitoo source.

.. code:: bash

    cd /opt/janitoo/src
    git clone https://github.com/bibi21000/janitoo.git

Janitoo has a makefile for semi-automated installations. Let's link it :

.. code:: bash

    ln -s /opt/janitoo/src/janitoo/Makefile.all Makefile

And use it. Create the needed directories for Janitoo:

.. code:: bash

    sudo make directories

Install dependencies and develop sources for Python:

.. code:: bash

    sudo make module=janitoo deps
    sudo make module=janitoo develop

Create the list of packages in /opt/janitoo/src using your favorite editor ... or vim ;) :

.. code:: bash

    vim Makefile.local

Order is important. If some package appears in eggs dependencies before they've been downloaded, you'll run a 'binary' version of the package, not the one installed in src.

.. code:: bash

    # Makefile for local
    #

    SUBMODULES = janitoo_nosetests janitoo janitoo_factory janitoo_factory_exts\
     janitoo_hostsensor_raspberry janitoo_raspberry janitoo_raspberry_gpio janitoo_raspberry_dht \
     janitoo_raspberry_1wire \
     janitoo_tutorial

You're now ready to clone the needed modules. sudo password may be asked during this phase :

.. code:: bash

    make clone-all

Wait, wait and wait, specially on a raspberry.

After that, all the depencies are installed. You can jump to the first tutorial.

Update your clone
=================

You can update all modules using :

.. code:: bash

    make pull-all

Some packages may have update their entry-point, you need to develop all :

.. code:: bash

    sudo make develop-all

To uninstall :

.. code:: bash

    sudo make uninstall-all

If you encounter strange errors, missing modules, ..., uninstall (maybe twice) and develop again :

.. code:: bash

    sudo make uninstall-all
    sudo make develop-all
