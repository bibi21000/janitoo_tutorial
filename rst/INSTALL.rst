=========================
Installation for tutorial
=========================

Needed tools
============

.. code:: bash

    sudo apt-get install mosquitto

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

Janitoo has a makefile

.. code:: bash

    ln -s /opt/janitoo/src/janitoo/Makefile.all Makefile

Create the directories for Janitoo:

.. code:: bash

    sudo make directories

Install dependencies and develop sources for Python:

.. code:: bash

    sudo make module=janitoo deps
    sudo make module=janitoo develop

Create the list of packages in /opt/janitoo/src using your favorite editor ... or vim ;) :
Order is important

.. code:: bash

    vim Makefile.local

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

After that, all the depencies are installed.
