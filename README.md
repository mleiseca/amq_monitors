amq_monitors
============

Purpose
-------

You want to watch an ActiveMQ broker or queue in realtime and monitor the enqueue/dequeue rate

Usage
-----

### Single point in time output
python scalability.py --hostname localhost --port 1099 --queue "myqueue" --broker mybroker

python scalability.py --hostname localhost --port 1099 --broker mybroker --interval 10

### Continuous monioring

This will create a file based on the start execution time and keep invoking scalability.py and logging the output

./harness.sh --hostname localhost --port 1099 --broker mybroker --interval 30


Output
------
date,time,enqueue rate, dequeue rate, rate_difference

eg:

    2013-03-08,10:48:08,0.0000,0.0000,0.0000
    2013-03-08,10:48:30,0.0000,0.0000,0.0000
    2013-03-08,10:48:53,4.2000,4.2000,0.0000
