=======
Janitoo
=======


Preface
=======

In short words, Janitoo is a protocol based on mqtt. Its API allows rapid development of appliance server for Raspberry Pi ( mainly but not only).

The protocol is approximatively 60% developped : fixed addresses, primary mode are functionnals.

The protocol implements the concepts of network, nodes and values :

 - a network holds nodes
 - a node holds values
 - a value holds instances (not fully supported)

If you're famillar with Zwave (https://github.com/OpenZWave/open-zwave), Janitoo's protocol is a kind of Zwave over mqtt

The API implements the concepts of thread/bus, components and values :

 - a bus allows to share resources between its holded components. Each bus run in its own thread. A bus is mapped to a node in the protocol (in a controller node to be more precise)
 - a component is mapped to a node

You can see Janitoo in action here : https://www.youtube.com/watch?v=S3Gqj32sJ-Q

Look at the time line in description.

Some notes :

 - the web manager is 20% functionnal : you can only browse values, no updates. There is a huge memory hole in it (with socketio)
 - the flask socketio server and socketio server are under heavy development after a period of inactivity, so installation problems will occurs
 - maybe we should use websockets instead
