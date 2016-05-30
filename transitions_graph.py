#!/usr/bin/python
#From https://gist.github.com/svdgraaf/198e2c0cf4cf0a031c84
import pygraphviz as pgv
import threading

from janitoo.options import JNTOptions
from janitoo_tutorial.tutorial3 import TutorialBus as Bus3
from janitoo_tutorial.tutorial4 import TutorialBus as Bus4

bus = Bus3(options=JNTOptions({}))
fsm = bus.create_fsm()
fsm.show_graph(fname='rst/images/fsm_bus_3.png', prog='dot')

bus = Bus4(options=JNTOptions({}))
fsm = bus.create_fsm()
fsm.show_graph(fname='rst/images/fsm_bus_4.png', prog='dot')
