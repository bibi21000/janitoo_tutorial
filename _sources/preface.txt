=======
Janitoo
=======


Preface
=======

In short words, Janitoo is a protocol based on mqtt. Its API allows rapid development of appliance server for Raspberry Pi ( mainly but not only).

The protocol is approximatively 60% developped : fixed addresses, primary nodes are functionnals.

The protocol implements the concepts of network, nodes and values :

- a network holds nodes
- primary nodes and secondary nodes holds a map on the network
- a secondary node can became primary if the primary fails
- primary nodes (and maybe secondary ones) will send heartbeat for nodes in timeout
- a node holds values
- a value holds instances (not fully supported)

If you're famillar with Zwave (https://github.com/OpenZWave/open-zwave), Janitoo's protocol is a kind of Zwave over mqtt

The API implements the concepts of thread/bus, components and values :

- a bus allows to share resources between its holded components. Each bus run in its own thread. A bus is mapped to a node in the protocol (in a controller node to be more precise)
- a component is mapped to a node

You can see Janitoo in action here : https://www.youtube.com/watch?v=S3Gqj32sJ-Q

Look at the time line in description.


About this tutorial
===================

- it will take 1 or 2 hours for the all tutorial (or maybe less).
- all code is provided, just look at the specified file to look around.
- all configuration files are provided, you simply need to copy them the right place.


Notes
=====

- the web manager is 20% functionnal : you can only browse values, no updates. There is a huge memory hole in it (with socketio)
- the flask socketio server and socketio server are under heavy development after a period of inactivity, so installation problems will occurs
- maybe we should use websockets instead
