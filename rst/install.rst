=========================
Installation for tutorial
=========================

Goal
====

Install mosquitto (the messagging system) and clone Janitoo.


Needed tools
============

Janitoo uses mosquitto as a MQTT server. On Debian or Ubuntu, install it using :

.. code:: bash

    $ sudo apt-get install mosquitto netcat-openbsd

We install netcat too. So that we can verify that mosquitto is listen on port 1883 on your local interface :

.. code:: bash

    $ netcat -zv 127.0.0.1 1-9999 2>&1|grep succeeded

.. code:: bash

    Connection to 127.0.0.1 1883 port [tcp/*] succeeded!


Initial clone
=============

Create a directory for Janitoo.
It is recommended to use the default one (/opt/janitoo), unless you're ready to update a lot a configuration files :

.. code:: bash

    $ sudo mkdir -p /opt/janitoo/src

Janitoo is hosted on github, so you need to clone it into the created directory.
/opt/janitoo/src is called the janitoo source.

.. code:: bash

    $ cd /opt/janitoo/src
    $ git clone https://github.com/bibi21000/janitoo.git

Janitoo has a makefile for semi-automated installations. Let's link it :

.. code:: bash

    $ ln -s /opt/janitoo/src/janitoo/Makefile.all Makefile

And use it. Create the needed directories for Janitoo:

.. code:: bash

    $ sudo make directories

Install dependencies and develop sources for Python:

.. code:: bash

    $ sudo make module=janitoo deps
    $ sudo make module=janitoo develop

Create the list of packages in /opt/janitoo/src using your favorite editor ... or vim ;) :

.. code:: bash

    $ vim Makefile.local

Order is important. If some package appears in eggs dependencies before they've been downloaded, you'll run a 'binary' version of the package, not the one installed in src.

.. literalinclude:: ../../../Makefile.janitoo
   :language: bash


You're now ready to clone the needed modules. sudo password may be asked during this phase :

.. code:: bash

    $ make clone-all

Wait, wait and wait, specially on a raspberry.

After that, all the depencies are installed. You can jump to the first tutorial.


Install Client tools
====================

Janitoo contains remote client tools that you can install on your local computer (runing Debian or Ubuntu).
Simply clone the main janitoo package :

.. code:: bash

    $ sudo mkdir -p /opt/janitoo/src
    $ cd /opt/janitoo/src && git clone https://github.com/bibi21000/janitoo.git

And install it :

.. code:: bash

    $ cd /opt/janitoo/src/janitoo && sudo make develop

Check that the tools are correctly installed :

.. code:: bash

    $ jnt_query --help

.. code:: bash

    usage: jnt_query [-h] [--debug] [--output {txt,raw}]
                     {query,cmds,genres,types,caps,node,network} ...

    Browse and interact with the Janitoo nework.

    positional arguments:
      {query,cmds,genres,types,caps,node,network}
                            The command to launch
        query               Query a node value
        cmds                Show all available command classes for values
        genres              Show all available genres for values
        types               Show all available types for values
        caps                Show all available capabilties for a node
        node                Request infos from a node
        network             Request infos from network (broadcast)

    optional arguments:
      -h, --help            show this help message and exit
      --debug               Enable debug mode
      --output {txt,raw}    Enable debug mode

Update your clone
=================

It not need now, but you can update all modules in your clones using :

.. code:: bash

    $ make pull-all

Some packages may have update their entry-points, you need to develop all :

.. code:: bash

    $ sudo make develop-all

To uninstall :

.. code:: bash

    $ sudo make uninstall-all

If you encounter strange errors, missing modules, ..., uninstall (maybe twice) and develop again :

.. code:: bash

    $ sudo make uninstall-all
    $ sudo make develop-all
